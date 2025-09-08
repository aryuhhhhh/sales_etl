# 🛒 Sales ETL & Analytics Project  

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)  
![ETL](https://img.shields.io/badge/ETL-Pipeline-orange)  
![SQLite](https://img.shields.io/badge/Database-SQLite-green)  
![License](https://img.shields.io/badge/License-MIT-lightgrey)  
![Dataset](https://img.shields.io/badge/Dataset-Online%20Retail%20II-yellow)  

---

## 📖 Overview

This project processes the **Online Retail II Dataset (2009–2011)** to build a clean, analysis-ready sales database.  
An **ETL (Extract, Transform, Load) pipeline** is implemented in Python to generate:

- 🧹 Cleaned and transformed data  
- 💰 Revenue calculations  
- 🔁 Deduplicated transactions  
- 📅 Monthly sales aggregations  
- ⭐ Top customers and products summary  

The pipeline outputs both **aggregate CSV files** and a **SQLite database** for further analysis and visualization.

---

## 📂 Folder Structure

```text
sales-etl/
├─ data/                     
│   ├─ online_retail_II.xlsx  
│   ├─ agg_by_country.csv     
│   ├─ agg_by_product.csv     
│   └─ agg_by_month.csv       
├─ db/                       
│   └─ sales.db
├─ etl_sales_pipeline.py     
├─ requirements.txt          
└─ README.md                 
```
---

## ⚡ Getting Started

### 1️⃣ Requirements

- Python **3.8+**
- Dependencies listed in `requirements.txt`

Install them with:

```bash
pip install -r requirements.txt
```

### 2️⃣ Prepare Dataset

Download the **Online Retail II dataset** from [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/Online+Retail+II)  
and place `online_retail_II.xlsx` inside the `data/` folder.

### 3️⃣ Run the ETL Pipeline

Execute:

```bash
python etl_sales_pipeline.py
```

This will:

- 🧹 Clean and transform raw Excel data  
- 💰 Calculate revenue and add order month  
- 📊 Generate aggregate CSVs in `data/`  
- 💾 Load cleaned data + aggregates into SQLite (`db/sales.db`)  
- 🔎 Print sample analytics (monthly revenue, top products, top customers)  

---

## 📊 Outputs

```text
CSV Aggregates:
- agg_by_country.csv
- agg_by_product.csv
- agg_by_month.csv

SQLite Database:
- sales.db (cleaned transactional data + aggregates)
```

You can connect the database to **Power BI, Tableau, or Python notebooks** for advanced visualization and analytics.

---

## 📝 Notes

- The ETL pipeline is modular and can be extended for new transformations.  
- Data source: [Online Retail II Dataset](https://archive.ics.uci.edu/ml/datasets/Online+Retail+II).  
- Useful for learning **ETL workflows, SQL analytics, and dashboard integration**.  

---

## 🚀 Future Improvements

- Add more granular aggregations (e.g., customer segmentation, RFM analysis)  
- Automate scheduled ETL runs  
- Deploy interactive dashboards with **Streamlit/Power BI/Tableau**  
