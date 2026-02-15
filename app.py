import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Reliance Price Plotter", layout="wide")

st.title("📈 Reliance Price Timechart")
st.write("Visualizing the `ARIMAX_Data.csv` trend.")

# 1. File Upload (Optional - helps if you want to swap data later)
uploaded_file = st.file_uploader("Upload your ARIMAX_Data.csv", type="csv")

# Use uploaded file if available, otherwise try to load from the repo directly
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    try:
        # This looks for the file you uploaded to GitHub
        df = pd.read_csv('ARIMAX_Data.csv')
    except FileNotFoundError:
        st.info("Waiting for CSV file upload...")
        df = None

if df is not None:
    # 2. Basic Cleaning
    # Cleaning column names in case there are hidden spaces
    df.columns = df.columns.str.strip()
    
    st.write("### Data Preview", df.head())

    # 3. Dynamic Column Selection
    # This detects if your columns are named 'Date' and 'Price'
    date_col = 'Date'
    # Adjust 'Price' to match your specific CSV column (e.g., 'Reliance Close Price')
    price_col = [col for col in df.columns if 'Price' in col or 'Close' in col][0]

    if date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col])
        
        # 4. Interactive Plotly Chart
        fig = px.line(df, x=date_col, y=price_col, 
                     title=f'Trend of {price_col} over Time',
                     template="plotly_dark") # Making it look professional
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error(f"Could not find a '{date_col}' column in the file.")
