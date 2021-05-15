from server.config import get_db_uri

from sqlalchemy import create_engine

import pandas as pd
import numpy as np

engine = create_engine(get_db_uri())

sql = """
SELECT q.*, p.id as product_id , pl.id is not null as like_id 
  FROM  questionnaire q cross join 
        "Product" p left JOIN
        "ProductLike" pl on 
    pl.sessionid = q.sessionid and
    pl.product = p.id """

df = pd.read_sql_query(sql, con=engine)
print(df)
print(df.like_id.unique())
#print(pd.get_dummies(df, columns=["homealoneweekday", "idealholiday", "idealsaturday", "ideal_sunday"]))

#what about the ones they didnt like?

#print(res) 