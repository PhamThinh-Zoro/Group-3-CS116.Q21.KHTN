import streamlit as st
import numpy as np
import pickle

# --- 1. Cấu hình trang ---
st.set_page_config(page_title="Demo Dự báo Giao dịch", page_icon="📈")

# --- 2. Tải mô hình ---
# Sử dụng st.cache_resource để không phải load lại model mỗi lần tương tác UI
#@st.cache_resource
with open('modelB.pkl', 'rb') as f:
    model=pickle.load(f)


# --- 3. Giao diện người dùng (UI) ---
st.title("📈 Demo Dự báo Lượng Bán (Linear Regression)")
st.markdown("""
Ứng dụng này sử dụng mô hình Hồi quy tuyến tính (Simple Linear Regression) đã được huấn luyện để dự báo tổng số lượng (`total_quantity`) dựa trên thứ tự tuần (`week`).
""")

st.divider()

# --- 4. Nhập dữ liệu (Input) ---
st.subheader("Nhập thông tin dự đoán")

# Mặc dù model hiện tại không dùng item_id và location, ta vẫn để form cho giống thực tế
col1, col2, col3 = st.columns(3)

with col1:
    item_id = st.text_input("Mã sản phẩm (Item ID)", value="0006040000303")
with col2:
    location = st.text_input("Mã cửa hàng (Location)", value="42")
with col3:
    # Model chỉ thực sự nhận week làm features
    week = st.number_input("Tuần dự đoán (Week)", min_value=1, max_value=10, value=4)

# --- 5. Thực hiện dự đoán (Predict) ---
if st.button("Dự đoán", type="primary"):
    if model is not None:
        # Chuẩn bị input X (Model yêu cầu mảng 2D)
        X_input = np.array([[week]])
        
        # Chạy dự đoán
        pred_quantity = model.predict(X_input)[0]
        
        # Hiển thị kết quả
        st.divider()
        st.subheader("💡 Kết quả dự báo")
        st.success(f"**Tổng số lượng dự kiến** bán ra của sản phẩm **{item_id}** tại cửa hàng **{location}** trong **Tuần {week}** là: **{pred_quantity:.2f}**")
        
        # Giải thích nội bộ cho user hiểu cơ chế
        st.info(f"**Chi tiết kỹ thuật:** Mô hình đang áp dụng phương trình $y = ax + b$. Với hệ số $a$ (coef_) = {model.coef_[0]:.4f} và $b$ (intercept_) = {model.intercept_:.4f}.")