from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table, Column, Integer, String, DateTime, insert
from datetime import datetime

engine = create_engine('sqlite:///stocks.db', echo=True)
metadata_obj = MetaData()
stock_table = Table("stocks", metadata_obj, Column('Name', String),  Column('Price', Integer), Column('Datetime', DateTime))
metadata_obj.create_all(engine)

stock = "abc"
price = 10

with engine.connect() as conn:
    result = conn.execute(insert(stock_table),[{"Name": stock, "Price": price, "Datetime": datetime.now()}])