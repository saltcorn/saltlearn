from sqlalchemy import create_engine, MetaData, Table, Column, \
    Date, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import BYTEA, JSONB
from datetime import datetime


meta = MetaData()
models = Table('_sl_models', meta,
    Column('id', Integer, primary_key = True), 
    Column('fitdump', BYTEA), 
    Column('fit_at', Date), 
    Column('definition', JSONB),
    Column('table_id', ForeignKey('_sc_tables.id')),
)


def insert_model(fitdump, definition,table_id , engine):
    ins = models.insert().values(
        fitdump =fitdump, 
        table_id=table_id, 
        definition=definition,
        fit_at=datetime.now()
        )
    conn = engine.connect()
    result = conn.execute(ins)
"""
create table _sl_models(
    id serial primary key,
    fitdump bytea,
    fit_at timestamp,
    definition jsonb,
    table_id int references _sc_tables(id)
);

"""