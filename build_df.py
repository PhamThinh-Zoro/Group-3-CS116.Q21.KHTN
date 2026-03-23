import polars as pl

item_df = pl.read_parquet(r"items (1).parquet")

result = item_df.with_columns([
    # step: 1-5 -> int
    pl.col("description")
    .str.extract(r"step\s*([1-5])", 1)
    .cast(pl.Int8)
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
    "step",
    "size",
    "piece"
])

print(result['size'].unique())
print(result['step'].unique())
print(result['piece'].unique())

result.write_parquet("output.parquet")