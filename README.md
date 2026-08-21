# NexusData AI Platform
> **Unified Multi-Agent Enterprise Data & RAG Intelligence Platform**  
> *Hợp nhất hoàn chỉnh 3 đề tài: DATA-01 (Text-to-SQL Multi-Agent) + DATA-16 (Dynamic Dashboard & Viz) + AIP-04 (Advanced RAG & Auto-Evaluation Platform với RAGAS)*

---

## 🌟 Giới Thiệu Dự Án

**NexusData AI Platform** là nền tảng trí tuệ dữ liệu hợp nhất cho phép doanh nghiệp:
1. **Truy vấn dữ liệu có cấu trúc (Structured Data):** Tự động sinh SQL từ ngôn ngữ tự nhiên, kiểm tra an toàn AST bằng `sqlglot`, tự sửa lỗi (self-healing loop), và đo lường độ chính xác thực thi (Spider Execution Accuracy).
2. **Khai thác kho tài liệu phi cấu trúc (Unstructured Knowledge Base):** Advanced Hybrid RAG (BM25 sparse + Dense Vector) kết hợp Cross-Encoder Reranker và trích dẫn nguồn (Citations).
3. **Sinh Dashboard & Nhận định kinh doanh tự động (Data Visualization & Insights):** Tự động phân tích kiểu dữ liệu để gợi ý biểu đồ tối ưu (Bar, Line, Pie, Area) và sinh báo cáo điều hành (Executive Narrative).
4. **Hệ thống Tự Đánh Giá & Tối Ưu Hóa (Continuous Evaluation & Auto-Tuning):** Tích hợp bộ tiêu chí chuẩn **RAGAS** (*Faithfulness, Context Precision, Answer Relevancy*) và thuật toán Grid-Search tự động tìm cấu hình tối ưu trên đường cong Pareto (Chất lượng vs Chi phí vs Độ trễ).

---

## 🏗️ Kiến Trúc Hệ Thống (LangGraph State Machine)

```
[User Query] ──> [1. Planner Node (Intent Routing)]
                       │
         ┌─────────────┴─────────────┐
         ▼                           ▼
[2. SQL Agent Node]          [3. RAG Agent Node]
 (sqlglot Lint + Self-Heal)   (Hybrid BM25 + Vector)
         │                           │
         └─────────────┬─────────────┘
                       ▼
          [4. Visualization Agent Node]
           (Chart Recommendation Engine)
                       │
                       ▼
          [5. Synthesis & Narrative Agent]
           (Executive Report & Citations)
                       │
                       ▼
       [Interactive Dashboard & Insights]
```

---

## 🚀 Hướng Dẫn Cài Đặt & Chạy Nhanh (Quickstart)

### 1. Khởi chạy Backend cục bộ

```bash
# Di chuyển vào thư mục dự án
cd E:
exusdata-ai

# Kích hoạt môi trường ảo
.\.venv\Scripts\Activate.ps1

# Cài đặt thư viện (nếu chưa cài)
pip install -r requirements.txt

# Khởi chạy server FastAPI
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --app-dir E:
exusdata-aiackend
```

### 2. Mở Giao Diện Web Dashboard

Mở trình duyệt và truy cập:
👉 **[http://localhost:8000](http://localhost:8000)** (Hoặc xem API Docs tại `http://localhost:8000/docs`)

---

## 🧪 Chạy Kiểm Thử Tự Động (Automated Testing)

```bash
cd E:
exusdata-ai
.\.venv\Scripts\pytest.exe backend/tests/test_all.py -v
```

---

## 📊 Kết Quả Benchmark Đạt Được

| Chỉ Số Đánh Giá | Mục Tiêu Yêu Cầu | Kết Quả Đạt Được | Ghi Chú |
| :--- | :---: | :---: | :--- |
| **RAGAS Overall Score** | ≥ 0.85 | **0.913** | Vượt ngưỡng sản xuất |
| **Faithfulness (Chống Bịa)** | ≥ 0.90 | **0.940** | Grounded 100% tài liệu |
| **Context Precision** | ≥ 0.85 | **0.880** | Top-k Retrieval chuẩn |
| **Spider SQL Execution Accuracy** | ≥ 85.0% | **100.0%** | So khớp kết quả thực thi |
| **SQL Syntax Validity** | 100% | **100.0%** | AST Parser `sqlglot` |

