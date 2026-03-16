# Nhóm 3 CS116.Q21.KHTN - Báo cáo Thực nghiệm Mô hình Dự báo

## 1. Các phương pháp thử nghiệm

| Phương pháp | Mô tả | Đánh giá |
| :--- | :--- | :--- |
| **Phương pháp A** | Train mô hình Linear Regression cho từng cặp `item_id` & `location`. | **Không khả thi:** Số lượng cặp quá lớn (1,167,571) và thiếu dữ liệu huấn luyện (nhiều cặp chỉ có 1 điểm). |
| **Phương pháp B** | Lấy trung bình `quantity` theo `week` (1, 2, 3) và train trên 3 điểm này. | **Tối ưu:** Tốc độ thực thi cực nhanh và hiệu năng ổn định. |
| **Theo Item** | Train 1 mô hình riêng cho mỗi `item_id`. | **Độ chính xác cao nhất:** Phản ánh đúng chu kỳ bán ra của từng loại hàng hóa. |
| **Theo Location** | Train 1 mô hình riêng cho mỗi `location`. | **Kém ưu tiên:** Kết quả tương đương Phương pháp B nhưng thời gian xử lý lâu hơn. |

## 2. Kết quả thực nghiệm (MSE Loss)

So sánh sai số bình phương trung bình giữa các phương pháp:

* **Theo Item:** 34.0144
* **Theo Location:** 52.0989
* **Phương pháp B (Theo Week):** 52.1389
* **Phương pháp A:** 175.1751

## 3. Kết luận và Lựa chọn

Nhóm quyết định lựa chọn **Phương pháp B** làm phương án triển khai chính nhờ sự cân bằng giữa hiệu năng và tốc độ:

*  **Tốc độ xử lý:** Là phương án nhanh nhất, phù hợp với ưu tiên về thời gian của bài toán.
*  **Độ chính xác:** Cải thiện vượt trội so với Phương pháp A (MSE giảm từ 175.18 xuống 52.14).
*  **Phân tích kỹ thuật:** Mặc dù phương pháp train theo `item_id` có MSE thấp nhất (34.01), nhưng số lượng mô hình phải quản lý quá lớn (13,544 mô hình). 

> **Nhận xét:** Việc `item_id` cho kết quả tốt cho thấy các mặt hàng cùng loại có tính chu kỳ bán ra giống nhau hơn là phụ thuộc vào địa điểm bán hàng.
