from configparser import ConfigParser
from pathlib import Path
from urllib.parse import quote_plus

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text

config = ConfigParser()
loaded_files = config.read("config/database.ini")

if not loaded_files:
    raise FileNotFoundError("Could not find config/database.ini")

db = config["mysql"]

host = db["host"]
port = db.getint("port")
database = db["database"]
user = db["user"]
password = quote_plus(db["password"])

engine = create_engine(
    f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
)
# If use text encoding="utf--8" we can use the date as '%M/%D/%Y' otherwise needs to use double %%
sql = Path("members.sql").read_text(encoding="utf-8")

# If want to use WHERE Title LIKE :title in sql use this params
# params = {
#     "title": "%Leader%"
# }

df = pd.read_sql(text(sql), engine) #, params=params)
print(df.head())

# Select columns
df1_filtered = df[
    ['emp_no', 'Full_Name', 'Department', 'title', 'Salary']
].copy()

# Filter
df1_filtered = df1_filtered[
    df1_filtered["title"].str.contains("Leader", case=False, na=False)
]

# Remove duplicates
df1_filtered = df1_filtered.drop_duplicates(subset=["emp_no"])

# Rename headers
df1_filtered.columns = df1_filtered.columns.str.upper()

print(df1_filtered.head())