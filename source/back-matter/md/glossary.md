---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.16.7
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

<!-- #region editable=true slideshow={"slide_type": ""} -->
# Glossary

```{glossary}
Accessor
  In Python libraries, an *accessor* is a method or attribute added to an existing data structure, such as a `Dataset` in `xarray` library, to provide specialized functionality. Accessors extend the capabilities of the base object without modifying its core structure.

Application Programming Interface
  An application programming interface or API is a set of protocols and tools that enable pieces of software to communicate and exchange information. For example, the Nominatim service has an API for accessing its geocoding service.

API
  See {term}`Application Programming Interface`.

Argument
  The value passed to a function when it is called. Similar to a {term}`parameter`.

Aspect
  Aspect shows the (compass) direction that a slope faces, derived from elevation data. It is usually measured in degrees from 0° (north) to 360°.

Assertion
  A statement used in a Python program to check whether a given condition evaluates as `True` when the code is executed. When the condition is not `True`, an `AssertionError` is raised. Assertions are typically used for debugging and testing code.

Binary predicate
  See {term}`Spatial predicate`.

Camel case
  A variable naming convention in which words are joined without spaces by capitalizing the first letter of each word that follows the first. For example, `gpsStationId`.

Collection
  A group of data types known as containers, where multiple values can be stored together. The built-in container data types in Python are dictionary, list, set, and tuple.

Computer
  We use the definition of a computer given by {cite}`Zelle2017`: "A machine that stores and manipulates information under the control of a changeable program."
  
Coordinate Reference System
  A coordinate reference system (CRS) described how the coordinates or geometries are related to the places on Earth. It typically includes a set of geographic or projected coordinates and a mathematical model that describes the shape of the Earth and the relationship between the coordinates and their positions on the Earth's surface. A CRS is used to locate positions accurately and to enable the exchange of geographic data between different systems and applications.
  
Coordinate transformation
  See {term}`Map reprojection`.

Cost surface
  A cost surface is a raster representation used in map algebra in which each cell value indicates the cost (e.g., time, energy, money, or difficulty) required to traverse that cell. Cost surfaces are used in spatial analysis to model and calculate the least-cost path or accumulated cost between locations, factoring in terrain, land use, or other impedance variables. Cost surfaces are essential in applications such as route optimization, habitat connectivity, and emergency response planning.

Curvature
  Curvature describes how fast the slope is increasing or decreasing as we move along a surface. A positive curvature means the surface is curving up (upwardly convex) at that cell. A negative curvature means the surface is curving down (downwardly convex) at that cell.

DataFrame
  In pandas library, a DataFrame is a two-dimensional, tabular data structure with labeled rows and columns, similar to an Excel spreadsheet or SQL table. Each column can store data of different types (e.g., integers, floats, strings), and the DataFrame provides methods for data manipulation, including filtering, aggregation, and merging. It is one of the core data structures in pandas, widely used for data analysis and manipulation in Python.
  
Data model
  A data model is an conceptual (abstract) model that shows how elements of data are organized and how they relate to one another in a standardized manner and how the data relate to properties of real-world entities. Examples of data models are e.g. vector data model consisting of points, lines and areas; and raster data model constituted of a grid-like structure that hold the values for each grid cell.    

Data type
  An attribute defining the characteristics of a value in a program.
  For example, type `int` is an integer (whole number).
  
DateOffset
  A specific `pandas` object that represents a duration of time using calendar duration standards, such as a week ("W"). 
  
DatetimeIndex
  An immutable array of datetime64 data that is specified as the index of the DataFrame. Can be used for indexing and grouping data based on time.

DE-9IM
  See {term}`Dimensionally Extended 9-Intersection Model`.

Decimal degrees
  A decimal degree is a method of expressing latitude and longitude geographic coordinates as decimal fractions instead of degrees, minutes, and seconds. It represents the angle between a point on the earth's surface and the equator or prime meridian, respectively, in units of decimal degrees. Decimal degrees provide a more convenient representation of geographic coordinates and make it easier to perform calculations with them.

Delanay Triangulation
  Delaunay triangulation is a way of dividing a set of points into non-overlapping triangles (in 2D) or tetrahedra (in 3D) such that no point lies inside the circumcircle of any triangle. Delanay triangulation is widely used e.g. in interpolation and computer graphics for creating structured meshes from unstructured points.
  
Dependency
  Python packages are often linked to other Python libraries. These other packages (i.e. dependencies) are typically needed to be installed for a given Python package to work. 

Dictionary
  A built-in Python data structure comprising one or more unique "keys" and associated "values". Dictionary keys can be used to access associated values within a dictionary, and keys are typically numbers or character strings. Python dictionaries are enclosed in curly braces (`{` `}`) and dictionary items are listed in the form `key: value` separated by commas.

Dimensionally Extended 9-Intersection Model 
  Dimensionally Extended 9-Intersection Model (DE-9IM) is a fundamental framework in GIS used for describing and analyzing spatial relationships between geometric objects. DE-9IM provides a matrix-based approach where the rows and columns represent the interior, boundary, and exterior of two geometric shapes being compared. By examining the intersections of these parts, a detailed characterization of their spatial relationship can be achieved, including spatial predicates such as "touches", "overlaps", and "contains".  

Docstring
  A text string used to document a section of code. Docstrings are frequently used for functions to describe what the function does as well as providing information about input parameters and function outputs. You are encouraged to create docstrings when making functions as they can be used with the Python help function to show users how functions work.

Edge effect
  Edge effect is spatial distortion (bias) that occurs at the boundaries of a geographic datasets (raster and vector), often due to incomplete data or the influence of neighboring areas not included in the analysis. It can affect the accuracy of calculations like filtering, classification, or spatial modeling near the dataset's edges.

EPSG code
  An EPSG code is a unique identifier assigned to a specific coordinate reference system (CRS) or a spatial data transformation standard, as defined by the EPSG (European Petroleum Survey Group) registry. These codes, such as 4326 for WGS84 or 3857 for Web Mercator, simplify the process of referencing CRSs in geographic data processing.

Fork
  A personal copy of a GitHub repository that is linked to a user's GitHub account. Forks can be used to modify files without affecting the original repository and also allow users to see how the original repository has changed since the fork was created.

Function
  A reusable piece of code that performs a single action.
  
Geocoding
  The process of converting addresses to coordinates / points, or vice versa (called reverse-geocoding). Also see {term}`Georeferencing`.

GeoDataFrame
  GeoDataFrame in geopandas library is similar to pandas {term}`DataFrame` but designed to handle geospatial data. Each row in a GeoDataFrame represents a geometric object (e.g., point, line, polygon) with associated attributes. `GeoDataFrame` bundles various methods that support spatial operations like geometric calculations and spatial joins, making it essential for geospatial analysis in Python.
  
Geographic coordinate conversion
  See {term}`Map reprojection`.
  
Georeferencing
  Attaching information about a location to a piece of information is commonly referred as georeferencing, geolocating or geocoding. For example a postal address can be used to specify a location of a place with relatively high spatial accuracy at a level of door/mailbox. 

GeoSeries
  GeoSeries is used to store geospatial data, where each element is a geometric object like a point, line, or polygon. It extends the pandas {term}`Series` by supporting spatial operations, such as geometric transformations and spatial queries. A GeoSeries is often used to represent the geometry column in a {term}`GeoDataFrame`, making it a fundamental building block for geospatial analysis in Python.

Git
  A free and open-source distributed {term}`version control` system that tracks changes in {term}`source code`. Git allows multiple users to work on a project at the same time while maintaining a complete version history. Developed by Linus Torvalds.

Git branch
  An parallel copy of files in a Git repository starting from a specific snapshot that allows for independent development without affecting the original files from which the branch was created. Branches can be useful for adding new features or experimenting without worrying that the changes will affect the original files or code functionality.

Git clone
  The command in {term}`Git` used to create a copy of an existing {term}`repository`. Cloning downloads the files, commit history, and branches from the repository.

Git commit
  Verb: The process of writing or {term}`merging <Git merge>` changes made in the working copy of files in a {term}`repository{term}` of a {term}`version control` system. Noun: A specific instance of changes to files in a {term}`repository` of a {term}`version control` system. Each commit includes a unique ID and a message describing the changes. Similar to {term}`revision` and {term}`version`.

Git merge
  The command in {term}`Git` used to integrate changes from multiple {term}`commits <Git commit>` or branches. Merging combines commit histories and preserves changes both branches. If changes have been made to the same sections of the same file, merging may result in a merge conflict.

Git merge conflict
  A situation in which Git cannot automatically combine changes from different commits or branches because similar sections of the same files have been modified. This could occur in GitHub if you change similar sections of the same file locally and directly on GitHub. In such cases, the conflict must be resolved manually by editing together the changes and making a new commit.

Git pull
  The command in {term}`Git` used to fetch updates from a remote {term}`repository` and merge them into the current branch. Pulling ensures the local repository is up to date with the latest changes in the remote repository.

Git push
  The command in {term}`Git` used to upload local {term}`commits <Git commit>` to a remote {term}`repository`. Pushing makes the latest changes available to others with access to the repository.

Git remote
  A reference to a repository stored on a server or hosting service like GitHub. Remotes are often useful for keeping project files in sync when multiple users are working in the same code repository.

GitHub
  An online platform for collaborative development of {term}`software` based around the {term}`Git` {term}`version control` system. GitHub provides tools for collaboration, version control, issue tracking, and code review.

Hillshade
  A hillshade is a grayscale 3D-like representation of the terrain surface, created by simulating the effect of sunlight shining across the landscape. In GIS, hillshading is derived from a Digital Elevation Model (DEM) and is used to visualize topographic relief. The shading is based on specified azimuth (direction) and altitude (angle) of the light source, typically representing the sun.

Hypsometric curve
  The distribution of area above a given elevation in an region analyzed using hypsometric analysis. This is effectively a cumulative distribution of area as a function of elevation. The areas and elevations in hypsometric curves are frequently normalized to allow comparison between regions and for calculating a {term}`hypsometric integral`.

Hypsometric integral
  The area under a {term}`hypsometric curve`. This value can be used as a metric of the volume of rock and/or soil that has been removed from a given region such as a watershed.

Hypsometry
  The measurement of the distribution of elevations of Earth's (or other planet's) surface elevations within a specified area. Also known as hypsometric analysis.

IDE
  See {term}`Integrated Development Environment`.

Immutable
  A data type that can be modified after being defined. In reality, things are a bit more complicated, but this is sufficient for our purposes. Opposite of {term}`Mutable`.

Index
  A number indicating the location of a specific value stored in Python lists or tuples. The first index value of list is always 0.

Inner join
  The inner join results in a DataFrame that contains only the rows with matching keys (or binary/spatial predicate) in both original (Geo)DataFrames, excluding all rows in either (Geo)DataFrame that do not have a match in the other. The match can be based on a common key that can be found in both DataFrames (as in table join) or on a spatial predicate in case the data is merged based on the spatial relationship between two spatial data layers.
  
Integrated Development Environment
  An integrated development environment or IDE is a software program or package that provides a set of tools for writing, testing, and debugging software in a convenient, practical interface.

Interpolation
  Estimation of a value based on the known values in a data set. For example, an estimate of the mean daily temperature can be calculated from the average of the minimum and maximum temperatures that day.

Interpreter
  An interpreter is a computer program that is used to execute program instructions written in Python (or other languages). The interpreter reads your statements of code and based on these instructions actually does the work that has been assigned to it. 

Jupyter Notebook
  A web application that allows users to combine rich-formtted text with code cells in an interactive document. Jupyter Notebooks can contain nicely formatted text, equations, images, interactive visualizations, and more. More information can be found at <https://jupyter.org/>.

KD-Tree
  A KD-Tree, or K-dimensional tree, is a space-partitioning data structure for organizing points in a k-dimensional space. KD-Trees are useful for making specific search tasks faster and more efficient, such as nearest neighbor search. The structure recursively divides the space into two half-spaces at each level, using one dimension at each step. This division is typically done by selecting a median value along one dimension to split the dataset, creating a binary tree. KD-Trees enable efficient querying of the space, such as finding points within a given range or nearest to a specific point, by significantly reducing the number of comparisons needed to locate them.

K-Nearest Neighbor search
  K-Nearest Neighbor (KNN) search is a type of algorithm used to find the "k" closest points (or neighbors) to a given query point in a dataset. In the context of spatial data, KNN search can identify the nearest geographical features based on their spatial coordinates. The algorithm calculates distances between the query point and all points in the dataset, then selects the "k" smallest distances to determine the nearest neighbors. 

Left outer join
  A left outer join includes all the rows from the left (Geo)DataFrame and those rows from the right (Geo)DataFrame that have a matching key in the table, or that intersect or match based on the specified spatial relationship (e.g., intersects, contains, within). If there is no matching row in the right (Geo)DataFrame for a row in the left (Geo)DataFrame, the result will still include the row from the left (Geo)DataFrame, but with missing values (NaNs) in the columns from the right (Geo)DataFrame.

Library
  A group of related modules. See definition of a {term}`module`.

List
  A data type in Python that can be used to store collections of values. Values in Python lists can be added, removed, or modified, and the list items do not need to be the same data types. Python lists are enclosed in square brackets (`[` `]`) and list items are separated by commas.

Loop
  A programming construct that allows a section of code to be repeated a finite number of times or until a given condition is met.

Lossless compression
  Lossless compression is a data compression approach that is used to reduce the file size of a raster dataset when writing without compromising the data quality. Some commonly used lossless compression methods include `LZD` and `DEFLATE`.

Lossy compression
  Lossy compression is a data compression approach that can significantly reduce the file size of a raster dataset with some loss of data quality and precision. Some commonly used lossy compression methods include `JPEG` and `JPEG2000`.
  
Map projection
  A map projection is a mathematical method to draw a graphical representation of the Earth's surface on a flat surface, i.e. a map. 
  
Map reprojection
  Map reprojection is a process of converting coordinates described in one coordinate reference system (CRS) to another. The transformation between coordinate systems involves both translation and rotation, and requires knowledge of the shape and size of the earth, as well as its orientation in space.  

Markdown
  A lightweight markup language used to convert plain text input to rich-formatted output.
  Markdown can, for example, be used to create simple documentation with different heading levels, text in bold and/or italics, text in lists, or documentation that includes hyperlinks.
  More information can be found at <https://en.wikipedia.org/wiki/Markdown>.
  
Metadata
  Metadata refers to data that provides information about other data. It often describes characteristics of the data, such as its content, quality, format, and other relevant characteristics. For example, the metadata of a satellite image may include information about the image's resolution, file size, coordinate reference system, and the date it was taken. 

Method
  A function that is associated with an instance of a specific Python data type. Methods can be accessed by typing the variable name of the instance, a period, and the function name.

Module
  A file containing Python definitions and statements. Module files have the `.py` file extension.

Mutable
  A data type that can be modified after being defined. In reality, things are a bit more complicated, but this is sufficient for our purposes. Opposite of {term}`Immutable`.

Namespace
  A collection of names and information about the objects to which the names refer. The objects could be variables or methods. There are four namespaces in Python (sorted here in order of {term}`scope` from broadest to narrowest): built-in, global, enclosing, and local.

Optional parameter
  A function {term}`parameter` that does not need to be provided when calling the function in order to use it. Optional parameters will use default function values that are provided in the function definition in such cases.

Parameter
  A variable listed within the parentheses of a function definition. Similar to an {term}`argument`.

Pothole case
  A variable naming convention that utilzes underscore characters (`_`) to separate words in the variable name. For example, `gps_station_id`. Also known as snake case.

Program
  A detailed list of step-by-step instructions that tell the computer exactly what to do.
  
Programming language
  A set of exact and unambiguous instructions that can be understood by the computer.

Radiometric resolution
  In satellite imagery, radiometric resolution refers to the ability of a sensor to measure and distinguish differences in the intensity of the electromagnetic radiation it detects. It is determined by the number of bits used to represent the data for each pixel, which defines the range of possible intensity values. For example, an 8-bit sensor can record 256 levels of intensity (0–255), while a 16-bit sensor can record 65,536 levels. 

Radius query
  A radius query is a type of spatial query that retrieves all points within a specified distance (radius) from a given query point. The query is performed typically on a {term}`KD-Tree` to efficiently find points that fall within a given distance from the query point. KD-Tree supports only Point objects, i.e. it cannot be used to search other geometric types, such as LineStrings or Polygons.

Repository
  A collection of files, in {term}`Git` for example, and the history of their changes. Often referred to informally as a "repo."

Required parameter
  A function {term}`parameter` that must be defined when calling the function in order to use it. Required parameters do not have default function values given in the function definition. Also known as positional parameters.

Revision
  Another name for a {term}`version`.

Right outer join
  Right outer join includes all the rows from the right (Geo)DataFrame and those rows from the left (Geo)DataFrame that have a matching key in the table, or that intersect or match based on the specified spatial relationship (e.g., intersects, contains, within). If there is no matching row in the left (Geo)DataFrame for a row in the right (Geo)DataFrame, the result will still include the row from the right (Geo)DataFrame, but with missing values (NaNs) in the columns from the left (Geo)DataFrame.

R-tree
  An R-tree is a type of data structure used as a {term}`spatial index` to efficiently query spatial objects. It organizes spatial data by grouping nearby objects and representing these groups with their minimum bounding rectangle. This hierarchical structure allows to query spatial data efficiently by eliminating groups of objects that do not intersect with the query area. R-trees are widely used in geographic information systems (GIS), databases, and for various spatial search and optimization tasks, enabling fast access and retrieval of spatial data based on their location and geometric properties.

Scope
  The region in which a name defined in a program has meaning. Python will search for names within the scope of {term}`namespaces <namespace>`; first in the local, then enclosing, then global, and finally in built-in.

Script
  A Python script is a collection of commands in a file that can be executed like a program. 

Semantics
  The exact meaning of a component in a programming language, such as a statement or a function. For example, the `len()` function in Python is used to determine the length of a data structure that is defined in memory.

Series
  In pandas library, a Series is a one-dimensional array-like data structure that holds a sequence of values, each associated with a unique index. It can store data of any type, such as integers, floats, or strings. A Series is essentially a single column of data and can be used as a building block for a {term}`DataFrame`. It supports various operations for data manipulation and analysis, making it a fundamental component of pandas.

Shifting
  The process of adjusting references in time series data forward or backward in time. For example, values could be shifted backward by one week to compare data from a given week to equivalent data from the following week.

Signed integer
  A (data) type of integer in Python that can represent both positive and negative whole numbers. The "signed" attribute means the number includes a "+" or "-" sign to indicate its value's polarity. For example, -5 and 42 are signed integers. In Python, integers are stored as signed by default and can handle very large values thanks to their dynamic size.

Slope
  Slope is a measure of the steepness or incline of the terrain. Slope is commonly calculated from elevation values in a raster and it represents the rate of change in elevation over distance and is typically expressed in degrees or percent.

Software
  Another name for a {term}`program`.

Source code
  The list of instructions in a {term}`computer` {term}`programming language` that define what a {term}`program` should do.

Spatial extent
  In geographic data, spatial extent refers to the geographic area covered by a dataset or map. It is typically defined by the minimum and maximum coordinates (e.g., latitude and longitude) that bound the dataset, forming a rectangle or other boundary in geographic space.

Spatial index
  A spatial index is a data structure designed to efficiently query spatial data, such as Points, LineStrings and Polygons within a multidimensional space. It optimizes the storage of spatial objects, enabling fast searches based on their geographic location and spatial relationships. Spatial indexes are crucial in geographic information systems (GIS) and spatial database management, where rapid access to spatial data is essential for tasks such as proximity searches, map rendering and spatial analysis. Common types of spatial indexes include R-trees, quad-trees, and k-d trees, each with its own method for partitioning space and organizing spatial data for efficient querying.

Spatial join
  A spatial join is a method used to combine spatial data based on the locations and relationships of the features in two separate geospatial datasets. It merges the two datasets based on their spatial relations, e.g. by joining information from all points in a given dataset that are within given polygons present in another dataset.

Spatial queries
  A spatial query is a process in GIS commonly used e.g. to select spatial features or properties based on the spatial relationships between geospatial data layers or geometries. Spatial queries are used for answering topology related questions on the basis of geometric information only, i.e., the spatial position and extent of the geometric objects involved.

Spatial resolution
  The spatial resolution of a raster refers typically to the size of the cells in a raster dataset. It can also mean the ratio of screen pixels to image pixels at the current map scale. 

Spatial predicate
  Spatial predicate is an output from {term}`DE-9IM` model that describe the spatial relationship between two geometric objects. Example spatial predicates are within, contains, touches and intersect.
  
Spatio-temporal data model
  A data model that incorporates time (t) as an additional dimension to the geographical dimension (x, y). 

Spectral resolution
  In multispectral satellite data, spectral resolution refers to the ability of a sensor to distinguish between different wavelengths of electromagnetic radiation. It is defined by the number and width of the spectral bands the sensor can capture. Higher spectral resolution means the sensor can detect finer differences in wavelength, allowing for more detailed analysis of surface materials and phenomena.

Subplots
  The term used in Matplotlib to refer to individual plots when more than one plot is part of a single figure.

Syntax
  The precise form of a component in a programming language. For example, the print function in Python expects the syntax `print('hello')` in order to have the word hello displayed on the screen.

Temporal resolution
   In satellite imagery, temporal resolution refers to the frequency at which a specific area on Earth's surface is revisited and imaged by a satellite sensor. It determines how often data is collected for a given location and is typically expressed as the time interval between consecutive observations (e.g., daily, weekly). Higher temporal resolution enables more frequent monitoring, while lower temporal resolution provides less frequent updates but may cover broader areas or focus on finer spatial or spectral details.

Topological spatial relations
  Topological spatial relations describe how two or more geometric objects relate to each other concerning their position and boundaries. Topological spatial relations can be exemplified by relationships such as contains, touches and intersects. In GIS, these kind of topological relations play a crucial role as they enable queries that are less concerned with the exact coordinates or shapes of geographic entities but more focused on their relative arrangements and positions.
  
Tuple
  A [tuple](https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences) is a Python data structure that consists of a number of values separated by commas. Coordinate pairs are often represented as a tuple, such as: `(60.192059, 24.945831)`. Tuples belong to [sequence data types](https://docs.python.org/3/library/stdtypes.html#typesseq) in Python. Other sequence data types are lists and ranges. Tuples have many similarities with lists and ranges, but they are often used for different purposes. The main difference between tuples and lists is that tuples are [immutable](https://docs.python.org/3/glossary.html#term-immutable), which means that the contents of a tuple cannot be altered (while lists are mutable; you can, for example, add and remove values from lists).

Type conversion
  Changing the data type of a Python object. For example, `float(5)`.

Unary union
  The unary union operation takes multiple geometries and merges them into a single geometry. This is useful when you have a collection of shapes and you want to treat them as a single entity for analysis or visualization.

Unsigned integer
  A type of integer that represents only non-negative whole numbers, starting from zero. Unlike {term}`signed integers`, unsigned integers do not include a "+" or "-" sign, allowing them to use all their bits for positive values.

Variable
  A way of storing values in the memory of the computer using specific names that you define.

Version
  A specific instance of changes to files in a {term}`repository` of a {term}`version control` system. Also referred to as a {term}`revision`.

Version control
  The practice of tracking changes to computer files, typically {term}`source code` files for {term}`computer programs <Program>`. Version control allows users to easily collaborate and revert to previous versions.

Virtual environment
  A virtual environment is a Python programming environment which works in a way that the Python interpreter, libraries and scripts installed into it are isolated from the ones installed in other virtual environments, as well as from (possible) system Python, i.e., one which is installed as part of your operating system.

Watershed
  An area of land where all surface water drains to a common outlet, such as a river, lake, or ocean.
  
Well-known binary
  Well-known binary (WKB) is a format for representing vector geometry objects in compressed binary format which is useful for computer processing. The human-readable equivalent for WKB is `Well-known text` format. WKB can represent various geometric objects: Point, MultiPoint, LineString, MultiLineString, Polygon, MultiPolygon, Triangle, PolyhedralSurface, TIN (Triangulated irregular network) and GeometryCollection. Coordinates for the geometries can be represented in 2D, 3D or 4D (x,y,z,m).

Well-known text
  Well-known text (WKT) is a text markup language for representing vector geometry objects. WKT can represent various geometric objects: Point, MultiPoint, LineString, MultiLineString, Polygon, MultiPolygon, Triangle, PolyhedralSurface, TIN (Triangulated irregular network) and GeometryCollection. Coordinates for the geometries can be represented in 2D, 3D or 4D (x,y,z,m). The binary equivalent for WKT is `Well-known binary` format.
```
<!-- #endregion -->
