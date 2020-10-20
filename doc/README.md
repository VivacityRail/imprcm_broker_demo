# IMPRCM Documentation - source

This repository contains the source code for documentation and guidance on use of the T1010 toolkit. The source documents are in the ```docs``` folder. 

This is a Sphinx project with files written in ReStructured Text. (https://www.sphinx-doc.org/en/master/)

There is a quick guide to RST syntax here: http://docutils.sourceforge.net/docs/user/rst/quickref.html

The list of directives (``` .. something:: ```) is here: http://docutils.sourceforge.net/docs/ref/rst/directives.html

You can edit the RST files in any decent text editor. **Atom** (https://atom.io/) and Sublime Text (££) (https://www.sublimetext.com/) work in both Windows and Linux; **notepad++** (https://notepad-plus-plus.org/) is Windows-only. All these editors have plugins / extensions to support syntax highlighting and previewing of RST.

Various features of Sphinx usefulto this project are documented in **docs/customisations.rst**.

To build and publish the documentation you need an appropriate Python virtual environment, Sphinx and Docker to be installed.

Various scripts in this folder are used to build the documentation, run it in a local browser or upload it to a cloud-hosting location (Docker Cloud or Amazon AWS).

An automatic build using Jenkins will work if the build executes ```jenkins_build_docs.sh``` on a linux host.

Consult that script to see what commands you need to execute to build the documentation website and pdf copy from scratch. The built documentation ends up in a `_build` folder 
