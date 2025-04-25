import streamlit as st
import pandas as pd
from fp_growth import FPTree

st.set_page_config(page_title="FP-Growth Web App", layout="wide")

st.title("🛒 FP-Growth Frequent Pattern Mining")
st.write("Upload a transactional dataset (like Groceries) and extract frequent itemsets using FP-Growth.")

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
min_support = st.number_input("Minimum Support", min_value=1, value=3, step=1)

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        if 'Member_number' in df.columns and 'itemDescription' in df.columns:
            transactions = df.groupby('Member_number')['itemDescription'].apply(list).tolist()

            with st.spinner("⏳ Mining patterns... Please wait"):
                tree = FPTree(transactions, min_support)
                patterns = tree.mine_patterns()

            pattern_data = sorted([(', '.join(pattern), support) for pattern, support in patterns.items()],
                                  key=lambda x: -x[1])
            pattern_df = pd.DataFrame(pattern_data, columns=["Pattern", "Support"])

            st.success(f"✅ Found {len(pattern_df)} frequent patterns.")
            st.dataframe(pattern_df, use_container_width=True, height=600)


        else:
            st.error("CSV must have 'Member_number' and 'itemDescription' columns.")
    except Exception as e:
        st.error(f"Error: {e}")

