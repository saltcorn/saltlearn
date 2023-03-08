from server.config import get_db_uri
from tasks.prediction import predict
from dbmodels.model import models, insert_model
from sqlalchemy import create_engine
import pickle
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.mixture import GaussianMixture

engine = create_engine(get_db_uri())

sql = """
SELECT id, ftx
  FROM  "sub2"."MeasurementA" m
  where id >890 and id< 1300
  """
#preds=['wholookingfor','whatweartowork', 'ideal_sunday', 'idealsaturday','idealholiday','homealoneweekday','product_id' ]
df = pd.read_sql_query(sql, con=engine)

np = len(df['ftx'][0])
cols = ["foo{0}".format(x) for x in range(0,255)]
df1 = pd.DataFrame(df["ftx"].to_list(), columns=["f{0}".format(x) for x in range(0,255)])
print(df1)
gm = GaussianMixture(n_components=2, random_state=0).fit(df1)
print(gm.predict_proba(df1.iloc[[0]]))
conn = engine.connect()
for index, row in df1.iterrows():
    proba = gm.score_samples(df1.iloc[[index]])[0]
    id=df["id"][index]
    sqlup = """update "sub2"."MeasurementA" set anomaly_score = {0} where id = {1}""".format(proba, id)
    print(index, id, proba, sqlup)
    result = conn.execute(sqlup)
    print(result)




#["foo{0}".format(x) for x in range(0,255)]

#df_y = df['liked']
#df_x = df[preds]