from server.config import get_db_uri

from sqlalchemy import create_engine

import pandas

print(get_db_uri())

engine = create_engine(get_db_uri())

df = pandas.read_sql_query('SELECT * FROM "ProductLike"', con=engine)

print(df)