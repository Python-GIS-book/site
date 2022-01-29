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

# Anatomy of a plot


Before starting to visualize our data on a plot our data we need to address an obvious question: **What actually is a plot?** We will not go deep into the details of different types of plots (as it is not the purpose of this book), but rather we provide a brief introduction to different plots that can be created using Python and the (essential) elements of a plot.

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

In spite of the large variety of types of plots, there are certain elements that are common for most of them (not all). Thus, it is useful to know at least the basic terminology since it makes it easier to find help and information from the internet when you start creating or modifying your own plots.

Figure 4.2 illustrates different elements of a basic line plot.

![_**Figure 4.2**. The basic elements of a plot. Image source: Tenkanen (2017)_](../img/basic-elements-of-plot.png)

_**Figure 4.2**. The basic elements of a plot. Image source: Tenkanen (2017)_

## Common plotting terminology

These common terms may vary a bit depending on the plotting library that you use. For the list provided here we are using the typical terms for plotting in Matplotlib (see also Figure 4.2).

| Term         | Description                                                                                                         |
|--------------|---------------------------------------------------------------------------------------------------------------------|
| *axis*       | Axis of the graph that are typically x, y and z (for 3D plots).                                                     |
| *title*      | Title of the whole plot.                                                                                            |
| *label*      | Name for the whole axis (e.g. xlabel or ylabel).                                                                    |
| *legend*     | Legend for the plot.                                                                                                |
| *tick label* | Text or values that are represented on the axis.                                                                    |
| *symbol*     | Symbol for data point(s) (on a scatter plot) that can be presented with different symbol shapes/colors.             |
| *size*       | Size of, for example, a point on a scatter plot. Also used for referring to the text sizes on a plot.               |
| *linestyle*  | The style how the line should be drawn. Can be solid or dashed, for example.                                        |
| *linewidth*  | The width of a line in a plot.                                                                                      |
| *alpha*      | Transparency level of a filled element in a plot (values between 0.0 (fully transparent) to 1.0 (no trasnparency)). |
| *tick(s)*    | Refers to the tick marks on a plot.                                                                                 |
| *annotation* | Refers to the text added to a plot.                                                                                 |
| *padding*    | The distance between a (axis/tick) label and the axis.                                                              | 
