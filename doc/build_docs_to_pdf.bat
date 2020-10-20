@echo off
:: windows batch file to build documentation using sphinx, creating a pdf

:: prerequisites: Sphinx, Sphinx bootstrap theme

:: parameters:
:: 
:: 1 - source folder
:: 2 - name of the master document to use
:: 3 - todos setting 1 = include todos, 0 = don't

SETLOCAL 

SET sourcefolder=%1
SET master_docname=%2
SET todos=%3
:: SET 
IF ""%todos%=="" (SET todos=0)
SET me=%~n0



@echo %me%: building docs from source folder %sourcefolder% to document %master_docname% with todos option %todos%
@echo .

:: Activate the virtual environment
call python_env\scripts\activate.bat

:: ensure package requirements are satisfied. Note that requirements.txt can be edited if new versions of packages are required
pip install -q -r requirements.txt

:: Run Sphinx to build the files from the .rst files in docs to latex in docs/_build
sphinx-build -a -E -b latex  %sourcefolder% %sourcefolder%/_pdf_build
:: Run pdflatex to create the pdf
cd %sourcefolder%/_pdf_build
cd
:: so good you want to run it twice (this is so that it picks up cross-refs and contents defs created in the first pass)
pdflatex ./%master_docname%.tex
pdflatex ./%master_docname%.tex

copy .\%master_docname%.pdf ..\_static\downloads\pdf

:: Deactivate the virtual environment
deactivate
