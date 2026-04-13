# Tài liệu Hệ thống: Category Network Visualizer

Ứng dụng **Category Network Visualizer** là một công cụ phân tích dữ liệu mua sắm (Market Basket Analysis) được xây dựng trên nền tảng **Streamlit**. Mục tiêu chính là trực quan hóa mối quan hệ giữa các danh mục sản phẩm dựa trên tần suất chúng xuất hiện cùng nhau trong cùng một đơn hàng.

---

## 1. Công nghệ Sử dụng
* **Streamlit:** Khung giao diện web để tạo bảng điều khiển tương tác.
* **Polars:** Thư viện xử lý dữ liệu hiệu năng cao giúp xử lý các tập tin giao dịch lớn.
* **NetworkX:** Thư viện phân tích mạng lưới để xây dựng cấu trúc đồ thị.
* **Pyvis:** Thư viện hỗ trợ tạo đồ thị tương tác dưới dạng HTML.

---

## 2. Quy trình Xử lý Dữ liệu

### Bước 1: Nạp và Lọc dữ liệu
Hệ thống nạp hai tệp tin chính là `transactions-202411-to-202412.parquet` và `items.parquet`. 
* Sử dụng `@st.cache_resource` để tối ưu bộ nhớ.
* Lọc lấy top các sản phẩm phổ biến nhất để đảm bảo hiệu suất tính toán.

### Bước 2: Xác định Giỏ hàng (Basket)
Dữ liệu được nhóm theo `customer_id` và `updated_date`. Hệ thống ánh xạ từng sản phẩm về danh mục:
* **Level 1 (L1):** Danh mục rộng.
* **Combined (L1 + L2):** Kết hợp danh mục cấp 1 và cấp 2 để phân tích chi tiết.

### Bước 3: Tính toán Trọng số Liên kết
Mối quan hệ giữa hai danh mục $i$ và $j$ được xác định qua công thức:

$$Weight = \ln(\text{co\_count}) \times \left( \frac{\text{co\_count}}{\text{total\_i}} + \frac{\text{co\_count}}{\text{total\_j}} \right)$$

> **Chú thích:**
> * **co_count:** Số lần danh mục $i$ và $j$ xuất hiện cùng nhau.
> * **total_i / total_j:** Tổng số lần danh mục $i$ (hoặc $j$) xuất hiện trong toàn bộ dữ liệu.

---

## 3. Các Tính năng Chính

###  Cấu hình Hệ thống
* **Visualization Type:** Chuyển đổi giữa cấp độ danh mục L1 hoặc L1+L2.
* **Edge Weight Threshold:** Thanh trượt điều chỉnh ngưỡng hiển thị. Các liên kết có trọng số thấp hơn ngưỡng sẽ bị ẩn để giảm nhiễu đồ thị.

###  Trực quan hóa Mạng lưới
* **Nút (Node):** Đại diện cho một danh mục sản phẩm.
* **Cạnh (Edge):** Đại diện cho mối quan hệ mua kèm. Độ dày tỉ lệ với trọng số liên kết.
* **Tính tương tác:** Cho phép kéo thả, phóng to và xem thông tin chi tiết khi di chuột qua.

###  Bảng Điểm số & Xuất dữ liệu
* Cung cấp bảng thống kê chi tiết các cặp danh mục có liên kết mạnh nhất.
* Hỗ trợ nút **Download CSV** để tải dữ liệu về máy.

## 4. Thống kê Mạng lưới (Network Statistics)
Hệ thống tự động tính toán các chỉ số kỹ thuật:
1.  **Total Nodes:** Tổng số danh mục trong mạng lưới.
2.  **Total Edges:** Tổng số liên kết thỏa mãn điều kiện ngưỡng.
3.  **Avg Degree:** Số lượng kết nối trung bình trên mỗi danh mục.
4.  **Network Density:** Mật độ kết nối của toàn bộ hệ thống.

---
