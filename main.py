from dotenv import load_dotenv
import os
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from urllib.parse import quote_plus

load_dotenv()

df = pd.read_csv("sales.csv")

print("orignal data:")
print(df)

df["total"] = df["price"] * df["quantity"]

print("\nAfter adding total:")
print(df)

print("\nTotal revenue:")
print(df["total"].sum())

print("\nRevenue by product:")
print(df.groupby("product")["total"].sum())

top_product = df.groupby("product")["total"].sum().idxmax()
print("\nTop earning product:", top_product)

revenue = df.groupby("product")["total"].sum()

revenue.plot(kind="bar")
plt.title("revenue by product")
plt.xlabel("product")
plt.ylabel("revenue")

plt.show()

user = os.getenv("DB_USER")
password = quote_plus(os.getenv("DB_PASSWORD"))
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
db = os.getenv("DB_NAME")

engine = create_engine(
    f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"
)

df.to_sql("sales_data", engine, if_exists="replace", index=False)

print("Data saved to MySQL!")