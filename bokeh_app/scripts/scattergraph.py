from os.path import dirname, join
from django.shortcuts import render
import os
import numpy as np
import pandas as pd
import math
import datetime
import sqlite3 as sql

from bokeh.plotting import figure

from bokeh.models import (CategoricalColorMapper, HoverTool, GMapOptions, WheelZoomTool, NumberFormatter,
						  ColumnDataSource, Panel, Span, NumeralTickFormatter, HTMLTemplateFormatter, DateFormatter,
						  FuncTickFormatter, SingleIntervalTicker, LinearAxis)

from bokeh.models.widgets import (CheckboxGroup, Slider, RangeSlider, Button,
								  Tabs, CheckboxButtonGroup, MultiSelect,
								  TableColumn, DataTable, Select, TextInput)

from bokeh.layouts import (column, row, WidgetBox, layout)
from bokeh.palettes import Category20_16
from bokeh.plotting import gmap
from bokeh.events import ButtonClick
from bokeh.models.callbacks import CustomJS
from bokeh.transform import factor_cmap, factor_mark

Google_API = "AIzaSyASMYVNOlZoJjE5ObwpytcvtTNUO4GqUzw"


def scattergraph_tab(floorplans):
    df = floorplans


# column_names 
        # df = df.rename(columns={'project_name':'Neighborhood','builder_name':'Builder','city':'Market','master_plan':'Community','typical_lot_size':'Lot Size','total_units_planned':'Total Units','total_units_sold':'Units Sold','total_remaining':'Unsold Homes','hoa1':'HOA','assessments':'Tax Rate','plan_name_1_field':'Plan Name','field_of_beds_1_field':'Beds','field_of_floors_1_field':'Floors','garage_1_field':'Garages','square_footage_1_field':'Square Footage','price_1_field':'Base Price'})

# colors
        # movies["color"] = np.where(movies["Oscars"] > 0, "orange", "grey")
        # movies["alpha"] = np.where(movies["Oscars"] > 0, 0.9, 0.25)
        # movies.fillna(0, inplace=True)  # just replace missing values with zero
        # movies["revenue"] = movies.BoxOffice.apply(lambda x: '{:,d}'.format(int(x)))
    
    axis_map = {
        "Home Size": "Square Footage (1)",
        "Base Price": "Price (1)",
        "Lot Size (sf)": "Typical Lot Size",
        "Latitude": "Lat",
        "Longitude": "Long",
        "Sales Rate": "Sales Rate"
    }

# desc = 
        #   Div(text=open(join(dirname(__file__), "description.html")).read(), sizing_mode="stretch_width")

# Max and Min Values    
    sf_max = math.ceil(df['Square Footage (1)'].max()/500)*500
    sf_min = math.floor(df['Square Footage (1)'].min()/500)*500
    price_max = math.ceil(df['Price (1)'].max()/50000)*50000
    price_min = math.floor(df['Price (1)'].min()/50000)*50000
    lot_max = math.ceil(df['Typical Lot Size'].max()/500)*500
    lot_min = math.floor(df['Typical Lot Size'].min()/500)*500

# Input controls
    max_sf_widget = TextInput(title = "Maximum Square Footage", value = str(sf_max))
    min_sf_widget = TextInput(title = "Minimum Square Footage", value = str(sf_min))
    max_price_widget = TextInput(title = "Maximum Base Price", value = str(price_max))
    min_price_widget = TextInput(title = "Minimum Base Price", value = str(price_min))
    max_lot_size_widget = TextInput(title = "Maximum Lot Size (sf)", value = str(lot_max))
    min_lot_size_widget = TextInput(title = "Minimum Lot Size (sf)", value = str(lot_min))

    # builder_select = MultiSelect(title="Builder Select", value=sorted(list(df['Builder Name'].unique())),options=sorted(list(df['Builder Name'].unique())))
    # market_select = MultiSelect(title="Market Select", value=sorted(list(df['City'].unique())),options=sorted(list(df['City'].unique())))

    x_axis = Select(title = "X Axis", options = sorted(axis_map.keys()), value = "Home Size")
    y_axis = Select(title = "Y Axis", options = sorted(axis_map.keys()), value = "Base Price")

    fha_span = Span(location=403000,dimension='width', line_color='blue',line_dash='dashed', line_width=.1)
    cll_span = Span(location=453100,dimension='width', line_color='green',line_dash='dashed', line_width=.1) 

    sf_slider = RangeSlider(title="Square Footage", start=sf_min, end=sf_max, value=(sf_min,sf_max), step=500, value_throttled=(250,250))
    price_slider = RangeSlider(title="Base Price", start=price_min, end=price_max, value=(price_min,price_max), step=500, value_throttled=(50000,50000))
    lot_slider = RangeSlider(title="Lot Size (SF)", start=lot_min, end=lot_max, value=(lot_min,lot_max), step=500, value_throttled=(250,250))


# Create Column Data Source that will be used by the plot
    source = ColumnDataSource(data=dict(SF=[], Price=[], Builder=[], Color=[], Neighborhood=[], LotSize=[], Market=[], Sales_Rate =[], Total_Homes=[], Homes_Sold=[], Unsold_Homes=[], Beds=[], Baths=[], HOA=[], Tax_Rate=[], Floors=[], Lat=[], Long=[], Submarket=[], OpenDate=[]))    # source = ColumnDataSource(data=df)

# TOOLTIPS=[
    #     ("Title", "@title"),
    #     ("Year", "@year"),
    #     ("$", "@revenue")
    # ]

    floors = [str(x) for x in df['# of Floors (1)'].unique()]
    markers = ['hex','circle_x','triangle','square']
    # p = figure(plot_height=600, plot_width=700, title="", toolbar_location=None, tooltips=TOOLTIPS, sizing_mode="scale_both")

# Create plots and attributes
    p = figure(plot_height=500, plot_width=800, title="Competitive Market Area")
    p.scatter(x='SF', y='Price', source=source, size=15, line_color='black', fill_alpha=.25,

            # legend='Floors',
            # # marker=factor_mark('Floors', markers, floors),
            # color=factor_cmap('Floors', 'Category10_4', floors)
            )
    map_options = GMapOptions(lat=df.Lat.mean(), lng=df.Long.mean(), map_type="roadmap", zoom=8)
    pmap = gmap(Google_API, map_options, plot_width=360, plot_height=400, title="CMA Map", toolbar_location="above")
    pmap.circle(x="Long", y="Lat", size=15, fill_color='blue', fill_alpha=0.25, line_color='black', line_width=.08, source=source)

    p.yaxis.formatter=NumeralTickFormatter(format="$ 0,0")
    p.xaxis.formatter=NumeralTickFormatter(format="0,0")    

# Filter dataframe based on widget inputs
    def filter_df():
        # builder_list = [builder_select_widget.labels[i] for i in builder_select_widget.active]
        # market_list = [market_select_widget.labels[i] for i in market_select_widget.active]

        # submarket_val = submarket.value.strip()
        selected = df[
            (df['Square Footage (1)'] <= float(sf_slider.value[1])) & 
            (df['Square Footage (1)'] >= float(sf_slider.value[0])) &
            (df['Price (1)'] <= float(price_slider.value[1])) &
            (df['Price (1)'] >= float(price_slider.value[0])) &
            (df['Typical Lot Size'] <= float(lot_slider.value[1])) &
            (df['Typical Lot Size'] >= float(lot_slider.value[0])) 
            # (df['Builder Name'].isin(builder_list)) &
            # (df['City'].isin(market_list))
        ]
        # if submarket_val != "All":
        #     selected = selected[selected['Submarket'].str.contains(submarket_val)==True]
        return selected

# Update df 
    def update():
        df = filter_df()
        df = df.sort_values(by=['Project Name'])

        p.xaxis.axis_label = x_axis.value
        p.yaxis.axis_label = y_axis.value
        # p.title.text = "%d Floorplans Selected, %d Communities Selected, %d Builders Selected" % (len(df), df.Neighborhood.nunique(), df.Builder.nunique())
        
        source.data = dict(
            # x=df[x_name],
            # y=df[y_name],
            SF=df['Square Footage (1)'],
            Price=df['Price (1)'],
            # Color=df['Color'], 
            Neighborhood=df['Project Name'],
            Floors=df['# of Floors (1)'], 
            Builder=df['Builder Name'],
            Market=df['City'], 
            Lot_Size=df['Typical Lot Size'],
            Sales_Rate=df['Sales Rate'],
            Total_Homes=df['Total Units Planned'], 
            Homes_Sold=df['Total Units Sold'],
            Unsold_Homes=df['Total Remaining'], 
            HOA=df['HOA1'], 
            Tax_Rate=df['Assessments'],
            Beds=df['# of Beds (1)'],
            Baths=df['# of Baths (1)'],
            Lat=df['Lat'],
            Long=df['Long'],
            # Submarket=df['Submarket'],
            # Open_Date=df['Open Date']
        )
        
# Add plot tools
    hover_callback = CustomJS(code="""var tooltips = document.getElementsByClassName("bk-tooltip");
            for (var i = 0, len = tooltips.length; i < len; i ++) {
                tooltips[i].style.top = "25px"; // unset what bokeh.js sets
                tooltips[i].style.left = "100px";
                tooltips[i].style.bottom = "";
                tooltips[i].style.right = "";
                """)
    hover_callback2 = CustomJS(code="""var tooltips = document.getElementsByClassName("bk-tooltip");
                for (var i = 0, len = tooltips.length; i < len; i ++) {
                tooltips[i].style.top = "25px"; // unset what bokeh.js sets
                tooltips[i].style.left = "-700px";
                tooltips[i].style.bottom = "";
                tooltips[i].style.right = "";
                }""")

    hover = HoverTool(tooltips = 
        [('Neighborhood','@Neighborhood'),
        ('Builder', '@Builder'),
        ('Market', '@Market'),
        ('Lot Size','@{Lot_Size}{(0,0)}'" SF"),
        ('Square Footage','@{SF}{0,0SF}'" SF"),
        ('Base Price','@{Price}{$0,0}'),
        ('Floors','@Floors'),
        ('Sales Rate','@{Sales_Rate}{(0.0)}'"/Mo"),
        ('Beds/Baths','@{Beds}'"/"'@{Baths}{(0.0)}'),
        ],
        callback = hover_callback,
        show_arrow=False,
        point_policy='snap_to_data')
    hover2 = HoverTool(tooltips = 
        [('Neighborhood','@Neighborhood'),
        ('Builder', '@Builder'),
        ('Market', '@Market'),
        ('Lot Size','@{Lot_Size}{(0,0)}'" SF"),
        ('Square Footage','@{SF}{0,0SF}'" SF"),
        ('Base Price','@{Price}{$0,0}'),
        ('Floors','@Floors'),
        ('Sales Rate','@{Sales_Rate}{(0.0)}'"/Mo"),
        ('Beds/Baths','@{Beds}'"/"'@{Baths}{(0.0)}'),
        ],
        callback = hover_callback2,
        show_arrow=False,
        point_policy='snap_to_data')

    table_columns = [TableColumn(field='Neighborhood', title='Neighborhood'),
                TableColumn(field='Market', title='Market'),
                TableColumn(field='Builder', title='Builder'),
                TableColumn(field='SF', title='Home Size', formatter=NumberFormatter(format='0,0')),
                TableColumn(field='Price', title='Base Price', formatter=NumberFormatter(format='$ 0,0[.]00'))
                # TableColumn(field="Sales_Rate", title="Sales Rate",formatter=HTMLTemplateFormatter(template='<code><%= value +" / Mo" %></code>')),
                # TableColumn(field="Lot_Size", title='Avg Lot Size',formatter=HTMLTemplateFormatter(template='<code><%= value +" SF" %></code>')),
                # TableColumn(field="Open_Date", title="Open Date",formatter=DateFormatter(format="%m/%d/%Y"))
                ]
                
    def floorplans_query():
        print('something')
        floorplans = pd.read_csv(join(dirname(join(dirname(__file__))),'data','floorplans.csv'))
        con = sql.connect(join('data','Market.db'))
        floorplans.to_sql('floorplans', con, if_exists='replace')
        con.close()
        print(floorplans)
        return print('Data uploaded from CSV!')
        scattergraph_tab(floorplans)

    def download():
        date = datetime.datetime.now().strftime("%m_%d_%y_h%Hm%Ms%S")
        print('Testing')
        df.to_csv(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'data','Downloads','scattergraph'+str(date)+'.csv')))

    button_dl = Button(label="Download", button_type="success")
    button_ul = Button(label="Upload data from CSV", button_type="success")
    button_dl.on_click(download)
    button_ul.on_click(floorplans_query)
    table = DataTable(source=source,  columns = table_columns, editable=True, height=600, width=1200,fit_columns=True,scroll_to_selection=True)

    controls = [sf_slider, price_slider, lot_slider]

    for control in controls:
        control.on_change('value', lambda attr, old, new: update())
    
    p.add_tools(hover)
    pmap.add_tools(hover2)
    pmap.add_tools(WheelZoomTool())
    inputs = column([*controls,button_ul,button_dl], width=180, height=250)
    inputs.sizing_mode = "fixed"

# Create layout
    l = layout([
        [column([inputs]), p, pmap],
        table], 
        sizing_mode="fixed")

    tab = Panel(child = l, title = 'Scattergraph')

# Initial call of update
    update()


# Return
    return tab