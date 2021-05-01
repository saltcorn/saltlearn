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


engine = create_engine(get_db_uri())
conn = engine.connect()
result = conn.execute('select 1;').fetchall()
print(result)