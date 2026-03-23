import streamlit as st
import pandas as pd

# Sửa lại tên module này cho đúng với file của bạn
# Ví dụ nếu hàm rec nằm trong file recommend.py thì đổi thành:
# from recommend import rec
from nhom7 import recommend_items
import polars as pl

df = pl.read_parquet("items.parquet")
df_trans = pl.read_parquet("transactions-2025-12.parquet")
print(df.columns)

import polars as pl

item_df = pl.read_parquet(r"items.parquet")

result = item_df.with_columns([
    # step: 1-5 -> int
    pl.when(
        pl.col("description").str.contains("(?i)cho mẹ bầu")
        & pl.col("description").str.extract(r"step\s*([1-5])", 1).is_null()
    )
    .then(0)
    .otherwise(
        pl.col("description")
        .str.extract(r"step\s*([1-5])", 1)
        .cast(pl.Int8)
    )
    .alias("step"),

    # size -> map thành số
    pl.col("description")
    .str.extract(r"\b(Newborn|S|M|L|XL|XXL)\b", 1)
    .replace({
        "Newborn": 0,
        "S": 1,
        "M": 2,
        "L": 3,
        "XL": 4,
        "XXL": 5
    })
    .cast(pl.Int8)
    .alias("size"),

    # piece -> số
    pl.col("description")
    .str.extract(r"(\d+)\s*miếng", 1)
    .cast(pl.Int16)
    .alias("piece"),
]).select([
    "item_id",
    "category_l1",
    "category_l2",
    "category_l3",
    "category",
    "step",
    "size",
    "piece",
    "description"
])

print(result['size'].unique())
print(result['step'].unique())
print(result['piece'].unique())

print(result)

st.set_page_config(
    page_title="Product Recommendation Demo",
    layout="wide"
)

st.title("Demo gợi ý sản phẩm")
st.write("Nhập `idx` của sản phẩm để lấy danh sách các sản phẩm liên quan.")

# Input sản phẩm
idx = st.text_input("Nhập idx sản phẩm", placeholder="Ví dụ: 1001")

# Số lượng kết quả muốn hiển thị
top_k = st.number_input("Số lượng sản phẩm muốn hiển thị", min_value=1, max_value=100, value=10, step=1)

if st.button("Recommend"):
    if not idx.strip():
        st.warning("Vui lòng nhập idx.")
    else:
        try:
            # Nếu idx của bạn là số nguyên thì ép kiểu ở đây
            # Nếu idx là string thì giữ nguyên như dưới
            input_idx = idx.strip()

            results = recommend_items(input_idx, result)

            if results is None:
                st.error("Hàm rec trả về None.")
            elif not isinstance(results, (list, tuple)):
                st.error("Hàm rec cần trả về list các dict, ví dụ: [{'item_id': ..., 'score': ...}, ...]")
            elif len(results) == 0:
                st.info("Không có sản phẩm gợi ý.")
            else:
                # Cắt top_k
                results = results[:top_k]

                # Đưa về DataFrame để hiển thị đẹp
                df_results = pd.DataFrame(results)

                st.subheader(f"Top {top_k} sản phẩm liên quan")
                st.dataframe(df_results, use_container_width=True)

                # Hiển thị dạng card đơn giản
                st.subheader("Hiển thị chi tiết")
                for i, item in enumerate(results, start=1):
                    with st.container():
                        st.markdown(f"### {i}. {item.get('item_id', 'N/A')}")
                        st.write(f"**Score:** {item.get('score', 'N/A')}")

                        # Nếu dict có thêm field khác thì hiện luôn
                        extra_fields = {
                            k: v for k, v in item.items()
                            if k not in ["item_id", "score"]
                        }

                        if extra_fields:
                            for k, v in extra_fields.items():
                                st.write(f"**{k}:** {v}")

                        st.divider()

        except ValueError as e:
            st.error(f"Lỗi dữ liệu: {e}")
        except Exception as e:
            st.error(f"Có lỗi xảy ra: {e}")