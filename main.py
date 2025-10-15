from config import get_connection
import pandas as pd

conn = get_connection()
cursor = conn.cursor()

with open("sql/01_success_rate_by_category.sql", "r") as f:
    query = f.read()

cursor.execute(query)
rows = cursor.fetchall()

cols = [desc[0] for desc in cursor.description]
df = pd.DataFrame(rows, columns=cols)
print(df)

cursor.close()
conn.close()
