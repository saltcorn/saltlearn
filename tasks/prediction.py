import pickle
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline

def predict(predictors, outcome, table, engine):
    sql_fields=[]
    num_preds=[]
    cat_preds=[]
    for pred in predictors:
        if pred.type.name in ['Int', 'Float']:
            sql_fields.append(pred.name)
            num_preds.append(pred.name)
        elif pred.type.name == "String":
            sql_fields.append(pred.name)
            num_preds.append(pred.name)
    
    sql_fields.append(outcome.name)
    sql = 'SELECT {0} FROM "{1}"'.format(",".join(sql_fields), table)
    df = pd.read_sql_query(sql, con=engine)
    df = df.dropna()
    df_y = df[outcome]
    df_x = df[num_preds+cat_preds]

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), num_preds),
            ('cat', OneHotEncoder(handle_unknown='ignore'), cat_preds)])
    
    clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('classifier', LinearRegression())])
    clf.fit(df_cat, df_y)

    s=pickle.dumps(clf)

    return