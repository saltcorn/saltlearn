from server.config import get_db_uri

from sqlalchemy import create_engine

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline

print(get_db_uri())

engine = create_engine(get_db_uri())

df = pd.read_sql_query('SELECT category, price FROM "Product" where price is not null', con=engine)
df_y = df['price']
#print(df)
#dums=pd.get_dummies(df["category"])
#print(dums)

df_cat = df[['category']]

categorical_features = ['embarked', 'sex', 'pclass']
categorical_transformer = OneHotEncoder(handle_unknown='ignore')

preprocessor = ColumnTransformer(
    transformers=[
        #('num', numeric_transformer, numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), ['category'])])

# Append classifier to preprocessing pipeline.
# Now we have a full prediction pipeline.
clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('classifier', LinearRegression())])

# Append classifier to preprocessing pipeline.
# Now we have a full prediction pipeline.
#xform = Pipeline(steps=[('preprocessor', preprocessor)]).fit_transform(df_x)
clf.fit(df_cat, df_y)
pred=clf.predict(pd.DataFrame.from_dict({'category': ["Clothing"]}))
print(pred)