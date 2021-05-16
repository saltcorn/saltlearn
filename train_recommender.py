from server.config import get_db_uri

from sqlalchemy import create_engine

import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline


engine = create_engine(get_db_uri())

sql = """
SELECT q.*, p.id as product_id , pl.id is not null as liked 
  FROM  questionnaire q cross join 
        "Product" p left JOIN
        "ProductLike" pl on 
    pl.sessionid = q.sessionid and
    pl.product = p.id """
preds=['wholookingfor','whatweartowork', 'ideal_sunday', 'idealsaturday','idealholiday','homealoneweekday','product_id' ]
df = pd.read_sql_query(sql, con=engine)
df_y = df['liked']
df_x = df[preds]

print(df_x)

preprocessor = ColumnTransformer(
        transformers=[            
            ('cat', OneHotEncoder(handle_unknown='ignore'), preds)])

clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('classifier', MLPClassifier())])


clf.fit(df_x, df_y)