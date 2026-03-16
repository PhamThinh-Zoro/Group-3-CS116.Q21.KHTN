# Nhóm 3 CS116.Q21.KHTN - Báo cáo Thực nghiệm Mô hình Dự báo
24520002 - Mai Quốc Anh
24520010 - Đặng Phú Duy
???????? - Phạm Ngọc Phú Thịnh

## 1. Các phương pháp thử nghiệm

| Phương pháp | Mô tả | Đánh giá |
| :--- | :--- | :--- |
| **Phương pháp A** | Huấn luyện mô hình Linear Regression riêng biệt cho từng cặp `item_id` & `location`. | **Không khả thi:** Số lượng cặp quá lớn (1,167,571) và thiếu dữ liệu trầm trọng (nhiều cặp chỉ có 1 điểm). |
| **Phương pháp B** | Huấn luyện **duy nhất 1 mô hình** trên toàn bộ dữ liệu hiện có. | **Tối ưu nhất:** Tốc độ thực thi cực nhanh, quản lý đơn giản và hiệu năng rất ổn định. |
| **Theo Item** | Huấn luyện mô hình riêng cho mỗi `item_id`. | **Độ chính xác cao nhất:** Phản ánh tốt chu kỳ bán ra của từng loại hàng hóa nhưng số lượng mô hình vẫn lớn (13,544). |
| **Theo Location** | Huấn luyện mô hình riêng cho mỗi `location`. | **Kém ưu tiên:** Kết quả tương đương Phương pháp B nhưng tốn thời gian huấn luyện nhiều mô hình hơn. |

## 2. Kết quả thực nghiệm (MSE Loss)

So sánh sai số bình phương trung bình giữa các phương pháp:

* **Theo Item:** 34.0144
* **Theo Location:** 52.0989
* **Phương pháp B (Global Model):** 52.1375
* **Phương pháp A:** 175.1751

## 3. Kết luận và Lựa chọn

Nhóm quyết định lựa chọn **Phương pháp B** làm phương án triển khai chính nhờ sự cân bằng lý tưởng giữa hiệu năng và tốc độ:

1.  **Tốc độ xử lý:** Là phương án nhanh nhất vì chỉ cần huấn luyện duy nhất một mô hình cho toàn bộ hệ thống.
2.  **Độ chính xác:** Cải thiện vượt trội so với Phương pháp A (MSE giảm từ 175.18 xuống 52.14).
3.  **Khả năng mở rộng:** Việc quản lý 1 mô hình (Phương pháp B) đơn giản hơn hẳn so với việc duy trì 13,544 mô hình (Theo Item) dù MSE có chênh lệch đôi chút.

> **Nhận xét:** Kết quả cho thấy các mặt hàng cùng loại (`item_id`) có tính chu kỳ bán ra tương đồng, trong khi yếu tố địa điểm (`location`) không tạo ra sự khác biệt quá lớn về xu hướng.
