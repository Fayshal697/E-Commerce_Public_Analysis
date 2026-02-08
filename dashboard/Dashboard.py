import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(
    page_title="E-Commerce Analysis Dashboard",
    layout="wide"
)

st.title("📊 E-Commerce Public Dataset Analysis")
st.markdown(
    """
    Dashboard ini menjawab dua pertanyaan bisnis utama:
    1. **Kategori produk dengan revenue terbesar (2017–2018)**
    2. **State dengan konsentrasi pelanggan terbanyak (akhir 2018)**
    """
)

# =============================
# LOAD DATA
# =============================
@st.cache_data
def load_data():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    category_path = os.path.join(BASE_DIR, "category_revenue_with_timestamps_with_state.csv")
    state_path = os.path.join(BASE_DIR, "customer_concentration_by_state.csv")

    category_df = pd.read_csv(category_path)
    state_df = pd.read_csv(state_path)

    category_df["order_purchase_timestamp"] = pd.to_datetime(
        category_df["order_purchase_timestamp"]
    )

    return category_df, state_df


category_df, state_df = load_data()

# =============================
# SIDEBAR FILTER
# =============================
st.sidebar.header("🔎 Filter Data")

# Date range filter
min_date = category_df["order_purchase_timestamp"].min().date()
max_date = category_df["order_purchase_timestamp"].max().date()

date_range = st.sidebar.date_input(
    "Rentang Tanggal",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Top-N filter
top_n = st.sidebar.slider(
    "Top Kategori Produk",
    min_value=1,
    max_value=10,
    value=5
)

# =============================
# FILTERING
# =============================
filtered_df = category_df[
    (category_df["order_purchase_timestamp"].dt.date >= date_range[0]) &
    (category_df["order_purchase_timestamp"].dt.date <= date_range[1])
]

top_category_df = (
    filtered_df
    .groupby("product_category_name_english", as_index=False)["price"]
    .sum()
    .sort_values(by="price", ascending=False)
    .head(top_n)
)

# =============================
# VISUALIZATION 1
# =============================
st.subheader("🏆 Top Kategori Produk Berdasarkan Revenue")

fig1, ax1 = plt.subplots(figsize=(10, 5))
ax1.barh(
    top_category_df["product_category_name_english"],
    top_category_df["price"]
)
ax1.set_xlabel("Total Revenue")
ax1.set_ylabel("Kategori Produk")
ax1.invert_yaxis()

st.pyplot(fig1)

st.markdown(
    f"""
    **Insight:**  
    Pada periode yang dipilih, kategori **{top_category_df.iloc[0]['product_category_name_english']}**
    menjadi penyumbang revenue terbesar.
    """
)

# =============================
# VISUALIZATION 2
# =============================
st.subheader("🌎 Konsentrasi Pelanggan Berdasarkan State (Akhir 2018)")

fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.bar(
    state_df["customer_state"],
    state_df["unique_customers"]
)
ax2.set_xlabel("State")
ax2.set_ylabel("Jumlah Pelanggan")

st.pyplot(fig2)

top_state = state_df.sort_values(
    by="unique_customers", ascending=False
).iloc[0]["customer_state"]

st.markdown(
    f"""
    **Insight:**  
    State **{top_state}** memiliki konsentrasi pelanggan tertinggi
    pada akhir tahun 2018.
    """
)

# =============================
# FOOTER
# =============================
st.markdown("---")
st.caption("© 2025 | E-Commerce Public Dataset Analysis | Streamlit Dashboard")