#####################################################################
#####################################################################
#
# Author: Marcus G. Young, GWU, 2020

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
# import networkx as nx
import numpy as np
import plotly.io as pio
from plotly.subplots import make_subplots
from urllib.request import urlopen
import json
import sys
import platform

class datatool:

#####################################################################
#####################################################################
# INITIALIZATION

    # Dataframe object from Pandas 
    data = 0

    # Plotly express graph object
    fig = 0

    # Current continous color scale of a figure. Change color scale using set_color_scale(color)
    color_scale = 'aggrnyl'

    # Current color of drawn lines, rectangles and circles
    draw_color = 'black'

    # Current width of drawn lines, rectangles and circles
    draw_width = 1

    # Networkx Graph reference. Not currently in use for any examples. 
    graph = 0

    # File path used for exporting modified Pandas Dataframe objects
    path = ''

    # Row counters for figures with multiple subplots.
    # Current row
    row = 1

    # Number of rows needed to be made. This is set in make_choropleth_subplots(self, rows, cols, titles)
    rowCount = 0

    # Column counters for figures with multiple subplots. 
    # Current column
    col = 1

    # Number of columns needed to made This is set in make_choropleth_subplots(self, rows, cols, titles)
    colCount = 0

    # Initialize GeoJson
    geo_data = 0

    # List of csv files used 
    csv_stack = []

    # Custom x coordinate array
    cusx = []
    # Custom y coordinate array 
    cusy = []

    # Custom map location array
    cusmapl = []
    # Custom map data array
    cusmapd = []

    # To hold points for drawing lines in maps via lat-long points
    scatlon = []
    scatlat = []

    # Latitude, longitude and color col names.
    latcolname = 0
    loncolname = 0
    ccolname = 0

    #linemap line width variable
    lineWidth = 3

    #linemap line color variable
    lineColor = 'black'

    # Initialize Pandas Dataframe and empty subplot with secondary_y axis
    def __init__ (self):
        if platform.system().lower() == 'windows':
            pio.renderers.default = 'browser'
        else:
            pio.renderers.default = 'firefox'
        # Load GeoJson data for add_level3_choropleth()
        try:
            with urlopen('https://raw.githubusercontent.com/tdwg/wgsrpd/master/geojson/level3.geojson') as f:
                self.geo_data = json.load(f)
        # User local geojson if load fails.       
        except: 
            print('Could Not Load GeoJson from Git, loading from local file: level3.geojson.json')
            with open('level3.geojson.json') as geojson_file:
                self.geo_data = json.load(geojson_file)
        # Initialize our plotly figure
        self.fig = go.Figure()


#####################################################################
#####################################################################
# FIGURE/DISPLAY

    # Sets the default renderer of datatool. Default is firefox. 
    def set_renderer(self, renderer):
        pio.renderers.default = renderer

    # Display the figure
    def display(self):
        self.fig.show()

    # Sets the x-axis range
    def set_x_range(self, lowr, highr):
        self.fig.update_xaxes(range=[lowr, highr])

    # Sets the y-axis range
    def set_y_range(self, lowr, highr):
        self.fig.update_yaxes(range=[lowr, highr])

    # Sets the figure title
    def set_title(self, title):
        self.fig.update_layout(title=title)

    def set_legend_title(self, title):  
        self.fig.update_layout(legend=dict(title=title))  

    # Sets x axis title
    def set_x_axis_title(self, title):
        self.fig.update_layout(xaxis_title=title)

    # Sets y1 axis title (leftmost)
    def set_y_axis_title(self, title):
        self.fig.update_yaxes(title_text=title)

    # Sets y2 axis title (rightmost)
    def set_y2_axis_title(self, title):
        self.fig.update_yaxes(title_text=title, secondary_y=True)

    # Sets the color scale of the figure
    # Available Colors: https://plotly.com/python/builtin-colorscales/
    # There are different color scales (https://plotly.com/python/builtin-colorscales/) one can use to color scatter_geo_iso3, choropleth_iso3, and choropleth_iso3_animate maps.
    # For setting colors and widths of drawn lines, rectangles, arrows and circles see set_draw_color(self,color) and set_draw_width(self,width).
    def set_color_scale(self, color):
        self.color_scale = color

#####################################################################
#####################################################################
# DATA/PRINTING

    # Adds a csv file to the data stack, when multiple CSVs are used.
    def add_csv(self, csv):
        self.csv_stack.append(csv)

    #** Changed:

    # Loads the most recent csv file into self.data, 
    # Loads the given csv file off the data stack, and 
    # provides a Null Value count.
    def load_csv_top(self):
        cfile = self.csv_stack.pop()
        self.load_csv(cfile)

    #** Changed to directly load a CSV (until we find a good example for the stack approach

    def load_csv(self, cfile):
        try:
            self.data = pd.read_csv(cfile)
            #**Marcus: print only if there are nulls.
            # If any values of any row are null, print a null value count
            if self.data.isnull().values.any() == True:
                print('File: ' + cfile)
                print('Null Value Count per Column: ')
                print(self.data.isnull().sum())
            print('File: ' + cfile + ' successfully loaded')
        except FileNotFoundError:
            print("csv file: \'" + cfile + "\' not found, please try again")
            sys.exit()

    # Sorts data by column name in descending order
    def sort_desc(self, col):
        self.data = self.data.sort_values(by=[col], ascending=False) 

    # Sorts data by column name in ascending order
    def sort_asc(self, col):
        self.data = self.data.sort_values(by=[col]) 

    #** ADDED 12/6/20 new sort
    def sort_by_multiple_columns(self, col_list, ascend_list):
        self.data = self.data.sort_values(col_list, ascending=ascend_list)

    # Only keeps first n rows of a dataset
    def use_n_rows(self, n):
        self.data = self.data.head(n) 

    # Prints the column labels for users to see the columns    
    def print_column_labels(self):
        for col in self.data.columns:
            print(col)

    # Returns a list of columns without the first column (so we don't plot Y-Axis)  
    def get_col_list(self):
        ret_data = self.data.drop(self.data.columns[0], axis=1)
        return ret_data.columns.to_list()

    #** ADDED 
    def add_column(self, colname, values_as_list):
        self.data[colname] = values_as_list

    # Displays the data of the current Pandas Dataframe
    def print_data(self):
        print(self.data)

    # Sets the path for helper functions
    def set_data_path(self, path):
        self.path = path

    # For each row where any column values are NaN in the dataframe this removes the row
    # The third line creates a new csv file with the rows that had null values removed. 
    # The new csv file is saved in the self.path. 
    def clean_data(self, file_name):
        self.path += file_name
        self.data.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)
        self.data.to_csv(self.path)

    #********** BEGIN-NEW 
    def save_data_as(self, file_name):
        curpath = self.path + file_name
        self.data.to_csv(curpath)

    def get_data_as_array(self):
        return self.data.to_numpy()

    def set_data_from_array(self, A, index_col_values=None, col_headers=None):
        self.data = pd.DataFrame(A, index=index_col_values, columns=col_headers)
    #**** END-NEW

    # Returns a numpy array of the specified column
    def get_col_vals(self, column_name):
        for (columnName, columnData) in self.data.iteritems():
            if columnName == column_name:
                x = columnData.to_numpy()
        return x

    # Return rows containing a specific value in a column
    def cross_section(self, column_name, value, file_name):
        self.path += file_name
        self.data = self.data[self.data[column_name] == value]
        self.data.to_csv(self.path)


    # If any values of any row are NaN, remove that row using clean_data()
    def check_nan_df(self):
        if self.data.isnull().values.any() == True:
            self.clean_data()

    # Removes whitespace for given column nme
    def remove_whitespace(self, col_name, file_name):
        self.path += file_name
        self.data.columns.str.strip()
        self.data.to_csv(self.path)

    # Sorts the given column in ascending order
    def sort_col_asc(self, col_name, file_name):
        self.path += file_name
        self.data.sort_values(by=[col_name], ascending=True, inplace=True)
        self.data.to_csv(self.path)

    # Switches rows and columns
    def transpose(self, file_name):
        self.path += file_name
        self.data = self.data.transpose()
        self.data.to_csv(self.path)

    #Set hover template
    def set_hover_template(self, template):
        self.hovertemplate = template


#####################################################################
#####################################################################
# DRAWING AND PLOTTING


    # Line Graph with 1 y-axis
    def line_graph(self, x, y):
        self.fig.add_trace(go.Scatter(x=self.get_col_vals(x),y=self.get_col_vals(y),name=y))

    # Add second y-axis to line_graph
    def line_graph_y2(self, x, y):
        self.fig = make_subplots(specs=[[{'secondary_y': True}]])
        self.fig.add_trace(go.Scatter(x=self.getValues(x), y=self.getValues(y), name=y),
        	secondary_y=True,)

    # Line graph with connectgaps activated and shows scatter points and lines where gaps are connected
    def add_line_graph_connectgaps(self, x, y):
        self.fig.add_trace(go.Scatter(x=self.get_col_vals(x),
                                    y=self.get_col_vals(y),
                                    name=y, 
                                    mode='markers + lines',
                                    connectgaps=True),)

    #** Added name to be the same as the y column name
    # Simple bar chart
    def bar_chart(self, x, y):
        self.fig.add_trace(go.Bar(x=self.get_col_vals(x), y=self.get_col_vals(y), name=y))

    #** Changed parameter names
    # Bubble chart
    def bubble_chart(self, x=None, y=None, category=None, bubblesize=None, text=None):
        self.fig = px.scatter(self.data,
                                 x = x,
                                 y = y,
                                 size = bubblesize,
                                 color = category,
                                 size_max = 60,
                                 hover_name = text
                                 )

    # If this function executes without errors, packages installed correctly
    def simple_scatter(self, x, y, color):
        self.fig = px.scatter(self.data,
                                x = x,
                                y = y,
                                color=color)


#####################################################################
#####################################################################
# DRAWING


    # Draws a line with given coordinate endpoints
    #** Changed parameter names
    def draw_line(self, startx, starty, endx, endy):
        self.fig.add_shape(type='line', x0=startx, y0=starty, x1=endx, y1=endy, line=dict(width=self.draw_width, color=self.draw_color))

    # Rectangle is drawn using the lower_x and lower_y coordinates as the lower left hand corner of the rectangle, and scaling it by the height and width values
    #** Changed parameter names
    def draw_rectangle(self, lower_x, lower_y, width, height):
        self.fig.add_shape(type='rect', x0=lower_x, y0=lower_y, x1=lower_x+width, y1=lower_y+height, line=dict(width=self.draw_width, color=self.draw_color))

    # Circle is drawn from using the lower_x as the start of left hand side of the ellipse and lower_y as the bottom of the ellipse, and scaling it by the height and width values
    #** Changed parameters
    def draw_ellipse(self, lower_x, lower_y, width, height):
        self.fig.add_shape(type='circle', x0=lower_x, y0=lower_y, x1=lower_x+width, y1=lower_y+height, line=dict(width=self.draw_width, color=self.draw_color))

    # Draws an arrow from base(ax,ay) to arrowhead(x,y)
    def draw_arrow(self, ax, ay, x, y, arrowhead, arrowsize=None):
        self.fig.add_annotation(x=x,
                                y=y,
                                xref='x',
                                yref='y',
                                axref='x',
                                ayref='y',
                                ax=ax,
                                ay=ay,
                                arrowhead=arrowhead,
                                arrowsize=arrowsize,
                                showarrow=True,
                                arrowwidth=self.draw_width, 
                                arrowcolor=self.draw_color)

    #** Can you add a function to draw a string? (So that we can label things on the drawing)?
    def draw_text(self, x, y, text):
        self.fig.add_annotation(x=x,
                                y=y,
                                xref='x',
                                yref='y',
                                text=text,
                                showarrow=False)

    #** Can you add a function to set the draw color? Or is that already addressed by one of the earlier color functions?
    # Sets the color of drawn lines, rectangles, ellipses and arrows
    # Available colors: https://plotly.com/python-api-reference/generated/plotly.graph_objects.layout.shape.html#plotly.graph_objects.layout.shape.Line
    def set_draw_color(self, color):
        self.draw_color = color

    # Sets the width of drawn lines, rectangles, ellipses and arrows
    # Widths must be a value greater than or equal to 1
    def set_draw_width(self, width):
        self.draw_width = width
                            
    # Adds points to custom data
    def add_point(self, x, y):
        self.cusx.append(x)
        self.cusy.append(y)

    # Plots basic line graph using custom input data
    def plot_points(self):
        self.fig.add_trace(go.Scatter(x=self.cusx,
                                    y=self.cusy))


#####################################################################
#####################################################################
# LINE MAPS

    # Plots basic line graph using custom input data
    def plot_choro_map(self):
        self.fig.add_trace((go.Choropleth(locations=self.cusmapl,
                                            z = self.cusmapd)))
                            
    #** Added a simpler method as default
    def linemap(self, lat_col, long_col, marker_text=None):
        self.linemap_detailed(lat_col=lat_col, long_col=long_col, marker_color='Red', marker_size=8, marker_text=marker_text, hovertext=None, showlegend=None)

    #** Changed param names
                    
    def linemap_detailed(self, lat_col, long_col, marker_color=None, marker_size=None, marker_text=None, marker_text_size=10, hovertext=None, showlegend=None):
        mtext = ''
        if marker_text != None:
            mtext = self.data[marker_text]

        htext = None
        if hovertext != None:
            htext = self.data[hovertext]

        self.fig.add_trace(go.Scattergeo(
                    lat = self.data[lat_col],
                    lon = self.data[long_col],
                    mode = 'markers + text',
                    marker_color = marker_color,
                    marker_size = marker_size,
                    hoverinfo = 'lon + lat + text',
                    text = mtext,
                    hovertext = htext,
                    showlegend = showlegend,
                    #showlegend = None,
                    textposition = 'top center',
                    textfont=dict(
                        family='sans serif',
                        size=marker_text_size,
                        color='black'
                    )
                    ))

    # Sets line width
    def set_line_width(self, width):
        self.lineWidth = width

    # Sets line color
    def set_line_color(self, color):
        self.lineColor = color

    # Choropleth map using ISO-3 location data
    def choropleth_iso3(self, locations, color, hover_name):
        self.fig = px.choropleth(self.data,
                    locations = locations,
                    hover_name = hover_name,
                    color = color,
                    locationmode = 'ISO-3',
                    color_continuous_scale = self.color_scale)

    #Animated choropleth map that uses animate parameter to decide which column to animate the map by                
    def choropleth_iso3_animate(self, locations, color, hover_name, animate):
        self.fig = px.choropleth(self.data,
                    locations = locations,
                    color = color,
                    hover_name = hover_name,
                    animation_frame = animate,
                    locationmode = 'ISO-3',
                    color_continuous_scale = self.color_scale)

    # Plots a choropleth map based on US counties    
    #** Does this belong in the tilemap section? What's an example for using it?
    # This does belong in the linemap section. This function was intended to display plotly's ability to plot choropleth maps at a county level.
    # We don't have an example set up for this method and the example I implemented in the past isn't working currently so in light of this method not being used
    # in any current example it should be deleted.
    def county_choropleth(self, locations, color):
        try:
            with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as f:
                counties = json.load(f)
        except: 
            print('Could not load GeoJson from Git')
            sys.exit()

        self.fig = px.choropleth(self.data, geojson=counties, locations=locations, color=color,
                           color_continuous_scale=self.color_scale,
                           range_color=(0, 12),
                           scope='usa',
                           labels={'unemp':'unemployment rate'}
                          )
        self.fig.update_layout(margin={'r':0,'t':0,'l':0,'b':0})

    # Adds a level3 choropleth map subplot to a figure. You must use make_choropleth_subplots(rows, cols, titles) before using.
    def add_level3_choropleth(self, locations, color):
        self.fig.add_trace((go.Choropleth(geojson=self.geo_data, 
                                            locations=self.data[locations], 
                                            featureidkey='properties.LEVEL3_NAM',
                                            z = self.data[color],
                                            zmin = 0,
                                            zmax = 1
                            )),row=self.row, col=self.col)
        if self.row < self.rowCount and self.col == self.colCount:
            self.row += 1
            self.col = 1
        else:
            self.col += 1
    # Adds a normal choropleth map subplot to a figure. You must use make_choropleth_subplots(rows, cols, titles) before using.
    def add_choropleth(self, locations, color):
        self.fig.add_trace((go.Choropleth(locations=self.data[locations],
                                            zmin = self.data[color].min(),
                                            zmax = self.data[color].max(),
                                            z = self.data[color],
                            )),row=self.row, col=self.col)
        if self.row < self.rowCount and self.col == self.colCount:
            self.row += 1
            self.col = 1
        else:
            self.col += 1

    # Adds a normal scatter map subplot to a figure. You must use make_scattergeo_subplots(rows, cols, titles) before using.       
    def add_scattergeo(self, lat, lon, marker_color=None, marker_size=None, hovertext=None, showlegend=None, lineLat=None, lineLong=None):
        self.fig.add_trace((go.Scattergeo(
                    lat = self.data[lat],
                    lon = self.data[lon],
                    mode = 'markers + text',
                    marker_color = marker_color,
                    marker_size = marker_size,
                    hovertext = self.data[hovertext],
                    showlegend = showlegend,
                    textposition = 'top center',
                    textfont=dict(
                        family='sans serif',
                        size=16,
                        color='black'
                    ))),row=self.row, col=self.col)
        self.add_list_line(lineLat, lineLong)
        if self.row < self.rowCount and self.col == self.colCount:
            self.row += 1
            self.col = 1
        else:
            self.col += 1

    # Adds a line between two locations
    #** I've added linemap_add_line() below. Do we still need add_mig_line()?
    # I don't think we need this anymore, linemap_add_line() covers this method's functionality.
    # Deleted. 

    # Adds a line between two locations
    #** Added this. Note that linemaps and tilemaps are inconsistent
    # in lat-long (one uses strings, one uses numbers). It would be
    # best to let datatool functions use numbers.
    def linemap_add_line(self, lat1, long1, lat2, long2):  

        lat1 = str(lat1)
        long1 = str(long1)
        lat2 = str(lat2)
        long2 = str(long2)

        self.fig.add_trace(go.Scattergeo(
                        lat = [lat1, lat2],
                        lon = [long1, long2],
                        mode = 'lines',
                        hoverinfo= 'text',
                        line = dict(width = self.lineWidth, color = self.lineColor),
                        showlegend = False))


    # Adds a line between two coordinates
    #** How does this differ from the above? What is it for?
    # This method was helpful for migration_prediction.py in our anthro-example 2.
    # This method allowed me to input entire arrays of lattitude and longitude coordinates which was very helpful when plotting
    # multiple migration routes in migration_prediction.py.
    # This method isn't intended for users to use, it was just helpful when making migration_prediction.py
    def add_list_line(self, lat, lon):  
        self.fig.add_trace(go.Scattergeo(
                        lat = lat,
                        lon = lon,
                        mode = 'lines',
                        line = dict(width = 3, color = 'black'),
                        showlegend = False),row=self.row, col=self.col)

    # Make multiple plots
    #** linemap or tilemap? Example of use?
    # This would be a linemap since the method that depends on this is add_level3_choropleth() which is listed as a linemap.
    # See megafauna_sol.py in anthro-example1 for an example of use
    def make_choropleth_subplots(self, rows, cols, titles):
        self.rowCount = rows
        self.colCount = cols
        self.fig = make_subplots(rows=rows, 
                                cols=cols, 
                                specs = [[{'type': 'choropleth'} for c in np.arange(cols)] for r in np.arange(rows)], 
                                subplot_titles=titles,
                                horizontal_spacing=0.0,
                                vertical_spacing=0.05)

    # Make multiple plots
    #** linemap or tilemap? Example of use?
    # This would be a linemap since the method that depends on this is add_scattergeo() which is listed as a linemap.
    # See migration_prediction.py in anthro-example2 for an example of use.
    def make_scattergeo_subplots(self, rows, cols, titles):
        self.rowCount = rows
        self.colCount = cols
        self.fig = make_subplots(rows=rows, 
                                cols=cols, 
                                specs = [[{'type': 'scattergeo'} for c in np.arange(cols)] for r in np.arange(rows)], 
                                subplot_titles=titles,
                                horizontal_spacing=0.0,
                                vertical_spacing=0.05)

    # Use a world map with physical features outlined
    #** Can you write an example?
    # This method is really just used to style a linemap_points() map.
    # See migration_sol.py in anthro-example2 to see an examlple of this style of map.
    def physical_features_map(self):
        self.fig.update_geos(
            resolution=50,
            showcoastlines=True, coastlinecolor='RebeccaPurple',
            showland=True,
            showocean=True, oceancolor='LightBlue',
            showlakes=True, lakecolor='Blue',
            showrivers=True, rivercolor='Blue'
        ) 

    # Sets linemaps to show country borders
    def show_countries(self):
        self.fig.update_geos(
            showcountries = True
        )


    # Adds location to a map
    #** Example?
    # locations = ['USA', 'CHN', 'RUS', 'DEU', 'GBR']
    # data = ['1', '2', '3', '4', '5']
    # for loc in locations:
    #     dt.add_map_location(loc)
    # for d in data:
    #     dt.add_map_data(d)
    # dt.plot_choro_map()
    def add_map_location(self, location):
        self.cusmapl.append(location)

    # Adds data to a map 
    #** Example?
    # locations = ['USA', 'CHN', 'RUS', 'DEU', 'GBR']
    # data = ['1', '2', '3', '4', '5']
    # for loc in locations:
    #     dt.add_map_location(loc)
    # for d in data:
    #     dt.add_map_data(d)
    # dt.plot_choro_map()
    def add_map_data(self, data):
        self.cusmapd.append(data)



    # Takes ISO3 country code column name, and adds a continent column
    #** Can you write an example?
    # See add_continents.py. I added continent-codes.csv which is needed for this to work. Also replace the file name with your own path in add_continents.py
    def add_continents(self, code, file_name):
        self.path += file_name
        continents = pd.read_csv('continent-codes.csv')
        continent_dict = dict(zip(continents.Three_Letter_Country_Code, continents.Continent_Name))
        self.data['continents'] = self.data[code].map(continent_dict)
        self.data.to_csv(self.path)


#####################################################################
#####################################################################
# TILE MAPS

    #Sets the column names for scatter plot in order to draw lines
    #** Changed from set_lat_lon_color_col()
    def tilemap_attach_col_lat_long(self, lat, lon, data_col=None):
        self.latcolname = lat
        self.loncolname = lon
        self.ccolname = data_col

    #** Added simplified version 
    def tilemap(self):
        self.tilemap_detailed(None, None, center=dict(lat=0,lon=0), zoom=0, title=None)

    #** Added one more simple version
    def tilemap_czt(self, center, zoom, title):
        self.tilemap_detailed(None, None, center=center, zoom=zoom, title=title)

    # The detailed version with all the parameters.
    def tilemap_detailed(self, hover_name, hover_data, center, zoom, title):
   	    self.fig = px.scatter_mapbox(self.data,
                    lat = self.latcolname,
                    lon = self.loncolname,
                    color = self.ccolname,
                    hover_name = hover_name,
                    hover_data = hover_data,
                    center = center,
                    title = title,
                    mapbox_style = 'open-street-map',
                    zoom = zoom,
                    color_discrete_sequence = px.colors.qualitative.Light24)


    # Adds a line to a scattermap
    def tilemap_add_line(self, lat0, lon0, lat1, lon1):
        self.scatlat = np.linspace(lat0, lat1, 500)
        self.scatlon = np.linspace(lon0, lon1, 500)
        for x in range(len(self.scatlat)):
            self.data = self.data.append({self.latcolname: self.scatlat.item(x), self.loncolname: self.scatlon.item(x), self.ccolname: 'Line'}, ignore_index=True)



#####################################################################
#####################################################################
# NETWORKS


    #Creates an empty graph with specified total_nodes
    # def create_empty_graph(self):
    #     self.G = nx.Graph()

    # #Adds a Node to G
    # def add_node(self, node):
    #     self.G.add_node(node)

    # #Adds a Node to G
    # def add_node_amount(self, amount):
    #     for i in range(amount):
    #         self.G.add_node(i)

    # #Add edges to G
    # def add_edge(self, x1, x2):
    #     self.G.add_edge(x1, x2)

    # #Add edges from Datafame
    # def add_edge_data(self, x1, x2):
    #     A = list(self.data[x1].unique())
    #     B = list(self.data[x2].unique())
    #     for i,j in self.data.iterrows():
    #         self.G.add_edges_from([(j[x1], j[x2])])
    # #Draws Edges
    # def draw_graph(self, title):
    #     #Position nodes using Fruchterman-Reingold force-directed algorithm.
    #     pos = nx.spring_layout(self.G, k=0.5, iterations=50)
    #     for n, p in pos.items():
    #         self.G.nodes[n]['pos'] = p
    #     #Draw Edges
    #     edge_trace = go.Scatter(
    #         x=[],
    #         y=[],
    #         line=dict(width=0.5,color='#888'),
    #         hoverinfo='none',
    #         mode='lines')
    #     #Set scatter plot line locations
    #     for edge in self.G.edges():
    #         x0, y0 = self.G.nodes[edge[0]]['pos']
    #         x1, y1 = self.G.nodes[edge[1]]['pos']
    #         edge_trace['x'] += tuple([x0, x1, None])
    #         edge_trace['y'] += tuple([y0, y1, None])
    #     #Draw Nodes
    #     node_trace = go.Scatter(
    #         x=[],
    #         y=[],
    #         text=[],
    #         mode='markers',
    #         hoverinfo='text',
    #         marker=dict(
    #             showscale=True,
    #             colorscale='RdBu',
    #             reversescale=True,
    #             color=[],
    #             size=15,
    #             colorbar=dict(
    #                 thickness=10,
    #                 title='Node Connections',
    #                 xanchor='left',
    #                 titleside='right'
    #             ),
    #             line=dict(width=0)))
    #     #Set scatter plot node locations
    #     for node in self.G.nodes():
    #         x, y = self.G.nodes[node]['pos']
    #         node_trace['x'] += tuple([x])
    #         node_trace['y'] += tuple([y])
    #     #Color Nodes
    #     for node, adjacencies in enumerate(self.G.adjacency()):
    #         node_trace['marker']['color']+=tuple([len(adjacencies[1])])
    #         node_info = str(adjacencies[0]) + ' # of connections: '+str(len(adjacencies[1]))
    #         node_trace['text']+=tuple([node_info])
    #     #Draw the Network
    #     self.fig = go.Figure(data=[edge_trace, node_trace],
    #          layout=go.Layout(
    #             title=title,
    #             titlefont=dict(size=16),
    #             showlegend=False,
    #             hovermode='closest',
    #             margin=dict(b=20,l=5,r=5,t=40),
    #             xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    #             yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
