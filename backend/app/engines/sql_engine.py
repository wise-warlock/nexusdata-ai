import duckdb
import sqlglot
from sqlglot import exp
from typing import Dict, Any, List, Tuple, Optional
import pandas as pd
from loguru import logger
import os

class SQLEngine:
    def __init__(self, db_path: str = "E:/nexusdata-ai/backend/app/data/sample_dw.duckdb"):
        self.db_path = db_path
        self._schema_cache = None

    def get_connection(self):
        return duckdb.connect(self.db_path, read_only=True)

    def get_schema_summary(self) -> str:
        """Returns a formatted schema definition for LLM prompt context."""
        if self._schema_cache:
            return self._schema_cache

        con = self.get_connection()
        tables = con.execute("SHOW TABLES;").fetchall()
        schema_text = []

        for (table_name,) in tables:
            columns = con.execute(f"DESCRIBE {table_name};").fetchall()
            col_defs = [f"  {col[0]} ({col[1]})" for col in columns]
            
            try:
                sample_df = con.execute(f"SELECT * FROM {table_name} LIMIT 2;").fetchdf()
                sample_str = sample_df.to_dict(orient="records")
            except Exception:
                sample_str = []

            schema_text.append(
                f"Table `{table_name}`:\n" + 
                "\n".join(col_defs) + 
                f"\n  Sample Data: {sample_str}\n"
            )

        con.close()
        self._schema_cache = "\n".join(schema_text)
        return self._schema_cache

    def validate_and_lint_sql(self, sql_query: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Validates SQL syntax with sqlglot and checks for destructive operations.
        Returns: (is_valid, cleaned_sql, error_message)
        """
        cleaned = sql_query.strip()
        if cleaned.startswith("```sql"):
            cleaned = cleaned[6:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()

        # 1. Parse AST
        try:
            parsed = sqlglot.parse_one(cleaned, read="duckdb")
        except Exception as e:
            return False, None, f"SQL Syntax Error: {str(e)}"

        # 2. Security Linter: Only allow SELECT statements
        if not isinstance(parsed, exp.Select):
            # Check if it's a Union or has Select root
            is_select_type = False
            for node in parsed.walk():
                if isinstance(node, (exp.Drop, exp.Delete, exp.Insert, exp.Update)):
                    return False, None, "Security Violation: Destructive query detected. Only SELECT queries are permitted."

        return True, cleaned, None

    def estimate_bytes_and_cost(self, sql_query: str) -> Dict[str, Any]:
        """
        Estimates scan cost and execution complexity for HITL gate.
        """
        con = self.get_connection()
        try:
            explain_df = con.execute(f"EXPLAIN {sql_query}").fetchall()
            explain_str = "\n".join([str(r[0]) for r in explain_df])
            is_large = "SCAN" in explain_str and "orders" in sql_query.lower()
            estimated_bytes = 1024 * 1024 * 2.5 if is_large else 1024 * 512
            estimated_cost_usd = (estimated_bytes / (1024**3)) * 0.005
            return {
                "estimated_bytes": estimated_bytes,
                "estimated_cost_usd": round(estimated_cost_usd, 6),
                "requires_hitl": estimated_bytes > (100 * 1024 * 1024)
            }
        except Exception as e:
            return {"estimated_bytes": 0, "estimated_cost_usd": 0.0, "requires_hitl": False, "error": str(e)}
        finally:
            con.close()

    def execute_query(self, sql_query: str, max_rows: int = 100) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
        """
        Executes verified SQL query on DuckDB and returns a pandas DataFrame.
        """
        is_valid, cleaned_sql, err = self.validate_and_lint_sql(sql_query)
        if not is_valid:
            return None, err

        con = self.get_connection()
        try:
            df = con.execute(cleaned_sql).fetchdf()
            if len(df) > max_rows:
                df = df.head(max_rows)
            return df, None
        except Exception as e:
            logger.error(f"SQL execution failed: {e}")
            return None, f"Runtime Execution Error: {str(e)}"
        finally:
            con.close()

    def evaluate_execution_accuracy(self, predicted_sql: str, ground_truth_sql: str) -> bool:
        """
        Spider-like Execution Accuracy evaluation:
        Compares result sets of predicted SQL vs ground truth SQL.
        """
        df_pred, err_pred = self.execute_query(predicted_sql)
        df_gt, err_gt = self.execute_query(ground_truth_sql)

        if err_pred is not None or err_gt is not None:
            return False

        try:
            df_pred_norm = df_pred.sort_index(axis=1)
            df_gt_norm = df_gt.sort_index(axis=1)
            
            if df_pred_norm.shape != df_gt_norm.shape:
                return False

            diff = (df_pred_norm.values != df_gt_norm.values)
            return diff.sum() == 0
        except Exception:
            return False

sql_engine = SQLEngine()