CREATE or replace FUNCTION predict_Product_price (xs "Product", model_id integer)
  RETURNS double precision
AS $$
  import pickle
  import pandas
  import json
  rv = plpy.execute("SELECT fitdump, definition FROM _sl_models where id = {0}".format(model_id), 1)
  clf2 = pickle.loads(rv[0]["fitdump"])
  ddict = {}
  defn = json.loads(rv[0]["definition"])
  for pred in defn['predictors']:
    ddict[pred['name']] = [xs[pred['name']]]
  pred=clf2.predict(pandas.DataFrame.from_dict(ddict))
  return pred[0]
$$ LANGUAGE plpython3u;
