---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.11.5
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

# Plotting in Python

Data visualization is an essential part of understanding and interpreting data, and Python has a large number of libraries available for use in visualizing different types of data. Below we provide a bried overview of some of the Python plotting landscape as well as an introduction to the terminology commonly used to refer to different parts of a plot created using Python.


## Python plotting libraries

![_**Figure 4.1**. Plotting libraries available in Python. Interactive version online at <https://pyviz.org/overviews/index.html>._](../img/python-plotting.png)

_**Figure 4.1**. Plotting libraries available in Python. Interactive version online at <https://pyviz.org/overviews/index.html>._

Python has many nice, useful libraries that can be used for plotting. In the figure above, you can see a number of the available plotting library options, along with how they relate to one another. Of the options above we would like to highlight the following:

- [Matplotlib](https://matplotlib.org/) [^matplotlib]: Matplotlib is one of the most widely used Python plotting libraries, sometimes referred to as "*the grand old man of Python plotting*". Plot examples can be found in the [Matplotlib gallery](https://matplotlib.org/gallery.html).

  - [Matplotlib Basemap](https://matplotlib.org/basemap/index.html) [^basemap]: The Matplotlib Basemap Toolkit is a plugin for visualizing maps in Python. Example plots available in the [Matplotlib basemap gallery](https://matplotlib.org/basemap/users/examples.html).
  - [Seaborn](https://seaborn.pydata.org/) [^seaborn]: Seaborn is a high-level interface for drawing attractive statistical graphics that is built on top of Matplotlib. Example plots can be found in the [Seaborn gallery](https://seaborn.pydata.org/examples/index.html).

- [Bokeh](https://docs.bokeh.org/en/latest/) [^bokeh]: Bokeh is a modern plotting library for static and interactive web-based plots including graphs, maps, and charts. Examples can be found in the [Bokeh gallery](https://docs.bokeh.org/en/latest/docs/gallery.html).
- [Plotly](https://plotly.com/python/) [^plotly]: Similar in some ways to Bokeh, Plotly is a modern plotting library for static and interactive web-based plots. Some features are commercial. Example plots are available in the [Plotly gallery](https://plotly.com/python/basic-charts/).
- [Dash](https://plotly.com/dash/) [^dash]: Dash is a Python framework for building analytical web applications. No JavaScript required.
- [ggplot](https://yhat.github.io/ggpy/) [^ggplot]: ggplot is a Python plotting environment for those familiar with creating plots in R using ggplot2. You can use ggplot in Python too! Plot examples can be found in the [ggplot examples](https://yhat.github.io/ggpy/).
- [HoloViews](https://holoviews.org/) [^holoviews]: and [GeoViews](https://geoviews.org/) [^geoviews]: HoloViews and GeoViews aim to let the data visualize itself. Learn more in the HoloViews introductory video at <https://www.youtube.com/watch?v=hNsR2H7Lrg0>.

  - Both are modern and powerful visualization libraries built on top of Matplotlib and Bokeh that make exploring and visualizing your data quicker than ever before.
  - HoloViews is designed for basic plotting. More information available in the [HoloViews tutorial](https://holoviews.org/Tutorials/index.html) and the [HoloViews example plots](https://holoviews.org/Examples/index.html).
  - GeoViews is designed for creating nice and interactive maps. Examples can be found in the [GeoViews gallery](https://geoviews.org/gallery/index.html).

You should explore the plotting galleries and examples of different visualization libraries above to learn what's possible to do in Python. As you will see, the plotting possibilities in Python are numerous and rich. To get started, we suggest starting by learning to use one that suits your needs best, and later extending your knowledge and skills to other visualization libraries as necessary.

<!-- #region -->
## Anatomy of a plot

There are a variety of different kinds of plots (also known as graphs, charts, diagrams, etc.) available that have been designed to visually represent the characteristics of a dataset. Here is a list of several different types of plots that can be used to present different kinds of data. You can find more information about this plots online in Wikipedia, for example.

- [Bar chart](https://en.wikipedia.org/wiki/Bar_chart)
- [Histogram](https://en.wikipedia.org/wiki/Histogram)
- [Scatter plot](https://en.wikipedia.org/wiki/Scatter_plot)
- [Line chart](https://en.wikipedia.org/wiki/Line_chart)
- [Scatter plot](https://en.wikipedia.org/wiki/Scatter_plot)
- [Pie chart](https://en.wikipedia.org/wiki/Pie_chart)
- [Box plot](https://en.wikipedia.org/wiki/Box_plot)
- [Violin plot](https://en.wikipedia.org/wiki/Violin_plot)
- [Dendrogram](https://en.wikipedia.org/wiki/Dendrogram)
- [Chord diagram](https://en.wikipedia.org/wiki/Chord_diagram)
- [Treemap](https://en.wikipedia.org/wiki/Treemap)
- [Network chart](https://en.wikipedia.org/wiki/Network_chart)

However, before starting to visualize our data on a plot our data we need to address an obvious question: **What actually is a plot?** We will not go deep into the details of different types of plots such as those listed above, as it is not the purpose of this book, but rather we will provide a brief introduction to different plots that can be created using Python and the (essential) elements of a plot.

![_**Figure 4.2**. The basic elements of a plot. Image source: Tenkanen (2017)._](../img/basic-elements-of-plot.png)

_**Figure 4.2**. The basic elements of a plot. Image source: Tenkanen (2017)._


In spite of the large variety of types of plots, there are certain elements that are common for most of them (not all). Thus, it is useful to know at least the basic terminology since it makes it easier to find help and information from the internet when you start creating or modifying your own plots. Figure 4.2 illustrates different elements of a basic line plot.
<!-- #endregion -->

### Common plotting terminology

The common terms in Table 4.1 may vary a bit depending on the plotting library that you use. For the list provided here we are using the typical terms for plotting in Matplotlib (see also Figure 4.2).

: _**Table 4.1**. Common terminology for plot features in Matplotlib._

| Term       | Description                                       |
|:-----------|:--------------------------------------------------|
| axis       | Axis of the graph that are typically x, y and z   |
|            | (for 3D plots).                                   |
| title      | Title of the whole plot.                          |
| label      | Name for the whole axis (e.g. xlabel or ylabel).  |
| legend     | Legend for the plot.                              |
| tick label | Text or values that are represented on the axis.  |
| symbol     | Symbol for data point(s) (on a scatter plot) that |
|            | can be presented with different symbol shapes or  |
|            | colors.                                           |
| size       | Size of, for example, a point on a scatter plot.  |
|            | Also used for referring to text sizes on a plot.  |
| linestyle  | The style how the line should be drawn. Can be    |
|            | solid or dashed, for example.                     |
| linewidth  | The width of a line in a plot.                    |
| alpha      | Transparency level of a filled element in a plot  |
|            | (values range between 0.0 (fully transparent) to  |
|            | 1.0 (no trasnparency)).                           |
| tick(s)    | Refers to the tick marks on a plot.               |
| annotation | Refers to the text added to a plot.               |
| padding    | The distance between a (axis/tick) label and the  |
|            | axis.                                             |



## Footnotes

[^basemap]: <https://matplotlib.org/basemap/index.html>
[^bokeh]: <https://docs.bokeh.org/en/latest/>
[^dash]: <https://plotly.com/dash/>
[^geoviews]: <https://geoviews.org/>
[^ggplot]: <https://yhat.github.io/ggpy/>
[^holoviews]: <https://holoviews.org/>
[^matplotlib]: <https://matplotlib.org/>
[^plotly]: <https://plotly.com/python>
[^seaborn]: <https://seaborn.pydata.org>
