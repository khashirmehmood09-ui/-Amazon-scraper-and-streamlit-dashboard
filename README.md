# -Amazon-scraper-and-streamlit-dashboard
"An automated e-commerce niche price tracker and data dashboard built with Python, BeautifulSoup, and Streamlit."
# 🛍️ Automated E-Commerce Niche Price Tracker & Dashboard

A professional web scraping and data pipeline tool designed to target specific product categories on e-commerce platforms, clean data automatically, prevent duplicates, and display insights through an interactive web interface.

## 🚀 Features
* **Targeted Web Scraping:** Extracts product titles, prices, and daily timestamps for specific search queries across multiple pages using BeautifulSoup.
* **ETL Pipeline & Storage:** Automatically appends new records to a central CSV dataset while filtering and dropping duplicate entries.
* **Interactive Dashboard:** Built with **Streamlit** to provide a live preview, total record metrics, keyword filtering, and CSV data downloads.

## 🛠️ Tech Stack
* **Python**
* **BeautifulSoup & Requests** (Web Scraping)
* **Pandas** (Data Transformation & Cleaning)
* **Streamlit** (Web Application & UI)

## 💻 How to Run Locally
1. Clone the repository:
   ```bash
2. pip install -r requirements.txt
3. streamlit run app.py
