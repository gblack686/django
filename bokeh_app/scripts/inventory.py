from bokeh.core.properties import field
from bokeh.core.properties import value
from bokeh.io import curdoc, output_notebook
from bokeh.layouts import layout, column, row, WidgetBox
from bokeh.models import (ColumnDataSource, HoverTool, SingleIntervalTicker, Panel,
                          Slider, Button, Label, CategoricalColorMapper, PrintfTickFormatter)
from bokeh.palettes import Spectral6
from bokeh.plotting import figure, show
from bokeh.transform import factor_cmap



import bokeh
import numpy as np
import pandas as pd
import datetime as dt

# df['Start Date'] = pd.to_datetime(df['Start Date'])
# df['Start Month'] = pd.to_datetime(df['Start Date']).dt.strftime("%Y-%b")

def inventory_tab(inventory):
    df = pd.DataFrame(inventory)
    top_owners = list(df.groupby('Market').agg('sum').reset_index()[['Market','Unsold Homes']].sort_values('Unsold Homes',ascending=False)[:12]['Market'])
    top_owners_df = df[df['Market'].isin(top_owners)]
    top_owners_df = top_owners_df[top_owners_df['Site Condition']!='Sold Out']
    x_axis = list(top_owners)
    stacks = list(top_owners_df['Site Condition'].unique())
    colors = ['green','blue','crimson','tan']

    data = {}
    for x in top_owners_df['Site Condition'].unique():
        group_df = top_owners_df[top_owners_df['Site Condition'] == x]
        loop_list = []
        for each in top_owners:
            y = group_df[group_df[("Market")]==each]['Unsold Homes'].sum()
            loop_list.append(y)
        data[x] = loop_list

    data.update({'x_axis':x_axis})


    p = figure(x_range=x_axis, plot_width=1400, plot_height=650, title="Projected Absorption",
            toolbar_location=None, tools="hover", tooltips='@x_axis @$name:$name')

    # p.vbar(x='Market', top='Unsold Homes', width=0.9, source=source)
    p.vbar_stack(stacks, x='x_axis', width=.9, color=colors, source=data, legend=[value(x) for x in stacks])

    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    p.axis.minor_tick_line_color = None
    p.outline_line_color = None
    p.legend.location = "top_right"
    p.legend.orientation = "horizontal"
    p.xaxis.major_label_orientation = .45
    p.xaxis.axis_label = 'Market'
    p.yaxis.axis_label = 'Unsold Homes'

    layout = p

    tab = Panel(child=layout, title='Inventory')

    return tab

