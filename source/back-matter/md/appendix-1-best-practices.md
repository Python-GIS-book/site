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

# Python programming best practices


Content to be added.


## Using modules

### Import modules at the start of your files

According to the good coding practices described in [PEP 8](https://peps.python.org/pep-0008/#imports) [^pep8], we should always import modules at the top of a file. In this section, we have demonstrated how to import different modules along the way, but in general it is better to import required modules as the very first thing. PEP 8 refers more to traditional script files, but we can apply the guideline to Jupyter Notebook files as well by placing `import` statements in the first code cell of the notebook.

### Avoid importing functions using wildcards

It is best not to import many functions from a module using the form `from X import *`, where `X` is a Python module. `from X import *` will import all of the functions in module X, and though you might think this is helpful, it is much better to simply `import X` or `import X as Y` to maintain the connection between the functions and their module. In addition to losing the connection between the module and the function, it is much more likely you will encounter conflicting function names when using `from X import *`.

### Choose logical names when renaming on import

Do not use confusing names when renaming on import. Be smart when you import modules, and follow generally used conventions (`import pandas as pd` is a good way to do things!). If you want to make the module name shorter on import, pick a reasonable abbreviation. For instance, `import matplotlib as m` could be confusing, especially if we used `import math as m` above and might do so in other Jupyter notebooks or script files. Similarly, `import matplotlib as math` is perfectly OK syntax in Python, but bound to cause trouble. Remember, people need to be able to read and understand the code you write. Keep it simple and logical.


## Footnotes

[^pep8]: <https://peps.python.org/pep-0008/#imports>
