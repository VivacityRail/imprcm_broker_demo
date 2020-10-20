# autobuild command to build docs and serve on localhost:8083
# Needs autobuild to be installed and added to path. see wiki under Sphinx for details 
# https://github.com/VivacityRail/ImpRCM/wiki/Sphinx#auto-running-sphinx

# clear the _build folder
Remove-Item docs/_build -recurse

# build
sphinx-autobuild -a -b html -p 8083 -D todo_include_todos=1 -N -q -i docs/_pdf_build -E docs docs/_build