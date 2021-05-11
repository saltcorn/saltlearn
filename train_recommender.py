from server.config import get_db_uri

from sqlalchemy import create_engine
from surprise import NormalPredictor
from surprise import Dataset
from surprise import Reader
from surprise.model_selection import cross_validate

import pandas
import numpy as np

engine = create_engine(get_db_uri())

df = pandas.read_sql_query('SELECT * FROM "ProductLike"', con=engine)
df = df[df.sessionid.notnull()]
df['rating'] = 1
reader = Reader(rating_scale=(0, 1))
data = Dataset.load_from_df(df[['sessionid', 'product', 'rating']], reader)
res=cross_validate(NormalPredictor(), data, cv=2)
print(res)