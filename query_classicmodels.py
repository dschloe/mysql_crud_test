import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def query_database():
    # SQLite 데이터베이스 연결
    conn = sqlite3.connect('classicmodels_db.sqlite')
    
    # 테이블 목록 조회
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("\nAvailable tables:")
    for table in tables:
        print(f"- {table[0]}")
    
    # 각 테이블의 데이터 조회 및 시각화
    for table in tables:
        table_name = table[0]
        print(f"\nData from {table_name} table:")
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql_query(query, conn)
        print(f"Total rows in {table_name}: {len(df)}")
        
        # 테이블별 시각화
        if table_name == 'customers':
            # 국가별 고객 수 시각화
            plt.figure(figsize=(12, 6))
            country_counts = df['country'].value_counts().head(10)
            sns.barplot(x=country_counts.values, y=country_counts.index)
            plt.title('Top 10 Countries by Number of Customers')
            plt.xlabel('Number of Customers')
            plt.tight_layout()
            plt.savefig('customers_by_country.png')
            plt.close()
            
        elif table_name == 'products':
            # 제품 라인별 평균 가격 시각화
            plt.figure(figsize=(12, 6))
            product_line_prices = df.groupby('productLine')['MSRP'].mean().sort_values(ascending=False)
            sns.barplot(x=product_line_prices.values, y=product_line_prices.index)
            plt.title('Average MSRP by Product Line')
            plt.xlabel('Average MSRP')
            plt.tight_layout()
            plt.savefig('product_prices.png')
            plt.close()
            
        elif table_name == 'orders':
            # 월별 주문 수 시각화
            df['orderDate'] = pd.to_datetime(df['orderDate'])
            df['month'] = df['orderDate'].dt.to_period('M')
            monthly_orders = df['month'].value_counts().sort_index()
            
            plt.figure(figsize=(12, 6))
            monthly_orders.plot(kind='line', marker='o')
            plt.title('Number of Orders by Month')
            plt.xlabel('Month')
            plt.ylabel('Number of Orders')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig('orders_by_month.png')
            plt.close()
            
        elif table_name == 'orderdetails':
            # 주문 금액 분포 시각화
            df['total_amount'] = df['quantityOrdered'] * df['priceEach']
            plt.figure(figsize=(12, 6))
            sns.histplot(df['total_amount'], bins=30)
            plt.title('Distribution of Order Amounts')
            plt.xlabel('Order Amount')
            plt.ylabel('Frequency')
            plt.tight_layout()
            plt.savefig('order_amounts_distribution.png')
            plt.close()
    
    # 연결 종료
    conn.close()

if __name__ == "__main__":
    query_database()
    print("\nVisualizations have been saved as PNG files in the current directory.") 