from server.config import get_db_uri

from sqlalchemy import create_engine
import pickle
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline

print(get_db_uri())

engine = create_engine(get_db_uri())

df = pd.read_sql_query('SELECT category, price FROM "Product" where price is not null', con=engine)
df_y = df['price']


df_cat = df[['category']]

categorical_features = ['embarked', 'sex', 'pclass']
categorical_transformer = OneHotEncoder(handle_unknown='ignore')

preprocessor = ColumnTransformer(
    transformers=[
        #('num', numeric_transformer, numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), ['category'])])

clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('classifier', LinearRegression())])


clf.fit(df_cat, df_y)

s=pickle.dumps(clf)
clf2 = pickle.loads(s)
pred=clf2.predict(pd.DataFrame.from_dict({'category': ["Clothing"]}))
print(pred)
