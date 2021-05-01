CREATE or replace FUNCTION predict_Product_price (xs "Product", model_id integer)
  RETURNS double precision
AS $$
  import pickle
  import pandas
  rv = plpy.execute("SELECT fitdump FROM _sl_models where id = {0}".format(model_id), 1)
  clf2 = pickle.loads(rv[0]["fitdump"])
  pred=clf2.predict(pandas.DataFrame.from_dict({
    'category': [xs["category"]],
    'pricep2':[xs["pricep2"]]
  }))
  return pred[0]
$$ LANGUAGE plpython3u;
