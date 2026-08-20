from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np

class VizEngine:
    """
    DATA-16 Visualization & Chart Recommendation Engine.
    Converts SQL execution DataFrames into interactive Apache ECharts & Recharts schemas.
    """

    @staticmethod
    def infer_column_types(df: pd.DataFrame) -> Dict[str, str]:
        types = {}
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]) or any(k in col.lower() for k in ["date", "month", "quarter", "year"]):
                types[col] = "temporal"
            elif pd.api.types.is_numeric_dtype(df[col]):
                types[col] = "numeric"
            else:
                types[col] = "categorical"
        return types

    def recommend_and_build_charts(self, df: pd.DataFrame, title: str = "Analysis Chart") -> List[Dict[str, Any]]:
        """
        Analyzes DataFrame structure and produces one or more optimal ECharts/Recharts schemas.
        """
        if df is None or df.empty or len(df.columns) < 2:
            return []

        col_types = self.infer_column_types(df)
        categorical_cols = [c for c, t in col_types.items() if t == "categorical"]
        temporal_cols = [c for c, t in col_types.items() if t == "temporal"]
        numeric_cols = [c for c, t in col_types.items() if t == "numeric"]

        charts = []

        # Scenario 1: Temporal Trend (Line or Area Chart)
        if temporal_cols and numeric_cols:
            x_col = temporal_cols[0]
            for y_col in numeric_cols[:2]:
                chart_schema = {
                    "id": f"chart_line_{x_col}_{y_col}",
                    "title": f"Xu hướng {y_col.replace('_', ' ').title()} theo {x_col.replace('_', ' ').title()}",
                    "type": "line",
                    "xAxis": {
                        "type": "category",
                        "data": [str(v) for v in df[x_col].tolist()]
                    },
                    "yAxis": {"type": "value"},
                    "series": [{
                        "name": y_col,
                        "type": "line",
                        "smooth": True,
                        "data": [float(v) if not pd.isna(v) else 0 for v in df[y_col].tolist()]
                    }],
                    "grid_width": "col-span-12 lg:col-span-6"
                }
                charts.append(chart_schema)

        # Scenario 2: Categorical Comparison (Bar Chart)
        if categorical_cols and numeric_cols:
            x_col = categorical_cols[0]
            # Primary Bar Chart
            bar_series = []
            for y_col in numeric_cols[:2]:
                bar_series.append({
                    "name": y_col.replace('_', ' ').title(),
                    "type": "bar",
                    "data": [float(v) if not pd.isna(v) else 0 for v in df[y_col].tolist()]
                })
            
            charts.append({
                "id": f"chart_bar_{x_col}",
                "title": f"So sánh theo {x_col.replace('_', ' ').title()}",
                "type": "bar",
                "xAxis": {
                    "type": "category",
                    "data": [str(v) for v in df[x_col].tolist()]
                },
                "yAxis": {"type": "value"},
                "series": bar_series,
                "grid_width": "col-span-12 lg:col-span-6"
            })

            # Scenario 3: Composition / Share (Pie/Donut Chart if <= 8 categories)
            if len(df) <= 8 and len(numeric_cols) >= 1:
                y_col = numeric_cols[0]
                pie_data = [
                    {"name": str(row[x_col]), "value": float(row[y_col]) if not pd.isna(row[y_col]) else 0}
                    for _, row in df.iterrows()
                ]
                charts.append({
                    "id": f"chart_pie_{x_col}_{y_col}",
                    "title": f"Cơ cấu tỷ trọng {y_col.replace('_', ' ').title()} theo {x_col.replace('_', ' ').title()}",
                    "type": "pie",
                    "series": [{
                        "name": y_col,
                        "type": "pie",
                        "radius": ["40%", "70%"],
                        "data": pie_data
                    }],
                    "grid_width": "col-span-12 lg:col-span-6"
                })

        # Fallback if no specific condition matched
        if not charts and len(df.columns) >= 2:
            x_col = df.columns[0]
            y_col = df.columns[1]
            charts.append({
                "id": "chart_default",
                "title": title,
                "type": "bar",
                "xAxis": {"type": "category", "data": [str(v) for v in df[x_col].tolist()]},
                "yAxis": {"type": "value"},
                "series": [{"name": y_col, "type": "bar", "data": [float(v) if str(v).replace('.','',1).isdigit() else 0 for v in df[y_col].tolist()]}],
                "grid_width": "col-span-12"
            })

        return charts

viz_engine = VizEngine()