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

df = pd.read_sql_query('SELECT category, price, pricep2 FROM "Product"', con=engine)
df = df.dropna()
df_y = df['price']


df_cat = df[['category', "pricep2"]]
#following https://scikit-learn.org/stable/auto_examples/compose/plot_column_transformer_mixed_types.html

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), ['pricep2']),
        ('cat', OneHotEncoder(handle_unknown='ignore'), ['category'])])

clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('classifier', LinearRegression())])


clf.fit(df_cat, df_y)

s=pickle.dumps(clf)
clf2 = pickle.loads(s)
pred=clf2.predict(pd.DataFrame.from_dict({
    'category': ["Clothing"],
    'pricep2':[45]
}))
print(pred)

#split into function
#store in db