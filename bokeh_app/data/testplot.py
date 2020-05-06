from bokeh.io import output_file, show, curdoc
from bokeh.models import ColumnDataSource, GMapOptions, WheelZoomTool
from bokeh.plotting import gmap
from bokeh.transform import factor_cmap
from bokeh.palettes import Spectral6


import pandas as pd

from api_keys import Google_API

df = pd.read_csv('inventory.csv')

map_options = GMapOptions(lat=df.Lat.mean(), lng=df.Long.mean(), map_type="roadmap", zoom=9)

# For GMaps to function, Google requires you obtain and enable an API key:
#
#     https://developers.google.com/maps/documentation/javascript/get-api-key
#
# Replace the value below with your personal API key:
p = gmap(Google_API, map_options, title="Austin")
p.add_tools(WheelZoomTool())

source = ColumnDataSource(df)


p.circle(x="Long", y="Lat", size=15, fill_color=factor_cmap('Site Condition', palette=Spectral6, factors=list(df['Site Condition'].unique())), fill_alpha=0.45, line_width=.01, source=source)

curdoc().add_root(p)