# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = docs

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

.PHONY: pages
pages:
	@echo
	@echo "Building pages with Jupyter-Sphinx."
	@echo "-----------------------------------"
	python ./$(SOURCEDIR)/page_builder.py
	make html


.PHONY: book
book:
	@echo
	@echo "Building pages with Sphinx."
	@echo "-----------------------------------"
	make clean
	make html
	make html
	# Remove unnecessary directories
	rm -rf docs/doctrees docs/jupyter_execute
	# Move files level up from html directory
	mv docs/html/* docs/
	rm -r docs/html
	# Create NoJekyll
	touch docs/.nojekyll
    # Create CNAME for pythongis.org (points Github Pages to that domain)
	echo 'pythongis.org' > docs/CNAME

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
