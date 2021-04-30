import pickle
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline

def predict(predictors, outcome, table, engine):
    sql_fields=[]
    all_preds=[]
    num_preds=[]
    cat_preds=[]
    for pred in predictors:
        if pred['type']['name'] in ['Int', 'Float']:
            sql_fields.append(pred['name'])
            all_preds.append(pred['name'])
            num_preds.append(pred['name'])
        elif pred['type']['name'] == "String":
            sql_fields.append(pred['name'])
            all_preds.append(pred['name'])
            cat_preds.append(pred['name'])
    
    sql_fields.append(outcome['name'])
    sql = 'SELECT {0} FROM "{1}"'.format(",".join(sql_fields), table)
    df = pd.read_sql_query(sql, con=engine)
    df = df.dropna()
    df_y = df[outcome['name']]
    df_x = df[all_preds]
    
    #following https://scikit-learn.org/stable/auto_examples/compose/plot_column_transformer_mixed_types.html
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), num_preds),
            ('cat', OneHotEncoder(handle_unknown='ignore'), cat_preds)])
    
    clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('classifier', LinearRegression())])

    print(cat_preds, num_preds)
    print(df_x)
    clf.fit(df_x, df_y)

    s=pickle.dumps(clf)

    return s