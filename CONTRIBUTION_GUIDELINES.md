# How to develop contents to this book project? - Guidelines

**Contents**

 - [Objectives](#objectives)
 - [Technologies used](#technologies-used)
 - [How to create content?](#pipeline---how-to-create-content)
 - [Formatting conventions](#formatting-conventions)
 - [Build local version of the docs](#to-build-local-version-of-the-docs)
 - [Upload contents to Github](#to-upload-the-contents-to-github)
 - [Ask for a review by making PR](#ask-for-a-review-by-making-a-pull-request)
 - **How to?**
    - [Sync Notebook with MyST Markdown](#sync-jupyter-notebook-with-myst_markdown)
    - [Add a citation](#add-a-citation)
    - [Allow errors to be included in the docs](#allow-an-error-to-happen-in-code-blocks)
    - [Hide cells on the website or in the book](#hide-cells)
    - [Lint Notebooks](#lint-notebooks)

## Objectives

By using the approaches described in this document we aim that producing the materials would:

 1. **be easy**
 2. allow us to benefit from all the latest developments in online education (e.g. the features developed by `executablebooks` -project)
 3. allow us to easily see the changes/additions made to the documents by contributors
 4. allow us to comment on texts / additions made by others (in GitHub)

## Technologies used

To achieve the goals specified above, we will use following technologies:

 1. Jupyter Book / sphinx-book-theme: allows us to make the learning experience better e.g. with interactive functionalities
 2. Jupyter Notebooks using [MyST markdown syntax](https://jupyterbook.org/content/myst.html) allowing us to use Sphinx directives and control the page layout 
 3. [Jupytext](https://github.com/mwouts/jupytext) - Syncs the notebooks with markdown version of the same file **allowing us to better use GitHub diff functionalities**
 4. [MyST_NB](https://myst-nb.readthedocs.io/en/latest/) - Converts the notebooks into RST files that are rendered by Sphinx. 
 

## Pipeline - How to create content?

The materials for the book are organized under different chapters. 

### To produce the content:
 
 1. Add your Jupyter notebook under the `nb` -subfolder (*notebooks*) where your content belongs, such as:
    - `part1/chapter-01/nb/02-python-basics.ipynb`
 2. Remember to name your file in an intuitive manner, and include chapter numbering, e.g. `2-1_intro-to-data-analysis-with-pandas.ipynb`
 3. Write contents into this notebook as you would do normally. Remember to use [MyST markdown syntax](https://jupyterbook.org/content/myst.html) for enriching the contents with Jupyter Book functionalities.
    - Note: after you have saved your notebook, a paired Markdown version of the file will be created automatically inside `md` -directory. See [more info from here](#sync-jupyter-notebook-with-myst_markdown).
 4. Push the files / changes to the branch you are working on (e.g. `chapter_1` branch)
    - Remember to push both the Jupyter Notebook and the paired Markdown version of the file

### To build local version of the docs:

Once you have written materials, and you want to see the results **live**, you can build and see the local version of the documentation by:

 1. Build the docs with `$ make html` (with sphinx-book-theme) 
 2. You can see the docs under `_build/html` directory located in the root of the project
    
### To upload the contents to GitHub:

Once you are happy with the contents, you can upload the contents (both Notebook and Markdown version) to GitHub into the `<chapter>` branch 
(see docs about our [branching workflow below](#ask-for-a-review-by-making-a-pull-request)).
 
**NOTE**: Pushing to `master` branch directly is not allowed (it is restricted), hence when you want to add something to master, you need to do it
 via Pull Request (PR).  
 
### Ask for a review by making a Pull Request

For building the book we use a **branching workflow** consisting of 3 levels (following best practices):

![Git branching workflow](img/branching_workflow.png)

Hence, when you are working on a topic (e.g. Chapter 2) you should have a separate branch for that topic and add your materials there 
(as demonstrated in the figure above).

When you are happy with the contents, and you would like to ask comments from other contributors, you should **make a Pull Request**
by merging the contents from your branch into the **develop** branch (note: not master). When you have done the pull request,
other contributors can make comments in GitHub directly to your "code" (documentation) and we can discuss in there easily. 
Once everything seems to be okay, some of the maintainers will accept the review and merge the contents to `develop` branch.

**Why not merge to master straight away?**

The master branch is facing the "outside" world. Hence, it is reserved for contents that are in a "publishable state". Once we
think that we want to publish the materials (e.g. for asking comments from "public"), we certainly can do that. But by default,
master is to be used only when we want to publish something, and send materials to "production".  

## Formatting conventions

## General text formatting

### Sections and subsections

Normal text is divided into sections and subsections using headings.
The top-level heading (H1) is reserved for page titles (major section titles).
Heading levels 2 and 3 are used for internal sections and sub-sections.
Heading level 4 should be used for "Check your understanding" sub-sections.

**Important**: Make sure that whenever you start a new section (starting with # character), the section
will be placed inside a new Markdown cell. This is needed because in the book building process, the heading
levels need to be modified, and the headings are always searched from the first line of a Markdown cell. 

### Text conventions

#### No formatting

Normal text is written without any special formatting.

#### Inline code

- variable names
- data types (e.g. `str`)
- data structures (e.g. `DataFrame`)
- function names
- methods / attributes (e.g. `.plot()` or `.area`)
- package / module names (e.g. `pandas`)
- commands
- keywords

##### Notes about inline code formatting

Inline code formatting for data types and data structures should be used *only* when referencing a specific instance of the data type or structure. Otherwise, normal text formatting should be used (e.g., dataframe).

> Here, we introduce {term}`pandas`, which is a common data analysis library in Python that utilizes two key data structures: {term}`DataFrame` and {term}`Series`. The dataframe structure in `pandas` is similar to the dataframe data structure in `R`. Let's begin by creating a new `DataFrame` called `my_data`.

In the text above we can see that the pandas library is mentioned for the first time, and as an important library we have included a link to the glossary using the {term}`` formatting. This is similar for the first references to DataFrame and Series. After this, we refer to dataframes in general, not a specific instance, so the text is not formatted. Finally, we create a new dataframe instance, so inline code formatting is used.

As another example, let's consider Python lists:

> So far, we have learned a bit about variables, their values, and data types in this section. We will now continue with a new data type called a *{term}`list`*. Using a list, we can store many related values together with a single variable. ... Let’s first create a `list` of some station names and print it out.

Similar to the pandas example, we link to the glossary when mentioning list for the first time. After that, general references to lists are not formatted. When creating a new list instance, we now use inline code formatting.

#### Code blocks

What: Multiline code as part of the Markdown text.

- Long code snippets
- File content
- Output from code
- Function / method documentation + help snippets

#### Bold text

- emphasizing text
- key strokes (**shift** + **enter**)

#### Italics

- glossary entries
- URLS
- file names
- file extensions 

### Figure captions

When you add an image to the notebook, the caption should be inserted as follows:

1. Add the full caption with styling inside the square brackets (as alt-text) - Latex will use this information, such as:
   - `![_**Figure 1.1**._ pandas DataFrame is a 2-dimensional data structure used for storing and mainpulating table-like data (data with rows and columns). pandas Series is a 1-dimensional data structure used for storing and manipulating an sequence of values.](./../img/pandas-structures-annotated.png)`

2. Add the same full caption (with same styling) also as a regular text after the image so that it is visible also in the website.

  - When the book PDF is built, the duplicate caption will be removed.
  
In the text, refer to the Figures using their figure numbers (e.g. Figure 1.1). 
The first part of the figure number refers to the chapter, 
and the second part to the sequential number (order) of the figure within the given chapter. 
  

### Glossary terms

Important terms should be included in italics using the glossary.
Glossary terms can be added with the format

```
*{term}`Glossary term`*
```

where "Glossary term" is the item listed in the glossary at `back-matter/glossary.md`.
It is also possible to have different text listed when linking to a glossary item, such as 

```
*{term}`My glossary item <item>`*
```

where the link to the glossary entry "item" has the displayed text "My glossary item".

### Footnotes

URLs should use footnotes such as[^url1].
Footnotes are formatted as `[^footnote]` when placed in the text.
They are enclosed in square brackets and start with the `^` character.
At the end of the document, the footnote definitions can be given in the form

```
[^footnote]: Footnote text and or URL with the form <https://jupyter.org>. Note the angled brackets `<` and `>` enclose the URL to autolink them.
```

### Special text formatting blocks

- Code blocks (more about this?)
- Admonitions (do we use these at all?)

```{note}
This is a note. It expands on the main text or indicates additional information not included in the main text. Additional reference material or differences from past topics, for example.
```

```{tip}
This is a tip. Tips should be used for helpful reminders or suggested use cases.
```

```{warning}
This is a warning. This is text that warns of potential for problems if it is ignored. This could be used to indicate unexpected behavior, such as needing to create copies of dataframes to avoid modifying source dataframes.
```

## How to?

### Sync Jupyter Notebook with MyST_Markdown

To be able to use GitHub's `diff` functionalities e.g. when doing a review of the materials that some of us has developed, 
it is "necessary" to have a Markdown version of the notebook. *Showing differences between notebooks in GitHub is a mess because 
the notebooks are essentially JSON files containing lots of metadata etc. which makes it hard to see the differences in the 
actual contents that we are interested in.*

In our project, all the notebooks that are stored under a folder named `nb` will be automatically synced and paired
as markdown files. The result looks something like:

![Paired notebook](img/jupytext-pairing-org.PNG)

where the `nb` directory contains the "original" notebook. The `md` directory with paired markdown file is automatically created after the notebook is saved for the first time. 
It is recommended to store all the external files such as images in a separate folder (`img` here) and place that on the same
directory level as `nb` and `md`. In such way, the relative paths work correctly always in both versions of the documentation.

The automation of this pairing process is controlled from the `.jupytext.toml` configuration file. 

#### Manual pairing

It is also possible to manually pair a single notebook. To make a ST_Markdown **paired version** of the notebook in Jupyterlab, choose the `Commands` tab from the left panel, and 
write `Jupytext` to the search box which will show you an option to `Pair Notebook with MyST Markdown`:
![Pairing notebook with MyST Markdown](img/Jupytext_pairing_in_JupyterLab.PNG)  

After you have activated the *pairing*, you will always have an identical copy of the Notebook in the same directory 
as a Markdown file. **NOTE**: The files are **really** synced, hence if you make a change to the Markdown version of the notebook
and save it, those changes will be automatically reflected to the Notebook as well (and vice versa). If you don't see the changes
in the Notebook in Jupyterlab, you might need to refresh the page (F5).  

### Add a citation

For adding citations, we take advantage of [sphinx-bibtex](https://sphinxcontrib-bibtex.readthedocs.io/en/latest/usage.html) extension for Sphinx.
There is a specific syntax for adding these using MyST markdown syntax ([see full docs here](https://jupyterbook.org/content/citations.html)).

The basic workflow:

 1. Add references to `references.bib` file that should be located on the same directory where you Notebook is located.
    - Hint: to add a reference to this file from Mendeley is easy by right clicking the document in Mendeley list and choosing 
    `Copy As --> BibTex Entry`. This is then copied to clipboard, and you can paste it into the `references.bib`.  
    
 2. Add a reference to the markdown cell with ```{cite}`myReference2020` ```
    - This name should match with the entry name that you added to `references.bib`
    - **Note**: You need to add parentheses for references that should be in parentheses in the text. For example, (```{cite}`McKinney2017` ```) to produce (McKinney, 2017) as the formatted citation in the text.
    - Similarly, references that would normally be in the format McKinney (2017) or McKinney, 2017 should be cited without parentheses.

 3. When you want to add the bibliography (see also note below), you should add ```{bibliography} path/to/references.bib ``` 
 to the location where you want to add the reference list (e.g. at the end of each Chapter).
 
**NOTE**: If you want to use a custom APA style (defined in conf.py), you should add the bibliography as follows:
```
{bibliography} path/to/references.bib
:style: apa
```  
 
### Allow an error to happen in code blocks?

Introducing errors in the code is quite typical when teaching. Writing contents that raise errors is straightforward, **however**,
when you want to **build** the website having errors you most probably end up having a build error when executing `make html`. 
To avoid this, it is necessary to add **a cell tag** `raises-exception` to those cells with errors that you want to include into the final documentation. 

To get information how to add a cell-tag, follow [these instructions](https://github.com/jupyterlab/jupyterlab-toc/issues/87).

### Hide cells

Cell tags can also be used to hide notebook cells in several different ways depending on the situation. You can find a few common situations below.

#### Removing a cell from the website and book

If you have a cell that does something that affects the content produced in the notebooks, but do not want that cell to be visible in any way in the book or on the website, you can add the `remove_cell` tag to the cell (note the underscore). This will completely remove it from both places.

#### Removing a cell from the book only and hiding the output on the website

Cells can be removed from being shown in the book and have their output hidden on the website (with a dropdown that can show the output) by using the `remove_book_cell` and `hide-cell` tags. This is common for output from one of the book questions, where the output is handy to see on the website (but hidden) while in the book the answers to the questions are in the back of the book.

#### Hiding cell output

If you wish for the cell output to be visible in the book, but not on the website, you can set the cell type to `Raw` and then use the `hide-cell` tag. This will include the text from the cell in the book, but show nothing on the website. This can be useful for adding book figures in cases where the normal figure output is not visible in the book.

### Lint Notebooks?

We are using `black` library for linting the Notebooks, so that the formatting of all the codes is done systematically.

You need to lint all Notebooks before commits from `develop` branch can be merged to `main` branch. To do this:

1. Ensure that the `python-gis-book` environment is activated and your terminal is located inside the `source` -folder.
2. To check which Notebooks require linting, you can run following command: `black . --check`
3. To check how the Notebooks will be formatted by `black`, you can run following command: `black . --diff`
4. To format the Notebooks with `black`, you can run following command: `black .`
   - This command will auto-format all the Notebook cells where the code is not formatted appropriately.
5. **Important**: Once you have formatted the Notebooks, you still need to sync the Markdown versions with the changes because `black` does not touch the .md files. To do this:
   1. Check which Notebooks were changed
   2. Remove the Markdown files associated with the changed Notebooks from the given `md` folder(s)
   3. Open and save the linted Notebooks which will create a synced Markdown-version of the Notebook.
   4. Commit + Push all the changes to Github

## Build PDF of the book

### Installations

TexLive installation on Ubuntu (and Windows WSL):
```
$ sudo apt-get install texlive-latex-recommended texlive-fonts-recommended texlive-latex-extra latexmk
```

Python environment for the book is in `ci/py38-book-building.yaml`

### Building the PDF from the contents

There is a [separate project (private)](https://github.com/Python-GIS-book/book-building) that is used to automate the book building using CRC Latex template.
This repo is only available for authors due to contract with the publisher. If you have a similar book project with CRC,
you can contact the authors to get help with building the formatted book based on Jupyter notebooks.   

## Footnotes

[^url1]: https://python.org
