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

# Effective plot design: line plots

As we have seen, you should be aiming to produce plots that include all of the elements that help make understanding the plotted data intuitive. Typically, this might include:

- Axis labels, including units if needed
- A legend
- Grid lines
- Plot and/or figure titles
- Annotation on the plot, such as text

In addition, there are several factors that can help improve the communication of the plotted information. When plotting line data, for example, the color of the lines might be an important consideration to tell different lines apart. This is especially true when plotting several lines on the same axes, as readers will need to be able to differentiate the lines and know which line refers to a given set of data. But there is more to plotting lines than simply choosing nice colors. 

Not all people viewing your plots will see them the same way. Some viewers may have color blindness, while others may have printed out a copy of your plot in grayscale from a printer. Thus, while choosing nice colors can help make your plots look visually pleasing to you, it is worthwhile to consider other viewers and formats in which your plots may be viewed. In this way your visualizations can be as inclusive to different viewers as possible.

## Tips for plotting lines

Let's consider an illustrative example. In this case we will use four lines to plot hypothetical monthly temperatures for various mythical lands in the year 1680 [^nerds]. We will use a pandas DataFrame called `data` for this purpose with four columns and one year of data. We can see temperatures for the first four months in the data table below by typing `data.head(4)`.

```python tags=["hide-cell"]
# Load the libraries we need
import matplotlib.pyplot as plt
import pandas as pd

dates = pd.date_range(start="16800101", end="16801201", freq="MS")
temperatures = {
    "Asgard": [
        2.61080759,
        3.80300147,
        6.81951259,
        8.07302111,
        10.92665915,
        13.18569725,
        11.15190422,
        11.88095271,
        8.16883214,
        7.27447255,
        3.43161114,
        2.78345483,
    ],
    "Camelot": [
        6.91054909,
        7.78720085,
        7.69825447,
        12.35036454,
        14.84349615,
        19.77590178,
        19.3768641,
        17.37775864,
        11.06999359,
        9.30251052,
        7.4073777,
        6.61132001,
    ],
    "Nysa": [
        9.97005829,
        13.20188993,
        12.94964658,
        16.57315997,
        21.00721179,
        22.90791358,
        22.53282688,
        19.92502575,
        19.95551156,
        15.53906563,
        10.7195169,
        10.19603786,
    ],
    "Paititi": [
        7.73300265,
        9.85720691,
        18.96796882,
        20.39733145,
        30.67161633,
        35.05950444,
        29.18180578,
        31.1744113,
        16.49727756,
        14.0604099,
        9.07097188,
        9.36868944,
    ],
}

data = pd.DataFrame(index=dates, data=temperatures)
```

```python
data.head(4)
```

And now we can create a plot (Figure 4.X) to visualize all of the temperature data for the four mythical lands using the pandas `plot()` function.

```python
ax = data.plot(
    xlabel="Date",
    ylabel="Temperature (°C)",
    figsize=(12, 6),
    title="Hypothetical temperatures of mythical lands",
)
```

_**Figure 4.X**. Hypothetical temperatures for one year in different mythical lands._

In Figure 4.X, we can see all of the data in the `data` DataFrame and many people may be able to distinguish the lines using the four different colors that have been selected. However, not all people will see the figure in the same way, and those who may have printed a copy in grayscale will see things quite differently.

![_**Figure 4.X**. Hypothetical mythical land temperatures in grayscale._](../img/lines-grayscale.png)

_**Figure 4.X**. Hypothetical mythical land temperatures in grayscale._

In Figure 4.X, we see that it is nearly impossible to tell which line is which in the plot, so color alone is not helping in distinguishing the lines on this plot. In this case a better option is to vary both color and the line pattern for each line so they can be distinguished easily irrespective of the selected line colors. That can be done using the `style` parameter as shown below.

```python
ax = data.plot(
    style=["-", ":", "--", "-."],
    xlabel="Date",
    ylabel="Temperature (°C)",
    figsize=(12, 6),
    title="Hypothetical temperatures of mythical lands",
);
```

Here in Figure 4.X viewers can easily tell which line is which whether they have colorblindness or have printed a figure from a grayscale printer. Figure 4.X uses four different line styles: `-` for a solid line, `:` for a dotted line, `--` for a dashed line, and `-.` for a line with dots and dashes. These are defined using shorthand plot formatting for Matplotlib [^shorthand], for which there are only four available line styles. If your plots require more than four line styles, you will likely need to use Matplotlib rather than pandas for the plotting. In that case you can find more about the line styles for Matplotlib plotting in the [Matplotlib documentation online](https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html) [^linestyles]. 

Although this plotting example may seem like a simple tip, it can make a great difference in ensuring all viewers see the same data effectively the same way. We will return to the topic of effective plot design to discuss selecting colors and other visualization tips in greater detail in Chapter 8.


## Footnotes

[^linestyles]: <https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html>
[^nerds]: We too are nerds, but please note these temperatures are in no way meant to be taken seriously.
[^shorthand]: See notes section at <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html>
