import streamlit as st
import polars as pl
from itertools import combinations
from collections import Counter
import networkx as nx
from pyvis.network import Network
import pandas as pd
import os

# Set page configuration
st.set_page_config(page_title="Category Network Visualizer", layout="wide")

st.title("🌐 Category Network Visualizer")

# ========== Load data ==========
@st.cache_resource
def load_data():
    transactions = pl.read_parquet(r"C:\coding_space\study\CS116\transactions-202411-to-202412.parquet")
    items = pl.read_parquet(r"C:\coding_space\study\CS116\items.parquet")
    return transactions, items

# ========== Build graph function ==========
def build_graph(transactions, items, category_type="l1", threshold=2.0):
    """Build graph based on category type (l1 or l1_l2) and threshold"""
    
    # Filter top items
    TOP_N = 10000000
    top_items = (
        transactions
        .group_by("item_id")
        .len()
        .sort("len", descending=True)
        .head(TOP_N)
        .get_column("item_id")
        .to_list()
    )
    
    transactions = transactions.filter(pl.col("item_id").is_in(top_items))
    items = items.filter(pl.col("item_id").is_in(top_items))
    
    # Get categories per basket
    if category_type == "l1":
        basket_with_cat = (
            transactions
            .join(items.select(["item_id", "category_l1"]), on="item_id", how="left")
            .group_by(["customer_id", "updated_date"])
            .agg(pl.col("category_l1").unique())
        )
        category_col = "category_l1"
    else:  # l1_l2
        basket_with_cat = (
            transactions
            .join(items.select(["item_id", "category_l1", "category_l2"]), on="item_id", how="left")
            .with_columns(
                combined_cat = pl.col("category_l1") + "_" + pl.col("category_l2")
            )
            .group_by(["customer_id", "updated_date"])
            .agg(pl.col("combined_cat").unique())
        )
        category_col = "combined_cat"
    
    # Calculate co-occurrence
    pair_counter = Counter()
    
    for row in basket_with_cat.iter_rows():
        cat_list = row[2]
        if len(cat_list) > 1:
            for pair in combinations(sorted(cat_list), 2):
                pair_counter[pair] += 1
    
    edges_df = pl.DataFrame({
        "cat_i": [k[0] for k in pair_counter.keys()],
        "cat_j": [k[1] for k in pair_counter.keys()],
        "co_count": list(pair_counter.values())
    })
    
    # Compute category totals
    category_counts_df = basket_with_cat.explode(category_col).group_by(category_col).len()
    
    # Filter top categories
    TOP_CATEGORIES = 1000
    
    top_categories = (
        category_counts_df
        .filter(pl.col(category_col).is_not_null())
        .sort("len", descending=True)
        .head(TOP_CATEGORIES)
        .get_column(category_col)
        .to_list()
    )
    
    # Filter edges
    edges_df = edges_df.filter(
        (pl.col("cat_i").is_in(top_categories)) & (pl.col("cat_j").is_in(top_categories)) &
        (pl.col("cat_i").is_not_null()) & (pl.col("cat_j").is_not_null())
    )
    
    # Update category_counts
    category_counts_df = category_counts_df.filter(
        (pl.col(category_col).is_in(top_categories)) & (pl.col(category_col).is_not_null())
    )
    
    # Join totals
    edges_df = (
        edges_df
        .join(category_counts_df, left_on="cat_i", right_on=category_col, how="left", coalesce=False)
        .rename({"len": "total_i"})
        .drop(category_col)
        .join(category_counts_df, left_on="cat_j", right_on=category_col, how="left", coalesce=False)
        .rename({"len": "total_j"})
        .drop(category_col)
    )
    
    # Compute weight
    edges_df = edges_df.with_columns(
        weight = pl.col("co_count").log() * (pl.col("co_count") / pl.col("total_i") + pl.col("co_count") / pl.col("total_j"))
    )
    
    # Build NetworkX graph
    G = nx.Graph()
    
    # Add nodes
    for cat in top_categories:
        G.add_node(cat)
    
    # Add edges with threshold
    EDGE_THRESHOLD = threshold
    
    for row in edges_df.iter_rows():
        cat_i, cat_j, co_count, total_i, total_j, weight = row
        if weight >= EDGE_THRESHOLD:
            G.add_edge(cat_i, cat_j, weight=weight)
    
    # Create visualization
    net = Network(height="800px", width="100%", notebook=False)
    
    # Set physics options
    net.set_options("""
{
  "physics": {
    "enabled": true,
    "stabilization": {
      "enabled": true,
      "iterations": 100
    },
    "repulsion": {
      "centralGravity": 0.05,
      "springLength": 500,
      "springConstant": 0.01,
      "nodeDistance": 400,
      "damping": 0.09
    },
    "maxVelocity": 50,
    "minVelocity": 0.1
  }
}
""")
    
    # Add nodes with colors
    color_map = {cat: f"hsl({i*40 % 360},70%,60%)" for i, cat in enumerate(top_categories)}
    
    for node in G.nodes():
        net.add_node(
            node,
            label=str(node),
            color=color_map.get(node, "#cccccc"),
            title=f"Category: {node}"
        )
    
    # Add edges
    for u, v, data in G.edges(data=True):
        net.add_edge(u, v, value=data["weight"])
    
    return net, G, edges_df, category_counts_df

# ========== Calculate edge scores ==========
def calculate_edge_scores(edges_df, threshold):
    """Calculate edge scores"""
    
    edge_scores = []
    
    for row in edges_df.iter_rows():
        cat_i, cat_j, co_count, total_i, total_j, weight = row
        if weight >= threshold:
            edge_scores.append({
                "From_Category": cat_i,
                "To_Category": cat_j,
                "Co_Occurrence": int(co_count),
                "Total_i": int(total_i),
                "Total_j": int(total_j),
                "Weight": round(weight, 4)
            })
    
    return pd.DataFrame(edge_scores).sort_values("Weight", ascending=False)

# ========== Main app ==========
try:
    transactions, items = load_data()
    
    # Sidebar for selection
    st.sidebar.title("⚙️ Settings")
    
    category_type = st.sidebar.radio(
        "Select visualization type:",
        ["Category L1", "Category L1 + L2"],
        help="Choose between category level 1 or combined level 1 and 2"
    )
    
    category_mode = "l1" if category_type == "Category L1" else "l1_l2"
    
    # Threshold slider
    default_threshold = 2.0 if category_mode == "l1" else 1.5
    threshold = st.sidebar.slider(
        "Edge Weight Threshold",
        min_value=0.0,
        max_value=10.0,
        value=default_threshold,
        step=0.1,
        help="Minimum weight for edges to be displayed. Higher values show fewer, stronger connections."
    )
    
    st.sidebar.write(f"Current threshold: **{threshold}**")
    
    # Build graph with progress
    with st.spinner(f"Building {category_type} network graph..."):
        net, G, edges_df, category_counts_df = build_graph(transactions, items, category_mode, threshold)
    
    st.success(f"✅ Graph built successfully! ({len(G.nodes())} nodes, {len(G.edges())} edges) with threshold {threshold}")
    
    # Display graph
    st.subheader(f"📊 {category_type} Network Visualization")
    
    # Save and display HTML
    html_file = f"graph_{category_mode}.html"
    net.write_html(html_file)
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html_string = f.read()
    
    st.components.v1.html(html_string, height=850)
    
    # Display edge scores
    st.subheader("🔗 Edge Scores")
    
    edge_scores_df = calculate_edge_scores(edges_df, threshold)
    
    st.dataframe(edge_scores_df, use_container_width=True, hide_index=True)
    
    # Download edge scores
    csv_edge = edge_scores_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Edge Scores (CSV)",
        data=csv_edge,
        file_name=f"edge_scores_{category_mode}.csv",
        mime="text/csv"
    )
    
    # Statistics
    st.subheader("📊 Network Statistics")
    
    stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
    
    with stats_col1:
        st.metric("Total Nodes", len(G.nodes()))
    
    with stats_col2:
        st.metric("Total Edges", len(G.edges()))
    
    with stats_col3:
        avg_degree = 2 * len(G.edges()) / len(G.nodes()) if len(G.nodes()) > 0 else 0
        st.metric("Avg Degree", f"{avg_degree:.2f}")
    
    with stats_col4:
        density = nx.density(G)
        st.metric("Network Density", f"{density:.4f}")

except Exception as e:
    st.error(f"❌ Error: {str(e)}")
    st.write("Please make sure the data files are in the correct location.")
