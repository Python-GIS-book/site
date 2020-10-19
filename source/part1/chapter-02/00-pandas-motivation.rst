Introduction to data analysis using Pandas
==========================================

What is Pandas?
---------------

.. figure:: img/pandas_logo.png
   :width: 300px

   Source: `Medium.com <https://medium.com/towards-data-science/a-quick-introduction-to-the-pandas-python-library-f1b678f34673>`__

`Pandas <http://pandas.pydata.org/>`__ is a modern, powerful and feature rich library that is designed for doing
data analysis in Python. It is a mature data analytics framework (originally written by Wes McKinney) that is widely used among different fields of science,
thus there exists a lot of good examples and documentation that can help you get going with your data analysis tasks.

Easy-to-use data structures
---------------------------

In Pandas the data is typically stored into a DataFrame that looks like a typical table with rows and columns
(+ indices and column names), where columns can contain data of different data types.
Thus, it reminds of how the data is stored e.g. in Excel or in R that also uses a concept of a dataframe. In fact,
Wes McKinney first `developed Pandas as an alternative for R <https://blog.quantopian.com/meet-quantopians-newest-advisor-wes-mckinney/>`_ to deal with different complex data structures.

Combines the power of many Python modules
------------------------------------------

Pandas is a "high-level" package, which means that it makes use of several other packages in the background.
This book focuses primarily on Pandas because it is easy-to-use, efficient and intuitive.
Pandas combines the performance of powerful Python libraries such as `NumPy <http://www.numpy.org/>`__,
`matplotlib <https://matplotlib.org/>`__ and `scipy <https://www.scipy.org/>`__.
Thus, you can use many of the features included in those packages even without importing them separately.

Supports multiple data formats
-------------------------------

One of the most useful features of Pandas is its ability to write and read data to and from numerous data formats.
Pandas supports reading and writing data e.g. from/to:

- CSV
- JSON
- HTML
- MS Excel
- HDF5
- Stata
- SAS
- Python Pickle format
- SQL (Postgresql, MySQL, Oracle, MariaDB, etc.)

See full list from `Pandas docs <http://pandas.pydata.org/pandas-docs/version/0.20/io.html>`__.