# 📊 Project Phân Tích Thống Kê & Visualization

## 📌 Giới thiệu
Project này dùng để:
- Kiểm định giả thuyết thống kê
- Vẽ biểu đồ (plot)
- Thống kê dữ liệu theo nhiều cấp độ

Gồm 2 file chính:
- `Hypothesis.pdf`: Báo cáo kiểm định
- `Tools.ipynb`: Code dùng để plot và thống kê

---

## 📂 Cấu trúc

.
├── Hypothesis.pdf
├── Tools.ipynb
└── README.md


---

## ⚙️ Chức năng

### 1. 📈 Plot
Có 2 cách vẽ:

- **Theo danh sách**
  - Truyền vào các item/category muốn vẽ

- **Random N**
  - Chọn ngẫu nhiên N item để vẽ

Hỗ trợ các level:
- `cat_l1`
- `cat_l2`
- `cat_l3`
- `cat`
- `item_id` (SKU)

Ngoài ra có hàm riêng để plot toàn bộ dataset

---

### 2. 📊 Thống kê
In ra thống kê theo các level:
- Toàn bộ
- `cat_l1`
- `cat_l2`
- `cat_l3`
- `cat`
- `item_id` (SKU)

Kết quả là các bảng thống kê để phân tích dữ liệu

---

## 🚀 Cách dùng

### 1. Mở notebook

jupyter notebook Tools.ipynb


### 2. Plot
- Chọn mode (list hoặc random)
- Chọn level
- Gọi hàm trong notebook

### 3. Thống kê
- Chạy các cell thống kê
- Xem kết quả bảng

---

## 📝 Ghi chú
- Dữ liệu đã được chia theo số ngày trong tuần
- Do các tuần có độ dài khác nhau nên đã được normalize trước