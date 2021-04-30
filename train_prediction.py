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

print(get_db_uri())

engine = create_engine(get_db_uri())

predictors=[{'name':'category', 'type':{"name":"String"}},
     {'name':'pricep2', 'type':{"name":"Float"}}]

outcome={'name':'price', 'type':{"name":"Float"}}
s1=predict(
    predictors,
    outcome,
    {'name':"Product",id:29},
    engine)

clf2 = pickle.loads(s1)
pred=clf2.predict(pd.DataFrame.from_dict({
    'category': ["Clothing"],
    'pricep2':[45]
}))
print(pred)

defn = {'predictors':predictors, 'outcome':outcome }
insert_model(s1, defn,29,engine)
#store in db

