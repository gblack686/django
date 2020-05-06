#!/usr/bin/env python
# Pandas for data management
import pandas as pd
import sqlite3 as sql
import os
import math
from os.path import dirname, join

from flask import Flask, render_template

from bokeh.embed import server_document
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
from bokeh.server.server import Server
from bokeh.themes import Theme
from tornado.ioloop import IOLoop

# Bokeh basics 
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs
from bokeh.themes import built_in_themes
from bokeh.embed import components

# Each tab is drawn by one script

from scripts.scattergraph import scattergraph_tab
from scripts.inventory import inventory_tab
from scripts.comps import comps_tab

app = Flask(__name__)

def create_doc(doc):
	# Using included state data from Bokeh for map
	from bokeh.sampledata.us_states import data as states

	# Read data into dataframes
	flights = pd.read_csv(join(dirname(__file__), 'data', 'flights.csv'), 
		                                          index_col=0).dropna()

	# Formatted Flight Delay Data for map
	map_data = pd.read_csv(join(dirname(__file__), 'data', 'flights_map.csv'),
	                            header=[0,1], index_col=0)

	# Read data from sqlite db
	floorplans = pd.read_sql("SELECT * FROM floorplans", sql.connect(join(dirname(__file__),'data','Market.db')))
	inventory = pd.read_sql("SELECT * FROM inventory i JOIN markets m ON i.market = m.name", sql.connect(join(dirname(__file__),'data','Market.db')))
	comps = pd.read_sql("SELECT * FROM sales_comps sc JOIN markets m ON sc.market = m.name", sql.connect(join(dirname(__file__),'data','Market.db')))

	# Create tabs
	tab1 = scattergraph_tab(floorplans)
	tab2 = inventory_tab(inventory)
	tab3 = comps_tab(comps)

	# Put all the tabs into one application
	tabs = Tabs(tabs = [tab1, tab2, tab3])

	# Put the tabs in the current document for display
	doc.add_root(tabs)
	# doc.theme = Theme(filename="theme.yaml")


@app.route('/', methods=['GET'])
def bkapp_page():
    script = server_document('http://localhost:5006/bkapp')
    return render_template("embed.html", script=script, template="Flask")


def bk_worker():
    # Can't pass num_procs > 1 in this configuration. If you need to run multiple
    # processes, see e.g. flask_gunicorn_embed.py
    server = Server({'/bkapp': create_doc}, io_loop=IOLoop(), allow_websocket_origin=["localhost:8000"])
    server.start()
    server.io_loop.start()

from threading import Thread
Thread(target=bk_worker).start()

if __name__ == '__main__':
    print('Opening single process Flask app with embedded Bokeh application on http://localhost:8000/')
    print()
    print('Multiple connections may block the Bokeh app in this configuration!')
    print('See "flask_gunicorn_embed.py" for one way to run multi-process')
    app.run(port=8000)
