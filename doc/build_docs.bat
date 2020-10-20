@echo off
:: windows batch file to build documentation using sphinx

:: prerequisites: Sphinx, Sphinx bootstrap theme

:: parameters:
:: 
:: 1 - source folder

SETLOCAL 

SET sourcefolder=%1
SET todos=%2
IF ""%todos%=="" (SET todos=0)
SET me=%~n0



@echo %me%: building docs from source folder %sourcefolder% with todos option %todos%
@echo .

:: Activate the virtual environment
call python_env\scripts\activate.bat

:: ensure package requirements are satisfied. Note that requirements.txt can be edited if new versions of packages are required
pip install -q -r requirements.txt

:: Run Sphinx to build the files from the .rst files in docs to html in docs/_build
sphinx-build -a -E -b html -D todo_include_todos=%todos% %sourcefolder% %sourcefolder%/_build

:: Deactivate the virtual environment
deactivate
