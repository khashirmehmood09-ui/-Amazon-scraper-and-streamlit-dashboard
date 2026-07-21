import streamlit as st
import pandas as pd
import datetime
import os

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="E-Commerce Niche Price Scraper",
    page_icon="🛍️",
    layout="wide"
)

file_path = r"C:\Users\lg\OneDrive\Belgeler\Desktop\amazon\AmazonWebScraperDataset.csv"

# --- App UI Title & Description ---
st.title("🛍️ Automated E-Commerce Competitor Price Tracker")
st.markdown("This dashboard displays your targeted Amazon niche scraped dataset, complete with duplicate handling and historical append logs.")

# --- Display Data & Analytics Section ---
if os.path.isfile(file_path):
    df_display = pd.read_csv(file_path)
    if not df_display.empty:
        # Metrics Row
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Records in DB", len(df_display))
        col2.metric("Unique Products", df_display['Title'].nunique())
        col3.metric("Latest Update Date", str(datetime.date.today()))
        
        # Search filter inside table view
        search_term = st.text_input("Filter results by title keyword:")
        if search_term:
            df_display = df_display[df_display['Title'].str.contains(search_term, case=False, na=False)]
            
        # Display interactive dataframe table
        st.dataframe(df_display, use_container_width=True)
        
        # Download Button for CSV
        csv_data = df_display.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Cleaned Dataset as CSV",
            data=csv_data,
            file_name="Amazon_Scraped_Dataset.csv",
            mime="text/csv"
        )
    else:
        st.info("The dataset file is currently empty. Run your scraping cell first!")
else:
    st.warning("No dataset found at the specified path. Please run your scraper code first to generate the CSV file.")
