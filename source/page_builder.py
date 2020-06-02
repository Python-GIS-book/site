
import os
import glob
import subprocess

_dir_path = os.path.dirname(os.path.realpath(__file__))


def get_notebooks():
    notebooks = [f for f in glob.glob(os.path.join(_dir_path, "**", "*.ipynb",), recursive=True)]
    return notebooks


def convert_notebooks_to_rst(notebook_list):
    for nb in notebook_list:
        cmd = ["jupyter", "nbconvert", "--ClearOutputPreprocessor.enabled=True",
               nb, "--to", "rst"]
        print(cmd)
        subprocess.run(cmd)


def add_hypothesis_block(writer):
    codes = ['\n\n.. raw:: html\n',
             '    <script src="https://hypothes.is/embed.js" async> </script>',
             '\n'
             ]
    for line in codes:
        writer.write(line)


def add_binder_block(writer, notebook_relative_path):
    codes = ["\n.. image:: https://mybinder.org/badge_logo.svg\n",
             f"    :target: https://mybinder.org/v2/gh/Python-GIS-book/site/master?urlpath=lab/tree/{notebook_relative_path}",
             "\n\n"
             ]
    for line in codes:
        writer.write(line)


def convert_notebooks_to_jupyter_sphinx_rst(notebook_list):
    for nb in notebook_list:
        cmd = ["jupyter", "nbconvert", "--ClearOutputPreprocessor.enabled=True",
               nb, "--to", "rst"]
        print(f"Processing {os.path.basename(nb)} ..")
        subprocess.run(cmd)

        # Read rst file and convert (allow Exceptions)
        with open(nb.replace('.ipynb', '.rst'), 'r') as rst:
            lines = rst.readlines()
            converted_lines = []
            for line in lines:
                if line.startswith(".. code:: ipython3"):
                    # Convert to jupyter-execute
                    line = line.replace(".. code:: ipython3",
                                        ".. jupyter-execute::\n    :raises:\n")

                converted_lines.append(line)

        # Write
        with open(nb.replace('.ipynb', '.rst'), 'w') as rst:
            for line in converted_lines:
                rst.write(line)

if __name__ == "__main__":

    notebooks = get_notebooks()
    if len(notebooks) > 0:
        convert_notebooks_to_jupyter_sphinx_rst(notebooks)
