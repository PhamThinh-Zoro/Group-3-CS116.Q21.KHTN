import streamlit as st
import pandas as pd
import polars as pl
from nhom7 import recommend_items

# -------------------------
# LOAD DATA
# -------------------------
@st.cache_data
def load_data():
    df = pl.read_parquet("items.parquet")
    df_trans = pl.read_parquet("transactions-2025-12.parquet")

    result = df.with_columns([
        # step
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

        # size
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

        # piece
        pl.col("description")
        .str.extract(r"(\d+)\s*miếng", 1)
        .cast(pl.Int16)
        .alias("piece"),
    ])

    return result

df = load_data()

# -------------------------
# CONFIG UI
# -------------------------
st.set_page_config(
    page_title="🛒 Product Recommender",
    layout="wide"
)

st.markdown(
    """
    <h1 style='text-align: center;'>🛍️ Hệ thống gợi ý sản phẩm</h1>
    <p style='text-align: center; color: gray;'>Nhập sản phẩm hoặc category để nhận gợi ý</p>
    """,
    unsafe_allow_html=True
)

# -------------------------
# INPUT
# -------------------------
col1, col2 = st.columns([2, 1])

with col1:
    idx = st.text_input(
        "🔍 Nhập item_id",
        placeholder="Ví dụ: 1001"
    )

with col2:
    top_k = st.number_input(
        "📊 Top K",
        min_value=1,
        max_value=50,
        value=10
    )

# -------------------------
# SHOW INPUT ITEM INFO
# -------------------------
def show_input_item(item_id):
    item = df.filter(pl.col("item_id") == item_id)

    if item.height == 0:
        st.warning("❌ Không tìm thấy sản phẩm")
        return None

    item = item.to_pandas().iloc[0]

    st.success("✅ Sản phẩm bạn chọn:")

    colA, colB = st.columns([1, 2])

    with colA:
        st.metric("🆔 Item ID", item["item_id"])

    with colB:
        st.write(f"**Category:** {item['category']}")
        st.write(f"**Step:** {item['step']}")
        st.write(f"**Size:** {item['size']}")
        st.write(f"**Piece:** {item['piece']}")

    st.info(f"📝 {item['description']}")

    return item

# -------------------------
# BUTTON
# -------------------------
if st.button("🚀 Recommend", use_container_width=True):

    if not idx.strip():
        st.warning("⚠️ Vui lòng nhập item_id")
    else:
        input_idx = idx.strip()

        # show item
        item_info = show_input_item(input_idx)

        if item_info is not None:
            with st.spinner("⏳ Đang tính toán gợi ý..."):
                try:
                    results = recommend_items(input_idx, df)

                    if not results:
                        st.info("Không có gợi ý.")
                    else:
                        results = results[:top_k]

                        st.markdown("---")
                        st.subheader(f"🎯 Top {top_k} sản phẩm gợi ý")

                        # TABLE
                        df_results = pd.DataFrame(results)
                        st.dataframe(df_results, use_container_width=True)

                        # CARD VIEW
                        st.markdown("### 📦 Chi tiết")

                        cols = st.columns(2)

                        for i, item in enumerate(results):
                            col = cols[i % 2]

                            with col:
                                with st.container():
                                    st.markdown(
                                        f"""
                                        <div style="
                                            padding:15px;
                                            border-radius:12px;
                                            border:1px solid #ddd;
                                            margin-bottom:10px;
                                        ">
                                            <h4>#{i+1} - {item.get('item_id')}</h4>
                                            <p>⭐ Score: {item.get('score')}</p>
                                        </div>
                                        """,
                                        unsafe_allow_html=True
                                    )

                except Exception as e:
                    st.error(f"❌ Lỗi: {e}")