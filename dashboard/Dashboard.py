import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi halaman
st.set_page_config(page_title="E-Commerce Analysis Dashboard", layout="wide")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    state_df = pd.read_csv('customer_concentration_by_state.csv')
    category_df = pd.read_csv('top_product_categories.csv')
    return state_df, category_df

state_df, category_df = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filter Eksplorasi")

# Filter 1: Pilih Negara Bagian (State)
all_states = state_df['customer_state'].unique().tolist()
selected_states = st.sidebar.multiselect(
    "Pilih Negara Bagian (State):",
    options=all_states,
    default=all_states[:10] # Default menampilkan 10 teratas
)

# Filter 2: Jumlah Top Kategori yang ingin ditampilkan
top_n = st.sidebar.slider("Jumlah Top Kategori Produk:", min_value=1, max_value=len(category_df), value=10)

# --- LOGIKA FILTERING ---
filtered_state_df = state_df[state_df['customer_state'].isin(selected_states)]
filtered_category_df = category_df.head(top_n)

# --- MAIN DASHBOARD ---
st.title("🗺️ E-Commerce Market & Product Analysis")
st.markdown("Dashboard ini berfokus pada sebaran geografis pelanggan dan performa kategori produk berdasarkan total penjualan.")

# --- ROW 1: METRICS ---
col1, col2 = st.columns(2)

with col1:
    total_cust = filtered_state_df['unique_customers'].sum()
    st.metric("Total Pelanggan (Filter)", f"{total_cust:,}")

with col2:
    total_sales = filtered_category_df['price'].sum()
    st.metric(f"Total Penjualan (Top {top_n})", f"R$ {total_sales:,.2f}")

st.divider()

# --- ROW 2: VISUALIZATIONS ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📍 Konsentrasi Pelanggan per State")
    if not filtered_state_df.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        # Mengurutkan agar visualisasi lebih baik
        df_plot = filtered_state_df.sort_values('unique_customers', ascending=False)
        sns.barplot(data=df_plot, x='unique_customers', y='customer_state', palette="viridis", ax=ax)
        ax.set_xlabel("Jumlah Pelanggan Unik")
        ax.set_ylabel("Negara Bagian")
        st.pyplot(fig)
    else:
        st.warning("Silakan pilih setidaknya satu Negara Bagian di sidebar.")

with col_right:
    st.subheader(f"🏆 Top {top_n} Kategori Produk")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=filtered_category_df, x='price', y='product_category_name_english', palette="magma", ax=ax)
    ax.set_xlabel("Total Penjualan (R$)")
    ax.set_ylabel(None)
    st.pyplot(fig)

# --- ROW 3: DATA PREVIEW ---
with st.expander("Lihat Detail Data Mentah"):
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.write("Data Konsentrasi Pelanggan", filtered_state_df)
    with col_d2:
        st.write("Data Kategori Produk", filtered_category_df)

st.caption("Data Source: E-Commerce Public Dataset")