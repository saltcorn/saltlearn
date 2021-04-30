from server.config import get_db_uri
from tasks.prediction import predict
from sqlalchemy import create_engine
import pickle
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline

print(get_db_uri())

engine = create_engine(get_db_uri())


s1=predict(
    [{'name':'category', 'type':{"name":"String"}},
     {'name':'pricep2', 'type':{"name":"Float"}}],
    {'name':'price', 'type':{"name":"Float"}},
    "Product",
    engine)

clf2 = pickle.loads(s1)
pred=clf2.predict(pd.DataFrame.from_dict({
    'category': ["Clothing"],
    'pricep2':[45]
}))
print(pred)

#split into function
#store in db