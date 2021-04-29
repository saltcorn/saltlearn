import os
import json
from config_path import ConfigPath

def get_db_uri():
    sqlite = os.environ.get("SQLITE_FILEPATH")
    if sqlite:
        return "sqlite:///{0}".format(sqlite)
    dburl = os.environ.get("DATABASE_URL")
    if dburl:
        return dburl

    db = os.environ.get("PGDATABASE")
    user = os.environ.get("PGUSER")
    pw = os.environ.get("PGPASSWORD")
    host = os.environ.get("PGHOST", "localhost")
    port = os.environ.get("PGPORT", 5432)
    if None in [db,user, pw,host,port]:
        return get_db_uri_from_cfg()
    else: 
        return "postgresql://{0}:{1}@{2}:{3}/{4}".format(user,pw, host,port,db )

def get_db_uri_from_cfg():
    conf_path = ConfigPath('', '', 'saltcorn')
    with open(conf_path.readFilePath()) as json_file:
        data = json.load(json_file)
        db = data.get("database")
        user = data.get("user")
        pw = data.get("password")
        host = data.get("host", "localhost")
        port = data.get("port", 5432)
        return "postgresql://{0}:{1}@{2}:{3}/{4}".format(user,pw, host,port,db )