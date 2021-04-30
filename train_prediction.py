from server.config import get_db_uri

from sqlalchemy import create_engine

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline

print(get_db_uri())

engine = create_engine(get_db_uri())

df = pd.read_sql_query('SELECT * FROM "Product" where price is not null', con=engine)
df_y = df['price']
print(df_y)
dums=pd.get_dummies(df["category"])
#print(dums)

df_cat = df[['category']]

preprocessor = ColumnTransformer(
    transformers=[('cat', OneHotEncoder(handle_unknown='ignore'), ['category'])])

#xform = Pipeline(steps=[('preprocessor', preprocessor)]).fit_transform(df_x)
xform = preprocessor.fit_transform(df)

# Append classifier to preprocessing pipeline.
# Now we have a full prediction pipeline.
#xform = Pipeline(steps=[('preprocessor', preprocessor)]).fit_transform(df_x)

print(xform)
model = LinearRegression()
model.fit(dums, df_y)
print(model)