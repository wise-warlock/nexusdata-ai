import os
import duckdb
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

DB_PATH = "E:/nexusdata-ai/backend/app/data/sample_dw.duckdb"
DOCS_DIR = "E:/nexusdata-ai/backend/app/data/sample_docs"
BENCHMARK_DIR = "E:/nexusdata-ai/backend/app/data/eval_benchmarks"

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)
os.makedirs(BENCHMARK_DIR, exist_ok=True)

print("--- Seeding DuckDB Enterprise Warehouse ---")
con = duckdb.connect(DB_PATH)

# 1. Regions
con.execute("""
CREATE OR REPLACE TABLE regions (
    region_id VARCHAR PRIMARY KEY,
    region_name VARCHAR NOT NULL,
    country VARCHAR NOT NULL,
    regional_director VARCHAR NOT NULL
);
""")
con.execute("""
INSERT INTO regions VALUES 
('REG_NORTH', 'Miền Bắc', 'Vietnam', 'Nguyễn Văn Hải'),
('REG_CENTRAL', 'Miền Trung', 'Vietnam', 'Trần Thị Mai'),
('REG_SOUTH', 'Miền Nam', 'Vietnam', 'Lê Hoàng Nam'),
('REG_OVERSEAS', 'Quốc Tế', 'Global', 'David Smith');
""")

# 2. Categories
con.execute("""
CREATE OR REPLACE TABLE categories (
    category_id VARCHAR PRIMARY KEY,
    category_name VARCHAR NOT NULL,
    description VARCHAR
);
""")
con.execute("""
INSERT INTO categories VALUES 
('CAT_ELEC', 'Thiết Bị Điện Tử & Gia Dụng', 'Smart devices, IoT, Smart Home products'),
('CAT_AUTO', 'Phụ Kiện & Pin Xe Điện', 'EV batteries, chargers, automotive accessories'),
('CAT_SOFTWARE', 'Giải Pháp Phần Mềm & Cloud', 'SaaS, enterprise cloud licenses, AI modules'),
('CAT_SERVICES', 'Dịch Vụ Bảo Trì & Triển Khai', 'Consulting, maintenance and installation services');
""")

# 3. Products
con.execute("""
CREATE OR REPLACE TABLE products (
    product_id VARCHAR PRIMARY KEY,
    product_name VARCHAR NOT NULL,
    category_id VARCHAR NOT NULL,
    unit_price DOUBLE NOT NULL,
    cost_price DOUBLE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);
""")
con.execute("""
INSERT INTO products VALUES 
('PROD_01', 'Smart Home Hub Gateway X', 'CAT_ELEC', 2500000, 1500000, true),
('PROD_02', 'Camera AI An Ninh Ngoài Trời 4K', 'CAT_ELEC', 1800000, 1100000, true),
('PROD_03', 'Bộ Cảm Biến Khói & Gas Thông Minh', 'CAT_ELEC', 850000, 450000, true),
('PROD_04', 'Trụ Sạc Xe Điện Wallbox 7.4kW', 'CAT_AUTO', 14500000, 9500000, true),
('PROD_05', 'Bộ Cáp Sạc Di Động Type 2', 'CAT_AUTO', 4200000, 2800000, true),
('PROD_06', 'Gói Bản Quyền Cloud Analytics Enterprise', 'CAT_SOFTWARE', 45000000, 15000000, true),
('PROD_07', 'Module AI Tối Ưu Năng Lượng Tòa Nhà', 'CAT_SOFTWARE', 28000000, 8000000, true),
('PROD_08', 'Gói Dịch Vụ Bảo Trì Tiêu Chuẩn 1 Năm', 'CAT_SERVICES', 12000000, 6000000, true);
""")

# 4. Customers
con.execute("""
CREATE OR REPLACE TABLE customers (
    customer_id VARCHAR PRIMARY KEY,
    customer_name VARCHAR NOT NULL,
    customer_type VARCHAR NOT NULL,
    tier VARCHAR NOT NULL,
    region_id VARCHAR NOT NULL,
    created_at DATE NOT NULL,
    FOREIGN KEY (region_id) REFERENCES regions(region_id)
);
""")
con.execute("""
INSERT INTO customers VALUES 
('CUST_01', 'Tập Đoàn Bất Động Sản An Gia', 'Enterprise', 'Platinum', 'REG_NORTH', '2023-01-15'),
('CUST_02', 'Công Ty Cổ Phần Công Nghệ Sao Mai', 'B2B', 'Gold', 'REG_NORTH', '2023-03-20'),
('CUST_03', 'Chuỗi Căn Hộ Dịch Vụ Hưng Thịnh', 'Enterprise', 'Platinum', 'REG_SOUTH', '2023-02-10'),
('CUST_04', 'Đại Lý Phân Phối Thiết Bị Miền Trung', 'B2B', 'Gold', 'REG_CENTRAL', '2023-05-12'),
('CUST_05', 'Công Ty Vận Tải Xanh Toàn Cầu', 'Enterprise', 'Platinum', 'REG_SOUTH', '2023-06-01'),
('CUST_06', 'Khách Hàng Cá Nhân Lê Văn Tùng', 'B2C', 'Silver', 'REG_NORTH', '2024-01-10'),
('CUST_07', 'Khách Hàng Cá Nhân Phạm Thanh Hà', 'B2C', 'Standard', 'REG_SOUTH', '2024-02-18'),
('CUST_08', 'Công Ty Công Nghệ Đông Dương', 'B2B', 'Silver', 'REG_OVERSEAS', '2023-11-05');
""")

# 5. Sales Targets (Q1-Q4 for 2025)
con.execute("""
CREATE OR REPLACE TABLE sales_targets (
    target_id VARCHAR PRIMARY KEY,
    region_id VARCHAR NOT NULL,
    year INT NOT NULL,
    quarter INT NOT NULL,
    target_revenue DOUBLE NOT NULL,
    target_profit DOUBLE NOT NULL,
    FOREIGN KEY (region_id) REFERENCES regions(region_id)
);
""")
con.execute("""
INSERT INTO sales_targets VALUES 
('TGT_2025_Q1_NORTH', 'REG_NORTH', 2025, 1, 1500000000, 600000000),
('TGT_2025_Q2_NORTH', 'REG_NORTH', 2025, 2, 1800000000, 720000000),
('TGT_2025_Q3_NORTH', 'REG_NORTH', 2025, 3, 2200000000, 900000000),
('TGT_2025_Q4_NORTH', 'REG_NORTH', 2025, 4, 2500000000, 1000000000),

('TGT_2025_Q1_SOUTH', 'REG_SOUTH', 2025, 1, 2000000000, 800000000),
('TGT_2025_Q2_SOUTH', 'REG_SOUTH', 2025, 2, 2400000000, 950000000),
('TGT_2025_Q3_SOUTH', 'REG_SOUTH', 2025, 3, 2800000000, 1150000000),
('TGT_2025_Q4_SOUTH', 'REG_SOUTH', 2025, 4, 3200000000, 1300000000),

('TGT_2025_Q1_CENTRAL', 'REG_CENTRAL', 2025, 1, 800000000, 320000000),
('TGT_2025_Q2_CENTRAL', 'REG_CENTRAL', 2025, 2, 950000000, 380000000),
('TGT_2025_Q3_CENTRAL', 'REG_CENTRAL', 2025, 3, 1100000000, 450000000),
('TGT_2025_Q4_CENTRAL', 'REG_CENTRAL', 2025, 4, 1300000000, 520000000);
""")

# 6. Orders and Order Items
con.execute("""
CREATE OR REPLACE TABLE orders (
    order_id VARCHAR PRIMARY KEY,
    customer_id VARCHAR NOT NULL,
    region_id VARCHAR NOT NULL,
    order_date DATE NOT NULL,
    year INT NOT NULL,
    quarter INT NOT NULL,
    month INT NOT NULL,
    status VARCHAR NOT NULL,
    total_amount DOUBLE NOT NULL,
    total_profit DOUBLE NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (region_id) REFERENCES regions(region_id)
);
""")

con.execute("""
CREATE OR REPLACE TABLE order_items (
    item_id VARCHAR PRIMARY KEY,
    order_id VARCHAR NOT NULL,
    product_id VARCHAR NOT NULL,
    quantity INT NOT NULL,
    unit_price DOUBLE NOT NULL,
    discount_percent DOUBLE NOT NULL,
    line_total DOUBLE NOT NULL,
    line_profit DOUBLE NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
""")

np.random.seed(42)
customer_ids = ['CUST_01', 'CUST_02', 'CUST_03', 'CUST_04', 'CUST_05', 'CUST_06', 'CUST_07', 'CUST_08']
cust_region_map = {
    'CUST_01': 'REG_NORTH', 'CUST_02': 'REG_NORTH', 'CUST_06': 'REG_NORTH',
    'CUST_03': 'REG_SOUTH', 'CUST_05': 'REG_SOUTH', 'CUST_07': 'REG_SOUTH',
    'CUST_04': 'REG_CENTRAL', 'CUST_08': 'REG_OVERSEAS'
}
products_data = [
    ('PROD_01', 2500000, 1500000),
    ('PROD_02', 1800000, 1100000),
    ('PROD_03', 850000, 450000),
    ('PROD_04', 14500000, 9500000),
    ('PROD_05', 4200000, 2800000),
    ('PROD_06', 45000000, 15000000),
    ('PROD_07', 28000000, 8000000),
    ('PROD_08', 12000000, 6000000),
]

start_date = datetime(2025, 1, 1)
order_rows = []
item_rows = []
item_idx = 1

for i in range(1, 151):
    order_id = f'ORD_2025_{i:04d}'
    c_id = np.random.choice(customer_ids)
    r_id = cust_region_map[c_id]
    days_offset = np.random.randint(0, 260)
    o_date = start_date + timedelta(days=days_offset)
    year = o_date.year
    quarter = (o_date.month - 1) // 3 + 1
    month = o_date.month
    status = 'COMPLETED' if np.random.rand() > 0.05 else 'PROCESSING'
    
    num_items = np.random.randint(1, 4)
    order_total = 0.0
    order_profit = 0.0
    
    for _ in range(num_items):
        prod = products_data[np.random.randint(0, len(products_data))]
        p_id, p_price, p_cost = prod
        qty = np.random.randint(1, 15) if 'PROD_06' not in p_id else np.random.randint(1, 3)
        disc = np.random.choice([0.0, 0.05, 0.10, 0.15, 0.20])
        
        line_total = qty * p_price * (1 - disc)
        line_profit = line_total - (qty * p_cost)
        order_total += line_total
        order_profit += line_profit
        
        item_rows.append((f'ITEM_{item_idx:05d}', order_id, p_id, qty, p_price, disc, line_total, line_profit))
        item_idx += 1
        
    order_rows.append((order_id, c_id, r_id, o_date.strftime('%Y-%m-%d'), year, quarter, month, status, order_total, order_profit))

con.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", order_rows)
con.executemany("INSERT INTO order_items VALUES (?, ?, ?, ?, ?, ?, ?, ?)", item_rows)

print(f"Seeded: {len(order_rows)} orders, {len(item_rows)} order items into DuckDB successfully.")
con.close()

# 7. Write Documents
print("--- Creating Enterprise Knowledge Base Documents ---")
doc_sales_policy = """# CHÍNH SÁCH CHIẾT KHẤU VÀ BÁN HÀNG DOANH NGHIỆP NĂM 2025

## 1. Mục Đích & Phạm Vi Áp Dụng
Chính sách này áp dụng cho toàn bộ các kênh bán hàng trực tiếp (Direct Sales) và Đại lý phân phối (Channel Partners) trên toàn quốc thuộc Tập đoàn NexusData.

## 2. Khung Chiết Khấu Theo Cấp Đại Lý & Khách Hàng (Tier Discount)
- **Đại lý Cấp 1 (Platinum Partner):** 
  - Chiết khấu thương mại cố định: **20%** trên giá niêm yết cho các thiết bị phần cứng (Smart Home, Trụ sạc).
  - Chiết khấu dịch vụ & phần mềm Cloud Analytics: **25%**.
  - Điều kiện: Doanh số cam kết tối thiểu 2.000.000.000 VNĐ / Quý.
- **Đại lý Cấp 2 (Gold Partner):** 
  - Chiết khấu thương mại: **15%** cho phần cứng, **18%** cho phần mềm.
  - Điều kiện: Doanh số tối thiểu 800.000.000 VNĐ / Quý.
- **Khách hàng Doanh nghiệp VIP (Enterprise B2B):**
  - Mua số lượng lớn từ 10 đơn vị sản phẩm trở lên: Được chiết khấu bổ sung **5%**.
  - Đơn hàng thanh toán 100% trong vòng 7 ngày: Chiết khấu thanh toán sớm **2%**.

## 3. Quy Định Phê Duyệt Giá & Thẩm Quyền (Human-In-The-Loop Governance)
- Mọi đơn hàng có mức giảm giá vượt quá **22%** bắt buộc phải có phê duyệt bằng văn bản từ Giám đốc Khối Kinh doanh Khu vực (Regional Director).
- Đơn hàng trên 5.000.000.000 VNĐ cần Tổng Giám Đốc ký duyệt trước khi phát hành hợp đồng.
"""

with open(os.path.join(DOCS_DIR, "chinh_sach_chiet_khau_ban_hang_2025.md"), "w", encoding="utf-8") as f:
    f.write(doc_sales_policy)

doc_regional_strategy = """# CHIẾN LƯỢC KINH DOANH VÀ KẾ HOẠCH DOANH SỐ QUÝ 3 - KHU VỰC MIỀN BẮC

## 1. Đánh Giá Hiện Trạng Quý 3 Miền Bắc
- Chỉ tiêu doanh thu Quý 3 năm 2025 cho khu vực Miền Bắc được giao là **2.200.000.000 VNĐ** với mục tiêu lợi nhuận gộp là **900.000.000 VNĐ**.
- Giám đốc phụ trách khu vực: Ông **Nguyễn Văn Hải**.

## 2. Trọng Tâm Tăng Trưởng & Sản Phẩm Chủ Lực
- Đẩy mạnh triển khai giải pháp *Smart Home Hub Gateway X* và *Trụ Sạc Xe Điện Wallbox 7.4kW* vào các dự án khu đô thị mới tại Hà Nội và Hải Phòng.
- Nhóm khách hàng chiến lược: Tập Đoàn Bất Động Sản An Gia và Công Ty Cổ Phần Công Nghệ Sao Mai.

## 3. Chính Sách Khuyến Khích Đột Phá Quý 3
- Hỗ trợ gói dùng thử 3 tháng miễn phí gói *Module AI Tối Ưu Năng Lượng Tòa Nhà* khi ký hợp đồng triển khai trên 50 trụ sạc.
- Thưởng nóng 3% doanh thu thuần cho đội ngũ kinh doanh khi hoàn thành vượt mức 115% chỉ tiêu quý.
"""

with open(os.path.join(DOCS_DIR, "chien_luoc_kinh_doanh_q3_mien_bac.md"), "w", encoding="utf-8") as f:
    f.write(doc_regional_strategy)

doc_warranty = """# QUY TRÌNH BẢO HÀNH VÀ HỖ TRỢ KỸ THUẬT SẢN PHẨM

## 1. Thời Hạn Bảo Hành Tiêu Chuẩn
- **Trụ Sạc Xe Điện Wallbox:** Bảo hành chính hãng 36 tháng, 1 đổi 1 trong 30 ngày đầu nếu lỗi nhà sản xuất.
- **Smart Home Hub & Camera AI:** Bảo hành 24 tháng.
- **Gói Phần Mềm Cloud Analytics:** Cam kết SLA 99.9% uptime, hỗ trợ kỹ thuật 24/7.

## 2. Quy Trình Tiếp Nhận & Phản Hồi Sự Cố
- Tiếp nhận sự cố qua cổng hỗ trợ hoặc AI Helpdesk.
- Đội kỹ thuật phản hồi trong vòng 2 giờ đối với sự cố mức Nghiêm trọng (Severity 1).
"""

with open(os.path.join(DOCS_DIR, "quy_trinh_bao_hanh_va_hoan_tra.md"), "w", encoding="utf-8") as f:
    f.write(doc_warranty)

# 8. Create Ground-Truth Benchmarks
print("--- Creating Evaluation Benchmarks (Spider & Ragas) ---")

spider_benchmarks = [
    {
        "id": "SQL_EVAL_01",
        "question": "Tổng doanh thu và lợi nhuận của từng khu vực trong năm 2025 là bao nhiêu?",
        "ground_truth_sql": "SELECT r.region_name, SUM(o.total_amount) as total_revenue, SUM(o.total_profit) as total_profit FROM orders o JOIN regions r ON o.region_id = r.region_id WHERE o.year = 2025 GROUP BY r.region_name ORDER BY total_revenue DESC;",
        "difficulty": "easy"
    },
    {
        "id": "SQL_EVAL_02",
        "question": "Liệt kê top 3 sản phẩm có doanh số bán cao nhất trong quý 3 năm 2025?",
        "ground_truth_sql": "SELECT p.product_name, SUM(oi.quantity) as total_qty, SUM(oi.line_total) as total_sales FROM order_items oi JOIN products p ON oi.product_id = p.product_id JOIN orders o ON oi.order_id = o.order_id WHERE o.year = 2025 AND o.quarter = 3 GROUP BY p.product_name ORDER BY total_sales DESC LIMIT 3;",
        "difficulty": "medium"
    },
    {
        "id": "SQL_EVAL_03",
        "question": "So sánh doanh thu thực tế và chỉ tiêu doanh thu của khu vực Miền Bắc theo từng quý năm 2025?",
        "ground_truth_sql": "SELECT st.quarter, st.target_revenue, COALESCE(SUM(o.total_amount), 0) as actual_revenue, (COALESCE(SUM(o.total_amount), 0) - st.target_revenue) as variance FROM sales_targets st JOIN regions r ON st.region_id = r.region_id LEFT JOIN orders o ON st.region_id = o.region_id AND st.year = o.year AND st.quarter = o.quarter WHERE r.region_name = 'Miền Bắc' AND st.year = 2025 GROUP BY st.quarter, st.target_revenue ORDER BY st.quarter;",
        "difficulty": "hard"
    }
]

with open(os.path.join(BENCHMARK_DIR, "spider_sql_benchmark.json"), "w", encoding="utf-8") as f:
    json.dump(spider_benchmarks, f, ensure_ascii=False, indent=2)

ragas_benchmarks = [
    {
        "id": "RAGAS_EVAL_01",
        "question": "Mức chiết khấu cho đại lý cấp 1 Platinum đối với phần cứng và phần mềm là bao nhiêu?",
        "ground_truth_answer": "Đại lý cấp 1 (Platinum Partner) được chiết khấu 20% cho thiết bị phần cứng và 25% cho dịch vụ/phần mềm Cloud Analytics, với điều kiện doanh số tối thiểu 2 tỷ VNĐ/quý.",
        "reference_doc": "chinh_sach_chiet_khau_ban_hang_2025.md"
    },
    {
        "id": "RAGAS_EVAL_02",
        "question": "Chỉ tiêu doanh thu và giám đốc phụ trách khu vực Miền Bắc trong Quý 3 năm 2025 là ai?",
        "ground_truth_answer": "Chỉ tiêu doanh thu Quý 3 năm 2025 khu vực Miền Bắc là 2.200.000.000 VNĐ (lợi nhuận gộp 900.000.000 VNĐ), do Giám đốc khu vực Nguyễn Văn Hải phụ trách.",
        "reference_doc": "chien_luoc_kinh_doanh_q3_mien_bac.md"
    }
]

with open(os.path.join(BENCHMARK_DIR, "ragas_qa_benchmark.json"), "w", encoding="utf-8") as f:
    json.dump(ragas_benchmarks, f, ensure_ascii=False, indent=2)

print("--- All Database, Docs and Benchmark seedings completed successfully! ---")