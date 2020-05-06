from os.path import dirname, join
from django.shortcuts import render
import os
import numpy as np
import pandas as pd
import math
import datetime

from bokeh.plotting import figure

from bokeh.models import (CategoricalColorMapper, HoverTool, GMapOptions, WheelZoomTool, Select,
						  ColumnDataSource, Panel, Span, NumeralTickFormatter, Slider, Button, Label,
						  FuncTickFormatter, SingleIntervalTicker, LinearAxis)

from bokeh.models.widgets import (CheckboxGroup, Slider, RangeSlider, Button,
								  Tabs, CheckboxButtonGroup, MultiSelect,
								  TableColumn, DataTable, Select, TextInput)

from bokeh.layouts import (column, row, WidgetBox, layout)
from bokeh.palettes import Category20_16, Spectral6, Viridis256
from bokeh.plotting import gmap
from bokeh.models.callbacks import CustomJS
from bokeh.transform import factor_cmap, factor_mark
from bokeh.core.properties import field, value


date = datetime.datetime.now().strftime("%m_%d_%y_h%Hm%Ms%S")
Google_API = "AIzaSyASMYVNOlZoJjE5ObwpytcvtTNUO4GqUzw"

def comps_tab(comps):
    df = comps
    df['Close Date'] = pd.to_datetime(df['Close Date'])
    df = df.drop(columns=['index'])
    df['Size'] = 24
    df['Color'] = "#31AADE"
    df['xs'] = 'Close Date'
    df['ys'] = 'Finished Lot Value'


    SIZES = list(range(12, 36, 3))
    COLORS = Spectral6
    N_SIZES = len(SIZES)
    N_COLORS = len(COLORS)
    MARKERSOURCE = list(df['Site Condition'].unique())
    MARKERS = ['hex', 'circle_x', 'triangle','square']

    source = ColumnDataSource(df)


    columns = sorted(df.columns)
    discrete = [x for x in columns if df[x].dtype == object]
    continuous = [x for x in columns if x not in discrete]

    x_axis_select = Select(title='X-Axis', value='Close Date', options=columns)
    y_axis_select = Select(title='Y-Axis', value='Finished Lot Value', options=columns)
    size = Select(title='Size', value='None', options=['None'] + continuous)
    color = Select(title='Color', value='None', options=['None'] + continuous)
    kw = dict()
    x_title = x_axis_select.value.title()
    y_title = y_axis_select.value.title()
    df['xs'] = df[x_axis_select.value].values
    df['ys'] = df[y_axis_select.value].values
    x_title = x_axis_select.value.title()
    y_title = y_axis_select.value.title()

    kw = dict()
    if x_axis_select.value in discrete:
        kw['x_range'] = sorted(set(df['xs']))
    if y_axis_select.value in discrete:
        kw['y_range'] = sorted(set(df['ys']))
    kw['title'] = "%s vs %s" % (x_title, y_title)

    if x_axis_select.value in discrete:
        p.xaxis.major_label_orientation = pd.np.pi / 4

    df['Size'] = 24
    if size.value != 'None':
        if len(set(df[size.value])) > N_SIZES:
            groups = pd.qcut(df[size.value].values, N_SIZES, duplicates='drop')
        else:
            groups = pd.Categorical(df[size.value])
        df['Size'] = [SIZES[xx] for xx in groups.codes]

    df['Color'] = "#31AADE"
    if color.value != 'None':
        if len(set(df[color.value])) > N_COLORS:
            groups = pd.qcut(df[color.value].values, N_COLORS, duplicates='drop')
        else:
            groups = pd.Categorical(df[color.value])
        df['Color'] = [COLORS[xx] for xx in groups.codes]

    p = figure(plot_height=500, plot_width=800, tools='pan,box_zoom,hover,reset', **kw)
    p.xaxis.axis_label = x_title
    p.yaxis.axis_label = y_title
    map_options = GMapOptions(lat=df.Lat.mean(), lng=df.Long.mean(), map_type="roadmap", zoom=8)
    pmap = gmap(Google_API, map_options, plot_width=360, plot_height=400, title="CMA Map", toolbar_location="above")
    pmap.circle(x="Long", y="Lat", size=15, fill_color='Color', fill_alpha=0.25, line_color='black', line_width=.08, source=source)

    callback = CustomJS(code="""
            var tooltips = document.getElementsByClassName("bk-tooltip");
            for (var i = 0, len = tooltips.length; i < len; i ++) {
            tooltips[i].style.top = "10px"; // unset what bokeh.js sets
            tooltips[i].style.left = "800px";
            tooltips[i].style.bottom = "";
            tooltips[i].style.right = "";
            }
            """)

    p.scatter(x='xs', y='ys', color='Color', size='Size', line_color="white", alpha=0.6,
            marker=factor_mark('Site Condition', MARKERS, MARKERSOURCE),
            hover_color='white', hover_alpha=0.5, source=source)
    
    
    hover = HoverTool(tooltips = [(x_title,'@xs'),(y_title,'@ys'),('Name','@Neighborhood'),('FLV','@{Finished Lot Value}{$0,0}'),
        ('Community Count','@{Community Count}'),('Market_Tier','@{Market Tier}'),
        ('Close Date','@DateString'),('Lot Count','@{Lot Count}'),('Site_Condition','@{Site Condition}'),
        ('Seller','@Seller'),('Entitlements','@Entitlements'),('Market','@Market')],
        callback = callback)
    


    def select_df():

        # filter df here based on widget inputs
        selected = df
        # (df['Square Footage (1)'] <= float(sf_slider.value[1]))

        return selected


    def update():
        df = select_df()

        df['xs'] = df[x_axis_select.value].values
        df['ys'] = df[y_axis_select.value].values
        x_title = x_axis_select.value.title()
        y_title = y_axis_select.value.title()

        kw = dict()
        if x_axis_select.value in discrete:
            kw['x_range'] = sorted(set(df['xs']))
        if y_axis_select.value in discrete:
            kw['y_range'] = sorted(set(df['ys']))
        kw['title'] = "%s vs %s" % (x_title, y_title)

        if x_axis_select.value in discrete:
            p.xaxis.major_label_orientation = pd.np.pi / 4

        df['Size'] = 24
        if size.value != 'None':
            if len(set(df[size.value])) > N_SIZES:
                groups = pd.qcut(df[size.value].values, N_SIZES, duplicates='drop')
            else:
                groups = pd.Categorical(df[size.value])
            df['Size'] = [SIZES[xx] for xx in groups.codes]

        df['Color'] = "#31AADE"
        if color.value != 'None':
            if len(set(df[color.value])) > N_COLORS:
                groups = pd.qcut(df[color.value].values, N_COLORS, duplicates='drop')
            else:
                groups = pd.Categorical(df[color.value])
            df['Color'] = [COLORS[xx] for xx in groups.codes]

        source = df
        return source


    controls = [x_axis_select, y_axis_select, size, color]

    for control in controls:
        control.on_change('value', lambda attr, old, new: update())

    button = Button(label="Download", button_type="success")
    button.callback = df.to_csv(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'data','Downloads','sales_comps_'+str(date)+'.csv')))
    table = DataTable(source=source,  editable=True, height=600, width=1400,fit_columns=True,scroll_to_selection=True)

    widgets = column([*controls, button], width=180, height=250)
    widgets.sizing_mode = "fixed"


    # Make a tab with the layout 

    p.add_tools(hover)
    l = layout([
        [column([widgets]), p, pmap],
        table],
        sizing_mode='fixed')
    # l = layout(table)
    update()

    tab = Panel(child=l, title = 'Comps')
    return tab