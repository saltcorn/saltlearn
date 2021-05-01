CREATE FUNCTION predict_Product_price (x Product, model_id integer)
  RETURNS double precision
AS $$
  return 5.0
$$ LANGUAGE plpython3u;