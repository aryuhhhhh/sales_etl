import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine, text

# Paths
DATA_PATH = Path("data/online_retail_II.xlsx")
DB_PATH = Path("db/sales.db")
TABLE_NAME = "sales"

def load_raw():
    """Load all sheets from Excel and merge"""
    dfs = pd.read_excel(DATA_PATH, sheet_name=None)
    df = pd.concat(dfs.values(), ignore_index=True)
    return df

def clean_transform(df: pd.DataFrame) -> pd.DataFrame:
    """Clean dataset and add calculated fields"""
    # Standardize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    
    # Drop rows without invoice or customer
    df = df.dropna(subset=["invoice", "customer_id"])
    
    # Fix data types
    df["invoicedate"] = pd.to_datetime(df["invoicedate"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0).astype(int)
    df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0.0)
    
    # Revenue and month
    df["revenue"] = df["quantity"] * df["price"]
    df["order_month"] = df["invoicedate"].values.astype("datetime64[M]")
    
    # Remove duplicates
    df = df.drop_duplicates(subset=["invoice", "stockcode"])
    
    # Clean text columns
    for col in ["description", "country"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()
    
    return df

def write_aggregates(df: pd.DataFrame):
    """Save aggregate CSVs"""
    Path("data").mkdir(exist_ok=True, parents=True)
    
    df.groupby("country")["revenue"].sum().sort_values(ascending=False)\
        .reset_index().to_csv("data/agg_by_country.csv", index=False)
    
    df.groupby("description")["revenue"].sum().sort_values(ascending=False)\
        .reset_index().to_csv("data/agg_by_product.csv", index=False)
    
    df.groupby("order_month")["revenue"].sum().sort_index()\
        .reset_index().to_csv("data/agg_by_month.csv", index=False)

def init_db():
    """Create SQLite DB and table if not exists"""
    engine = create_engine(f"sqlite:///{DB_PATH}")
    with engine.begin() as conn:
        conn.exec_driver_sql(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice TEXT,
                stockcode TEXT,
                description TEXT,
                quantity INTEGER,
                invoicedate TEXT,
                price REAL,
                customer_id TEXT,
                country TEXT,
                revenue REAL,
                order_month TEXT
            );
        """)
    return engine

def load_to_sqlite(df: pd.DataFrame):
    """Load DataFrame into SQLite"""
    engine = init_db()
    df.to_sql(TABLE_NAME, con=engine, if_exists="replace", index=False)
    print(f"✅ Loaded {len(df)} rows into {DB_PATH}")

def run_queries():
    """Run test SQL queries"""
    engine = create_engine(f"sqlite:///{DB_PATH}")
    queries = {
        "Revenue per Country": """
            SELECT country, ROUND(SUM(revenue),2) AS total_revenue
            FROM sales
            GROUP BY country
            ORDER BY total_revenue DESC
            LIMIT 10;
        """,
        "Top 5 Products": """
            SELECT description, ROUND(SUM(revenue),2) AS total_revenue, SUM(quantity) AS units_sold
            FROM sales
            GROUP BY description
            ORDER BY total_revenue DESC
            LIMIT 5;
        """,
        "Monthly Revenue Trend": """
            SELECT strftime('%Y-%m', invoicedate) AS month, ROUND(SUM(revenue),2) AS total_revenue
            FROM sales
            GROUP BY month
            ORDER BY month;
        """,
        "Top Customer by Lifetime Value": """
            SELECT customer_id, ROUND(SUM(revenue),2) AS lifetime_value
            FROM sales
            GROUP BY customer_id
            ORDER BY lifetime_value DESC
            LIMIT 1;
        """
    }
    with engine.begin() as conn:
        for name, q in queries.items():
            print(f"\n--- {name} ---")
            for row in conn.execute(text(q)):
                print(dict(row._mapping))

def main():
    print("📥 Loading raw data...")
    raw = load_raw()
    print(f"Raw shape: {raw.shape}")

    print("🧹 Cleaning and transforming...")
    clean = clean_transform(raw)
    print(f"Clean shape: {clean.shape}")

    print("📊 Writing aggregate CSVs...")
    write_aggregates(clean)

    print("💾 Loading into SQLite...")
    load_to_sqlite(clean)

    print("🔎 Running test SQL queries...")
    run_queries()

    print("\n✅ ETL pipeline finished. DB created at:", DB_PATH.resolve())

if __name__ == "__main__":
    main()
