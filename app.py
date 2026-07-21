import datetime
import os
import time
from bs4 import BeautifulSoup
import pandas as pd
import requests
import streamlit as st

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="E-Commerce Niche Price Scraper",
    page_icon="🛍️",
    layout="wide",
)

file_path = "AmazonWebScraperDataset.csv"

# --- App UI Title & Description ---
st.title("🛍️ Automated E-Commerce Competitor Price Tracker")
st.markdown(
    "This web application extracts targeted product listings from Amazon,"
    " prevents duplicate records, appends historical data, and presents clean"
    " insights."
)

# --- Sidebar Inputs for User Interactivity ---
st.sidebar.header("Scraper Configuration")
search_query = st.sidebar.text_input(
    "Search Keyword", value="gaming laptop"
)
max_pages = st.sidebar.slider("Select Number of Pages to Scrape", 1, 5, 2)

formatted_query = search_query.replace(" ", "+")

# --- Action Button to Run Scraper on Cloud ---
if st.sidebar.button("🚀 Run Scraper Now"):
  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
          " like Gecko) Chrome/122.0.0.0 Safari/537.36"
      ),
      "Accept-Language": "en-US,en;q=0.9",
      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
      "Referer": "https://www.amazon.com/",
  }

  today = datetime.date.today()
  file_exists = os.path.isfile(file_path)
  total_new_rows = 0

  progress_bar = st.progress(0)
  status_text = st.empty()

  import csv

  with open(file_path, "a+", newline="", encoding="UTF8") as f:
    writer = csv.writer(f)
    if not file_exists:
      writer.writerow(["Title", "Price", "Date"])

    for i, page_num in enumerate(range(1, max_pages + 1)):
      status_text.text(
          f"Scraping Page {page_num} of {max_pages} for '{search_query}'..."
      )
      progress_bar.progress((i + 1) / max_pages)

      URL = f"https://www.amazon.com/s?k={formatted_query}&page={page_num}"

      try:
        response = requests.get(URL, headers=headers)
        response.raise_for_status()
      except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
        continue

      soup = BeautifulSoup(response.content, "html.parser")
      
      # Flexible product container search
      products = soup.find_all("div", {"data-component-type": "s-search-result"})
      if not products:
        # Fallback search if container attribute differs
        products = soup.select("div.s-result-item[data-asin]")

      for product in products:
        try:
          # Flexible title extraction across categories
          title_elem = (
              product.find("h2", class_="a-size-base-plus") or
              product.find("span", class_="a-text-normal") or
              product.find("h2", class_="a-size-medium")
          )
          title = title_elem.get_text().strip() if title_elem else "N/A"

          # Flexible price extraction
          price_elem = product.find("span", class_="a-price")
          if price_elem:
            whole_price = price_elem.find("span", class_="a-price-whole")
            price = whole_price.get_text().strip() if whole_price else "N/A"
          else:
            price = "N/A"

          if title != "N/A" and price != "N/A" and len(title) > 5:
            writer.writerow([title, price, today])
            total_new_rows += 1
        except Exception:
          continue
      time.sleep(2)

  status_text.text("Scraping completed!")
  progress_bar.empty()
  st.success(f"Successfully scraped and added {total_new_rows} new records!")

  # Clean duplicates
  if os.path.isfile(file_path):
    df_temp = pd.read_csv(file_path)
    if not df_temp.empty:
      df_temp.drop_duplicates(subset=["Title", "Price"], keep="first", inplace=True)
      df_temp.to_csv(file_path, index=False)

# --- Display Data & Analytics Section ---
st.divider()
st.subheader("📊 Dataset Overview & Preview")

if os.path.isfile(file_path):
  df_display = pd.read_csv(file_path)
  if not df_display.empty:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Records in DB", len(df_display))
    col2.metric("Unique Products", df_display["Title"].nunique())
    col3.metric("Latest Update Date", str(datetime.date.today()))

    search_term = st.text_input("Filter results by title keyword:")
    if search_term:
      df_display = df_display[
          df_display["Title"].str.contains(search_term, case=False, na=False)
      ]

    st.dataframe(df_display, use_container_width=True)

    csv_data = df_display.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Cleaned Dataset as CSV",
        data=csv_data,
        file_name="Amazon_Scraped_Dataset.csv",
        mime="text/csv",
    )
  else:
    st.info(
        "Dataset is empty. Use the sidebar button 'Run Scraper Now' to fetch"
        " data!"
    )
else:
  st.warning(
      "No dataset found. Click 'Run Scraper Now' in the sidebar to generate"
      " data."
  )