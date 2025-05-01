

import streamlit as st
import pymysql
import pandas as pd

# --- DB CONNECTION ---
def get_connection():
    return pymysql.connect(
        host="localhost",
        port= 3306,
        user="root",
        password="1234",
        database="retail_orders1"  
    )

# --- QUERY FUNCTION ---
def run_query(query):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# --- STREAMLIT PAGE SETUP ---
st.set_page_config(page_title="Retail Order Analysis", layout="wide")

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["📊 Project Introduction", "📋 SQL Query Results", "👩‍💻 Creator Info"])

# --- QUERIES 
queries = {
    "1. Top 10 Highest Revenue Generating Products": """
        SELECT product_id, SUM(sale_price * quantity) AS total_revenue
        FROM df2
        GROUP BY product_id
        ORDER BY total_revenue DESC
        LIMIT 10;
    """,

    "2. Top 5 Cities with Highest Profit Margins": """
        SELECT df1.city, SUM(df2.profit) / SUM(df2.sale_price * df2.quantity) * 100 AS profit_margin
        FROM df1 JOIN df2 ON df1.order_id = df2.order_id
        GROUP BY df1.city
        ORDER BY profit_margin DESC
        LIMIT 5;
    """,

    "3. Total Discount Given for Each Category": """
        SELECT df1.category, SUM(df2.discount_amount) AS total_discount
        FROM df1 JOIN df2 ON df1.order_id = df2.order_id
        GROUP BY df1.category
        ORDER BY total_discount DESC;
    """,

    "4. Average Sale Price Per Product Category": """
        SELECT df1.category, AVG(df2.sale_price) AS average_sale_price
        FROM df1 JOIN df2 ON df1.order_id = df2.order_id
        GROUP BY df1.category
        ORDER BY average_sale_price DESC;
    """,
    
    "5. Region with the Highest Average Sale Price": """
        SELECT df1.region, AVG(df2.sale_price) AS average_sale_price
        FROM df1
        JOIN df2 ON df1.order_id = df2.order_id
        GROUP BY df1.region
        ORDER BY average_sale_price DESC
        LIMIT 1;
    """,

    "6. Total Profit Per Category": """
        SELECT df1.category, SUM(df2.profit) AS total_profit
        FROM df1
        JOIN df2 ON df1.order_id = df2.order_id
        GROUP BY df1.category
        ORDER BY total_profit DESC;
    """,

    "7. Top 3 Segments with the Highest Quantity of Orders": """
        SELECT df1.segment, SUM(df2.quantity) AS total_quantity
        FROM df1
        JOIN df2 ON df1.order_id = df2.order_id
        GROUP BY df1.segment
        ORDER BY total_quantity DESC
        LIMIT 3;
    """,

    "8. Average Discount Percentage Given Per Region": """
        SELECT df1.region, AVG(df2.discount_percent) AS avg_discount_percent
        FROM df1
        JOIN df2 ON df1.order_id = df2.order_id
        GROUP BY df1.region;
    """,

    "9. Product Category with the Highest Total Profit": """
        SELECT df1.category, SUM(df2.profit) AS total_profit
        FROM df1
        JOIN df2 ON df1.order_id = df2.order_id
        GROUP BY df1.category
        ORDER BY total_profit DESC
        LIMIT 1;
    """,

    "10. Total Revenue Generated Per Year": """
        SELECT YEAR(df1.order_date) AS year, SUM(df2.sale_price * df2.quantity) AS total_revenue
        FROM df1
        JOIN df2 ON df1.order_id = df2.order_id
        GROUP BY year
        ORDER BY year;
    """,

    "11. Region with Highest Number of Orders": """
        SELECT df1.region, COUNT(df1.order_id) AS total_orders
        FROM df1
        JOIN df2 ON df1.order_id = df2.order_id
        GROUP BY df1.region
        ORDER BY total_orders DESC;
    """,

    "12. Most Profitable Customer Segment": """
        SELECT df1.segment,
           COUNT(DISTINCT df1.order_id) AS total_orders,
           SUM(df2.sale_price * df2.quantity) AS total_revenue,
           SUM(df2.profit * df2.quantity) AS total_profit
        FROM df1
        JOIN df2 ON df1.order_id = df2.order_id
        GROUP BY df1.segment
        ORDER BY total_revenue DESC;
    """,

    "13. Orders with Maximum Profit Margin": """
        SELECT df1.order_id, df1.city, df1.state, df1.region,
           SUM(df2.profit * df2.quantity) / SUM(df2.sale_price * df2.quantity) AS profit_margin
        FROM df1
        JOIN df2 ON df1.order_id = df2.order_id
        GROUP BY df1.order_id, df1.city, df1.state, df1.region
        ORDER BY profit_margin DESC
        LIMIT 10;
    """,

    "14. City with Highest Average Profit Margin (LEFT JOIN)": """
        SELECT df1.city,
           AVG(df2.profit / (df2.sale_price * df2.quantity) * 100) AS avg_profit_margin
        FROM df1
        LEFT JOIN df2 ON df1.order_id = df2.order_id
        GROUP BY df1.city
        ORDER BY avg_profit_margin DESC
        LIMIT 1;
    """,

    "15. Top 5 Products with Highest Sale Price (INNER JOIN)": """
        SELECT df2.product_id, SUM(df2.sale_price) AS total_sale_price
        FROM df1
        INNER JOIN df2 ON df1.order_id = df2.order_id
        GROUP BY df2.product_id
        ORDER BY total_sale_price DESC
        LIMIT 5;
    """,

    "16. Top 5 Cities with Highest Total Quantity (RIGHT JOIN)": """
        SELECT df1.city, SUM(df2.quantity) AS total_quantity
        FROM df1
        RIGHT JOIN df2 ON df1.order_id = df2.order_id
        GROUP BY df1.city
        ORDER BY total_quantity DESC
        LIMIT 5;
    """,

    "17. Region with Highest Average Sale Price (FULL OUTER JOIN)": """
        SELECT region, AVG(sale_price) AS average_sale_price FROM (
            SELECT df1.region, df2.sale_price
        FROM df1
        LEFT JOIN df2 ON df1.order_id = df2.order_id
        UNION
        SELECT df1.region, df2.sale_price
        FROM df1
        RIGHT JOIN df2 ON df1.order_id = df2.order_id
    ) AS full_data
    GROUP BY region
    ORDER BY average_sale_price DESC;
    """,

    "18. Average Discount Percentage by State": """
        SELECT df1.state, AVG(df2.discount_percent) AS average_discount_percentage
        FROM df1
        INNER JOIN df2 ON df1.order_id = df2.order_id
        GROUP BY df1.state
        ORDER BY average_discount_percentage DESC;
    """,

    "19. Total Quantity Ordered by Segment": """
        SELECT df1.segment, SUM(df2.quantity) AS total_quantity_ordered
        FROM df1
        INNER JOIN df2 ON df1.order_id = df2.order_id
        GROUP BY df1.segment
        ORDER BY total_quantity_ordered DESC;
    """,

    "20. Top 5 Orders with Highest Discount Given": """
        SELECT df1.order_id, df2.discount_amount, df1.segment, df1.category
        FROM df1
        INNER JOIN df2 ON df1.order_id = df2.order_id
        ORDER BY df2.discount_amount DESC
        LIMIT 5;
    """
}

# --------------------- PAGE 1: INTRO ---------------------
if page == "📊 Project Introduction":
    st.title("📊 Retail Order Analysis")
    st.subheader("Explore key sales insights from retail data stored in MySQL.")
    st.markdown("""
    This Streamlit app connects to **MySQL (localhost)** and presents **20 business insights** using SQL.

    **Features:**
    - Run 20 different SQL queries
    - Visualize top-performing categories, regions, discounts, and more
    - Interactive UI with navigation tabs

    **Database Used:** `retail_orders1` (MySQL (localhost))
    """)

# --------------------- PAGE 2: SQL QUERIES ---------------------
elif page == "📋 SQL Query Results":
    st.title("📋 SQL Query Results")

    # Split queries into two parts
    queries1_10 = dict(list(queries.items())[:10])
    queries11_20 = dict(list(queries.items())[10:])

    # Use Tabs
    tab1, tab2 = st.tabs(["Queries 1–10", "Queries 11–20"])

    with tab1:
        selected_query_1 = st.selectbox("Select a Query (1–10):", list(queries1_10.keys()))
        try:
            result1 = run_query(queries1_10[selected_query_1])
            st.subheader(f"📌 {selected_query_1}")
            st.dataframe(result1)
        except Exception as e:
            st.error(f"Error: {e}")

    with tab2:
        selected_query_2 = st.selectbox("Select a Query (11–20):", list(queries11_20.keys()))
        try:
            result2 = run_query(queries11_20[selected_query_2])
            st.subheader(f"📌 {selected_query_2}")
            st.dataframe(result2)
        except Exception as e:
            st.error(f"Error: {e}")


# --------------------- PAGE 3: CREATOR ---------------------
elif page == "👩‍💻 Creator Info":
    st.title("👩‍💻 Creator Info")
    st.markdown("""
    **Project By:** Snigdha Maheshbabu  
    **Skills:** Python, SQL, Data Analysis, Streamlit, MySQL (localhost)

    """)
