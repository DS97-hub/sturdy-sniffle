# Display the output
Print('New Python file')
get_ipython().system('pip3 install folium')
get_ipython().system('pip3 install wget')
After completed the above tasks, you should be able to find some geographical patterns about launch sites.

Let's first import required Python packages for this lab:

get_ipython().system('pip3 install folium')
get_ipython().system('pip3 install wget')
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
Cell In[16], line 1
----> 1 get_ipython().system('pip3 install folium')
      2 get_ipython().system('pip3 install wget')

File /lib/python3.10/site-packages/IPython/core/interactiveshell.py:2590, in InteractiveShell.system_piped(self, cmd)
   2585     raise OSError("Background processes not supported.")
   2587 # we explicitly do NOT return the subprocess status code, because
   2588 # a non-None value would trigger :func:`sys.displayhook` calls.
   2589 # Instead, we store the exit_code in user_ns.
-> 2590 self.user_ns['_exit_code'] = system(self.var_expand(cmd, depth=1))

File /lib/python3.10/site-packages/IPython/utils/_process_posix.py:129, in ProcessHandler.system(self, cmd)
    125 enc = DEFAULT_ENCODING
    127 # Patterns to match on the output, for pexpect.  We read input and
    128 # allow either a short timeout or EOF
--> 129 patterns = [pexpect.TIMEOUT, pexpect.EOF]
    130 # the index of the EOF pattern in the list.
    131 # even though we know it's 1, this call means we don't have to worry if
    132 # we change the above list, and forget to change this value:
    133 EOF_index = patterns.index(pexpect.EOF)

AttributeError: module 'pexpect' has no attribute 'TIMEOUT'
import folium
import wget
import pandas as pd
---------------------------------------------------------------------------
ModuleNotFoundError                       Traceback (most recent call last)
Cell In[9], line 1
----> 1 import folium
      2 import wget
      3 import pandas as pd

ModuleNotFoundError: No module named 'folium'
# Import folium MarkerCluster plugin
from folium.plugins import MarkerCluster
# Import folium MousePosition plugin
from folium.plugins import MousePosition
# Import folium DivIcon plugin
from folium.features import DivIcon
---------------------------------------------------------------------------
ModuleNotFoundError                       Traceback (most recent call last)
Cell In[10], line 2
      1 # Import folium MarkerCluster plugin
----> 2 from folium.plugins import MarkerCluster
      3 # Import folium MousePosition plugin
      4 from folium.plugins import MousePosition

ModuleNotFoundError: No module named 'folium'
If you need to refresh your memory about folium, you may download and refer to this previous folium lab:

Generating Maps with Python

## Task 1: Mark all launch sites on a map
# Download and read the `spacex_launch_geo.csv`
​
​
url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv'
response = requests.get(url)
spacex_df = pd.read_csv(io.StringIO(response.text))
​
---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
Cell In[4], line 6
      1 ## Task 1: Mark all launch sites on a map
      2 # Download and read the `spacex_launch_geo.csv`
      5 url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv'
----> 6 response = requests.get(url)
      7 spacex_df = pd.read_csv(io.StringIO(response.text))

NameError: name 'requests' is not defined
First, let's try to add each site's location on a map using site's latitude and longitude coordinates

The following dataset with the name spacex_launch_geo.csv is an augmented dataset with latitude and longitude added for each site.

# Download and read the `spacex_launch_geo.csv`
from js import fetch
import io
​
URL = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv'
resp = await fetch(URL)
spacex_csv_file = io.BytesIO((await resp.arrayBuffer()).to_py())
spacex_df=pd.read_csv(spacex_csv_file)
---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
Cell In[18], line 8
      6 resp = await fetch(URL)
      7 spacex_csv_file = io.BytesIO((await resp.arrayBuffer()).to_py())
----> 8 spacex_df=pd.read_csv(spacex_csv_file)

NameError: name 'pd' is not defined
Now, you can take a look at what are the coordinates for each site.

# Select relevant sub-columns: `Launch Site`, `Lat(Latitude)`, `Long(Longitude)`, `class`
spacex_df = spacex_df[['Launch Site', 'Lat', 'Long', 'class']]
launch_sites_df = spacex_df.groupby(['Launch Site'], as_index=False).first()
launch_sites_df = launch_sites_df[['Launch Site', 'Lat', 'Long']]
launch_sites_df
---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
Cell In[17], line 2
      1 # Select relevant sub-columns: `Launch Site`, `Lat(Latitude)`, `Long(Longitude)`, `class`
----> 2 spacex_df = spacex_df[['Launch Site', 'Lat', 'Long', 'class']]
      3 launch_sites_df = spacex_df.groupby(['Launch Site'], as_index=False).first()
      4 launch_sites_df = launch_sites_df[['Launch Site', 'Lat', 'Long']]

NameError: name 'spacex_df' is not defined
Above coordinates are just plain numbers that can not give you any intuitive insights about where are those launch sites. If you are very good at geography, you can interpret those numbers directly in your mind. If not, that's fine too. Let's visualize those locations by pinning them on a map.

We first need to create a folium Map object, with an initial center location to be NASA Johnson Space Center at Houston, Texas.

# Start location is NASA Johnson Space Center
nasa_coordinate = [29.559684888503615, -95.0830971930759]
site_map = folium.Map(location=nasa_coordinate, zoom_start=10)
We could use folium.Circle to add a highlighted circle area with a text label on a specific coordinate. For example,

# Create a blue circle at NASA Johnson Space Center's coordinate with a popup label showing its name
circle = folium.Circle(nasa_coordinate, radius=1000, color='#d35400', fill=True).add_child(folium.Popup('NASA Johnson Space Center'))
# Create a blue circle at NASA Johnson Space Center's coordinate with a icon showing its name
marker = folium.map.Marker(
    nasa_coordinate,
    # Create an icon as a text label
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % 'NASA JSC',
        )
    )
site_map.add_child(circle)
site_map.add_child(marker)
Make this Notebook Trusted to load map: File -> Trust Notebook
and you should find a small yellow circle near the city of Houston and you can zoom-in to see a larger circle.

Now, let's add a circle for each launch site in data frame launch_sites

TODO: Create and add folium.Circle and folium.Marker for each launch site on the site map

An example of folium.Circle:

folium.Circle(coordinate, radius=1000, color='#000000', fill=True).add_child(folium.Popup(...))

An example of folium.Marker:

folium.map.Marker(coordinate, icon=DivIcon(icon_size=(20,20),icon_anchor=(0,0), html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % 'label', ))

# Initial the map
nasa_coordinate = [28.562302,-80.577356]
site_map = folium.Map(location=nasa_coordinate, zoom_start=5)
# For each launch site, add a Circle object based on its coordinate (Lat, Long) values. In addition, add Launch site name as a popup label
circle = folium.Circle(nasa_coordinate, radius=1000, color='#d35400', fill=True).add_child(folium.Popup('CCAFS LC-40'))
marker = folium.map.Marker(
    nasa_coordinate,
    # Create an icon as a text label
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % 'CCAFS LC-40',
        )
    )
site_map.add_child(circle)
site_map.add_child(marker)
Make this Notebook Trusted to load map: File -> Trust Notebook
The generated map with marked launch sites should look similar to the following:

Image
Now, you can explore the map by zoom-in/out the marked areas , and try to answer the following questions:

Are all launch sites in proximity to the Equator line?
Are all launch sites in very close proximity to the coast?
Also please try to explain your findings.

# Task 2: Mark the success/failed launches for each site on the map
spacex_df.tail(10)
Launch Site	Lat	Long	class
46	KSC LC-39A	28.573255	-80.646895	1
47	KSC LC-39A	28.573255	-80.646895	1
48	KSC LC-39A	28.573255	-80.646895	1
49	CCAFS SLC-40	28.563197	-80.576820	1
50	CCAFS SLC-40	28.563197	-80.576820	1
51	CCAFS SLC-40	28.563197	-80.576820	0
52	CCAFS SLC-40	28.563197	-80.576820	0
53	CCAFS SLC-40	28.563197	-80.576820	0
54	CCAFS SLC-40	28.563197	-80.576820	1
55	CCAFS SLC-40	28.563197	-80.576820	0
Next, let's try to enhance the map by adding the launch outcomes for each site, and see which sites have high success rates. Recall that data frame spacex_df has detailed launch records, and the class column indicates if this launch was successful or not

spacex_df.tail(10)
Next, let's create markers for all launch records. If a launch was successful (class=1), then we use a green marker and if a launch was failed, we use a red marker (class=0)

Note that a launch only happens in one of the four launch sites, which means many launch records will have the exact same coordinate. Marker clusters can be a good way to simplify a map containing many markers having the same coordinate.

Let's first create a MarkerCluster object

marker_cluster = MarkerCluster()
​
TODO: Create a new column in launch_sites dataframe called marker_color to store the marker colors based on the class value

​
# Apply a function to check the value of `class` column
# If class=1, marker_color value will be green
# If class=0, marker_color value will be red
​
​
​
ef assign_marker_color(launch_outcome):
    if launch_outcome == 1:
        return 'green'
    else:
        return 'red'
    
spacex_df['marker_color'] = spacex_df['class'].apply(lambda x: 'red' if x == 0 else 'green')
spacex_df.tail(10)
  Cell In[28], line 7
    ef assign_marker_color(launch_outcome):
       ^
SyntaxError: invalid syntax
TODO: For each launch result in spacex_df data frame, add a folium.Marker to marker_cluster

# Add marker_cluster to current site_map
site_map.add_child(marker_cluster)
​
# for each row in spacex_df data frame
# create a Marker object with its coordinate
# and customize the Marker's icon property to indicate if this launch was successed or failed, 
# e.g., icon=folium.Icon(color='white', icon_color=row['marker_color']
for index, record in spacex_df.iterrows():
    # TODO: Create and add a Marker cluster to the site map
    # marker = folium.Marker(...)
    marker_cluster.add_child(marker)
​
site_map
Your updated map may look like the following screenshots:

Image
Image
From the color-labeled markers in marker clusters, you should be able to easily identify which launch sites have relatively high success rates.

# TASK 3: Calculate the distances between a launch site to its proximities
# Add Mouse Position to get the coordinate (Lat, Long) for a mouse over on the map
formatter = "function(num) {return L.Util.formatNum(num, 5);};"
mouse_position = MousePosition(
    position='topright',
    separator=' Long: ',
    empty_string='NaN',
    lng_first=False,
    num_digits=20,
    prefix='Lat:',
    lat_formatter=formatter,
    lng_formatter=formatter,
)
​
site_map.add_child(mouse_position)
site_map
---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
Cell In[11], line 4
      1 # TASK 3: Calculate the distances between a launch site to its proximities
      2 # Add Mouse Position to get the coordinate (Lat, Long) for a mouse over on the map
      3 formatter = "function(num) {return L.Util.formatNum(num, 5);};"
----> 4 mouse_position = MousePosition(
      5     position='topright',
      6     separator=' Long: ',
      7     empty_string='NaN',
      8     lng_first=False,
      9     num_digits=20,
     10     prefix='Lat:',
     11     lat_formatter=formatter,
     12     lng_formatter=formatter,
     13 )
     15 site_map.add_child(mouse_position)
     16 site_map

NameError: name 'MousePosition' is not defined
Next, we need to explore and analyze the proximities of launch sites.

Let's first add a MousePosition on the map to get coordinate for a mouse over a point on the map. As such, while you are exploring the map, you can easily find the coordinates of any points of interests (such as railway)

# Add Mouse Position to get the coordinate (Lat, Long) for a mouse over on the map
from math import sin, cos, sqrt, atan2, radians
​
def calculate_distance(lat1, lon1, lat2, lon2):
    # approximate radius of earth in km
    R = 6373.0
​
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
​
    dlon = lon2 - lon1
    dlat = lat2 - lat1
​
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
​
    distance = R * c
    return distancedd_child(mouse_position)
site_map
---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
Cell In[12], line 21
     19     distance = R * c
     20     return distancedd_child(mouse_position)
---> 21 site_map

NameError: name 'site_map' is not defined
Now zoom in to a launch site and explore its proximity to see if you can easily find any railway, highway, coastline, etc. Move your mouse to these points and mark down their coordinates (shown on the top-left) in order to the distance to the launch site.

Now zoom in to a launch site and explore its proximity to see if you can easily find any railway, highway, coastline, etc. Move your mouse to these points and mark down their coordinates (shown on the top-left) in order to the distance to the launch site.

launch_site_lat = 28.563197
launch_site_lon = -80.576820
coastline_lat = 28.56334
coastline_lon = -80.56789
launchsite_coordinates = [launch_site_lat, launch_site_lon]
coastline_coordinates = [coastline_lat, coastline_lon]
distance_coastline = calculate_distance(launch_site_lat, launch_site_lon, coastline_lat, coastline_lon)
print(distance_coastline,' km')
---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
Cell In[13], line 7
      5 launchsite_coordinates = [launch_site_lat, launch_site_lon]
      6 coastline_coordinates = [coastline_lat, coastline_lon]
----> 7 distance_coastline = calculate_distance(launch_site_lat, launch_site_lon, coastline_lat, coastline_lon)
      8 print(distance_coastline,' km')

Cell In[12], line 20, in calculate_distance(lat1, lon1, lat2, lon2)
     17 c = 2 * atan2(sqrt(a), sqrt(1 - a))
     19 distance = R * c
---> 20 return distancedd_child(mouse_position)

NameError: name 'distancedd_child' is not defined
TODO: Mark down a point on the closest coastline using MousePosition and calculate the distance between the coastline point and the launch site.

​
# Create and add a folium.Marker on your selected closest coastline point on the map
# Display the distance between coastline point and launch site using the icon property 
# for example
# distance_marker = folium.Marker(
#    coordinate,
#    icon=DivIcon(
#        icon_size=(20,20),
#        icon_anchor=(0,0),
#        html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % "{:10.2f} KM".format(distance),
#        )
#    )
distance_marker = folium.Marker(
                    coastline_coordinates,
                    icon=DivIcon(
                    icon_size=(20,20),
                    icon_anchor=(0,0),
                    html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % "{:10.2f} KM".format(distance_coastline),
                    )
)
site_map.add_child(distance_marker)
---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
Cell In[36], line 12
      1 # Create and add a folium.Marker on your selected closest coastline point on the map
      2 # Display the distance between coastline point and launch site using the icon property 
      3 # for example
   (...)
     10 #        )
     11 #    )
---> 12 distance_marker = folium.Marker(
     13                     coastline_coordinates,
     14                     icon=DivIcon(
     15                     icon_size=(20,20),
     16                     icon_anchor=(0,0),
     17                     html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % "{:10.2f} KM".format(distance_coastline),
     18                     )
     19 )
     20 site_map.add_child(distance_marker)

NameError: name 'folium' is not defined
# Create and add a folium.Marker on your selected closest coastline point on the map
# Display the distance between coastline point and launch site using the icon property 
# for example
# distance_marker = folium.Marker(
#    coordinate,
#    icon=DivIcon(
#        icon_size=(20,20),
#        icon_anchor=(0,0),
#        html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % "{:10.2f} KM".format(distance),
#        )
#    )
​
coordinates = [
    [28.56342, -80.57674],
    [28.56342, -80.56756]]
​
lines=folium.PolyLine(locations=coordinates, weight=1)
site_map.add_child(lines)
distance = calculate_distance(coordinates[0][0], coordinates[0][1], coordinates[1][0], coordinates[1][1])
distance_circle = folium.Marker(
    [28.56342, -80.56794],
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % "{:10.2f} KM".format(distance),
        )
    )
site_map.add_child(distance_circle)
site_map
---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
Cell In[37], line 17
      1 # Create and add a folium.Marker on your selected closest coastline point on the map
      2 # Display the distance between coastline point and launch site using the icon property 
      3 # for example
   (...)
     10 #        )
     11 #    )
     13 coordinates = [
     14     [28.56342, -80.57674],
     15     [28.56342, -80.56756]]
---> 17 lines=folium.PolyLine(locations=coordinates, weight=1)
     18 site_map.add_child(lines)
     19 distance = calculate_distance(coordinates[0][0], coordinates[0][1], coordinates[1][0], coordinates[1][1])

NameError: name 'folium' is not defined
TODO: Draw a PolyLine between a launch site to the selected coastline point

# Create a `folium.PolyLine` object using the coastline coordinates and launch site coordinate
# lines=folium.PolyLine(locations=coordinates, weight=1)
​
coordinates = [launchsite_coordinates, coastline_coordinates]
lines=folium.PolyLine(locations=coordinates, weight=1)
site_map.add_child(lines)
site_map
---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
Cell In[38], line 5
      1 # Create a `folium.PolyLine` object using the coastline coordinates and launch site coordinate
      2 # lines=folium.PolyLine(locations=coordinates, weight=1)
      4 coordinates = [launchsite_coordinates, coastline_coordinates]
----> 5 lines=folium.PolyLine(locations=coordinates, weight=1)
      6 site_map.add_child(lines)
      7 site_map

NameError: name 'folium' is not defined
Your updated map with distance line should look like the following screenshot:

Image
TODO: Similarly, you can draw a line betwee a launch site to its closest city, railway, highway, etc. You need to use MousePosition to find the their coordinates on the map first

A railway map symbol may look like this:

Image
A highway map symbol may look like this:

Image
A city map symbol may look like this:

Image
# Create a marker with distance to a closest city, railway, highway, etc.
# Draw a line between the marker to the launch site
​
def distance_and_line(destination_coordinates):
    # Create a marker with distance to a closest city, railway, highway, etc.
    # Draw a line between the marker to the launch site
    
    #calculate the distance between the chosen destination and the launch site defined previously, using the calculate_distance function 
    distance_to_destination = calculate_distance(launch_site_lat, launch_site_lon, destination_coordinates[0], destination_coordinates[1])
    
    
    #define the distance marker (which will be shown at the chosen destination)
    distance_marker = folium.Marker(
        destination_coordinates,
        icon=DivIcon(
            icon_size=(20,20),
            icon_anchor=(0,0),
            html='<div style="font-size: 12; color:#ff5c33;"><b>%s</b></div>' % "{:10.2f} KM".format(distance_to_destination),
            )
        )
​
    #define the distance line (between the chosen destination and the launch site)
    distance_line=folium.PolyLine(
        locations=[launchsite_coordinates, destination_coordinates],
        weight=1
    )
​
    #add the distance marker to the map 
    site_map.add_child(distance_marker)
    #add the distance line to the map 
    site_map.add_child(distance_line)
closest_city_coordinates = [28.10106, -80.6369]
closest_railway_coordinates = [28.57209, -80.58528]
closest_highway_coordinates = [28.56333, -80.57079]
​
#add distance markers and lines for closest city, railway and highway, using the above function
distance_and_line(closest_city_coordinates)
distance_and_line(closest_railway_coordinates)
distance_and_line(closest_highway_coordinates)
​
#show the map
site_map
---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
Cell In[40], line 6
      3 closest_highway_coordinates = [28.56333, -80.57079]
      5 #add distance markers and lines for closest city, railway and highway, using the above function
----> 6 distance_and_line(closest_city_coordinates)
      7 distance_and_line(closest_railway_coordinates)
      8 distance_and_line(closest_highway_coordinates)

Cell In[39], line 9, in distance_and_line(destination_coordinates)
      4 def distance_and_line(destination_coordinates):
      5     # Create a marker with distance to a closest city, railway, highway, etc.
      6     # Draw a line between the marker to the launch site
      7     
      8     #calculate the distance between the chosen destination and the launch site defined previously, using the calculate_distance function 
----> 9     distance_to_destination = calculate_distance(launch_site_lat, launch_site_lon, destination_coordinates[0], destination_coordinates[1])
     12     #define the distance marker (which will be shown at the chosen destination)
     13     distance_marker = folium.Marker(
     14         destination_coordinates,
     15         icon=DivIcon(
   (...)
     19             )
     20         )

Cell In[34], line 20, in calculate_distance(lat1, lon1, lat2, lon2)
     17 c = 2 * atan2(sqrt(a), sqrt(1 - a))
     19 distance = R * c
---> 20 return distancedd_child(mouse_position)

NameError: name 'distancedd_child' is not defined
