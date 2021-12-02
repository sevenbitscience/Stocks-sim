from flask import Flask, render_template, g, request
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

@app.route("/view/<stock>")
def stock(stock=None):
    s = select(stock_table).where(stock_table.c.Name == stock)
    conn = engine.connect()
    cost = conn.execute(s).fetchall()[0][1]
    return render_template('stock.html', name=stock, cost=cost)

@app.route("/manage-stock", methods=["GET", "POST"])
def manage_stock():
    if request.method == 'POST':
        stock = request.form.get("stock_name")
        price = request.form.get("price")
        with engine.connect() as conn:
            result = conn.execute(insert(stock_table),[{"Name": stock, "Price": price, "Datetime": datetime.now()}])
            conn.commit()
        return render_template("manage-stock.html", name=stock, submitted=True)
    return render_template("manage-stock.html", submitted=False)