from flask import Flask, render_template, g, request
import click
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, insert
from datetime import datetime

from sqlalchemy.sql.expression import select

app = Flask(__name__)

engine = create_engine('sqlite:///stocks.db')
metadata_obj = MetaData()
stock_table = Table("stocks", metadata_obj, Column('Name', String),  Column('Price', Integer), Column('Datetime', DateTime))
metadata_obj.create_all(engine)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/view/<stockname>")
def stock(stockname=None):
    s = select(stock_table).where(stock_table.c.Name == stockname)
    conn = engine.connect()
    cost = conn.execute(s).fetchall()[0][1]
    return render_template('stock.html', name=stockname, cost=cost)

@click.command()
@click.argument('name', 'price')
def create_stock(name, price = 0):
    with engine.connect() as conn:
        result = conn.execute(insert(stock_table),[{"Name": name, "Price": price, "Datetime": datetime.now()}])
        conn.commit()