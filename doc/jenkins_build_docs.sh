#!/bin/bash

# jenkins_build_docs.sh
# build documents using sphinx. Assumes python3, pip, virtualenv and pdflatex have been installed

# note pdflatex installed using instructions here: https://gist.github.com/rain1024/98dd5e2c6c8c28f9ea9d


# expects parameters
#  jkn_sphinx_sourcefolder - sphinx source folder relative to workspace root
#  jkn_sphinx_todos        - sphinx todos (1 or default 0)



echo Sphinx build - source folder: $JKN_SPHINX_SOURCEFOLDER todos: $JKN_SPHINX_TODOS

# set up the virtual environment if it doesn't exist
if [ ! -d "docsource/python_env" ]; then
          virtualenv docsource/python_env
fi
# Activate the virtual environment
source ./docsource/python_env/bin/activate

# ensure package requirements are satisfied. Note that requirements.txt can be edited if new pip 
pip install -q -r docsource/requirements.txt

# clear the _build folders (to get rid of spurious left-over files)
rm -rf $JKN_SPHINX_SOURCEFOLDER/_build
rm -rf $JKN_SPHINX_SOURCEFOLDER/_build_pdf

# Run Sphinx to build the files from the .rst files in docs to a pdf in docs/_build_pdf
sphinx-build -a -q -b latex -D todo_include_todos=$JKN_SPHINX_TODOS $JKN_SPHINX_SOURCEFOLDER $JKN_SPHINX_SOURCEFOLDER/_build_pdf

# run pdflatex (twice) on the tex file to build the pdf
cd $JKN_SPHINX_SOURCEFOLDER/_build_pdf

pdflatex ./IMPRCM_documentation.tex
pdflatex ./IMPRCM_documentation.tex

cp ./IMPRCM_documentation.pdf ../_static/downloads/pdf/



# Run Sphinx to build the files from the .rst files in docs to html in docs/_build

cd ../../..
sphinx-build -a -q -b html -D todo_include_todos=$JKN_SPHINX_TODOS $JKN_SPHINX_SOURCEFOLDER $JKN_SPHINX_SOURCEFOLDER/_build

# :: Deactivate the virtual environment
deactivate
