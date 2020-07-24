import sys
import sqlite3
import pandas as pd

conn = sqlite3.connect('/Users/marcusmelo/Desktop/projeto_m4_gh/tendencias_musicais_web/db.sqlite3')

table_name = sys.argv[1]
csv_path = sys.argv[2]
data_df = pd.read_csv(csv_path)

data_df.to_sql(table_name, con=conn, if_exists='append', index=False)

conn.commit()
conn.close()
