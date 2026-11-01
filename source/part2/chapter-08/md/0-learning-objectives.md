---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.19.5
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

<!-- #region editable=true slideshow={"slide_type": ""} tags=["learning_objectives"] -->
# Learning objectives
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} -->
Chapter 8 focuses on spatial network analysis and introduces how to create routable networks that can be used to find shortest path from one location to another along a given street network. You will learn how to represent geographic data as networks in Python, how to calculate shortest paths and travel times along street networks retrieved from OpenStreetMap, and how to analyze the structure of a network through its connectivity, topology and centrality. The same techniques are also applied to other types of networks, such as rivers and power grids.

Knowing how to work with vector data using `geopandas` (Chapter 6) is a prerequisite for learning to analyze spatial networks in this chapter.
<!-- #endregion -->

<!-- #region editable=true slideshow={"slide_type": ""} tags=["lo_box"] -->
```{admonition} Learning objectives
:class: tip

At the end of this chapter, you should be able to:

- Represent geographic data as networks in Python using the `networkx` library
- Generate a routable network for a given transport mode
- Understand the basics of how commonly used route optimization algorithms work
- Calculate and visualize shortest paths and travel times along a network
- Check whether a network is connected and fix errors in its topology
- Measure the importance of nodes and edges with centrality measures

```
<!-- #endregion -->
