# How to develop contents to this book project? - Guidelines

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
 3. [Jupytext](https://github.com/mwouts/jupytext) - Converts the notebooks into markdown and **allows us to better use GitHub diff functionalities**
    - *We should always commit the files into GitHub in Markdown/Jupytext format!* : There is a custom `make upload <target_branch>` command for this.

## Pipeline - How to create content?

The materials for the book are organized under different chapters. 

### To produce the content:
 
 1. Add your Jupyter notebook under the folder where your content belongs
 2. Name your file in an intuitive manner, and include chapter numbering, e.g. `2-1_intro-to-data-analysis-with-pandas.ipynb`
 3. Write contents into this notebook as you would do normally. Remember to use [MyST markdown syntax](https://jupyterbook.org/content/myst.html) for enriching the contents with Jupyter Book functionalities.

### To build local version of the docs:

Once you have written materials, and you want to see the results **live**, you can build and see the local version of the documentation by:

 1. Build the docs with `$ make html` (with sphinx-book-theme) or `$ jb build /source`
 2. You can see the docs under `_build/html` directory
    - with `sphinx-book-theme` this directory is located in the root of the project
    -  with `Jupyter Book` this directory is located in the `source` directory. 

### To upload the contents to GitHub:

Once you are happy with the contents, you can upload the contents to GitHub into the `<chapter>` branch (see docs about our [branching workflow below](#ask-for-a-review-by-making-a-pull-request)).
The materials should be uploaded in **markdown format**. We use Jupytext to convert the notebooks to markdown (and back). 
For making this process as easy as possible, we have a custom command that does all this work for us:

To push your changes to branch `chapter2`, execute: 

 - `$ make upload chapter2`
 
The `chapter` branch can be also any other name. If a branch with given name does not exist, 
it will be created before uploading the materials.
 
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

**Why not merging to master straight away?**

The master branch is facing the "outside" world. Hence, it is reserved for contents that are in a "publishable state". Once we
think that we want to publish the materials (e.g. for asking comments from "public"), we certainly can do that. But by default,
master is to be used only when we want to publish something, and send materials to "production".  