#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# test documentation build configuration file, created by
# sphinx-quickstart on Sat Nov 18 13:23:08 2017.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import re
import datetime

# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- General configuration ------------------------------------------------

# Bootstrap theme https://github.com/ryan-roemer/sphinx-bootstrap-theme
# Install using pip install sphinx_bootstrap_theme
import sphinx_bootstrap_theme

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
# extensions = ['sphinx.ext.todo', 'sphinxcontrib.openapi','sphinxcontrib.redoc',]
extensions = ['sphinx.ext.todo', 'sphinxcontrib.openapi',]



# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'IMP-RCM'
# PJ - make date live
copyright = '{0}, RSSB'.format(datetime.datetime.now().year)
author = 'Vivacity Rail Consulting Ltd for RSSB'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#

# PJ 20180823 get the version from the most recent git tag that looks like vxxxxxx (now with semver)
# git describe returns somethiing like "v1.1.3-rc1-2-gaabbccd" comprising tag, number of commits after tag, short commit hash
# We want to show version = 1.1 and release = 1.1.3-rc1+2 (aabbccd)
# Or if no commits after the tag, release = 1.1.3-rc1 (aabbcccd)
# or if tag is v1.2-0-gaabbccd then the release = 1.2 (aabbccd)

# git describe tells you the tag. The re strips the v from the front
tagstring = re.sub('^v', '', os.popen('git describe --tags --long').read().rstrip(), flags=re.IGNORECASE).split('-')

git_tag = '-'.join(tagstring[:-2]) # all but last 2 bits are elements of the tag
rel_offset = tagstring[-2] # 2nd last is the offset
git_commit = tagstring[-1].lstrip('g') # last is the commit id - we don't want the g

version = '.'.join(git_tag.replace('-','.').split('.')[0:2]) # just major.minor version. Replace "-" at start of possible "-rcxxx" so it doesn't get included

rel_offset = '' if rel_offset == '0' else '+' + rel_offset
release = '{0}{1} ({2})'.format(git_tag, rel_offset, git_commit)

# The short X.Y version.
# version = '0.1'
# The full version, including alpha/beta/rc tags.
# release = '0.1.1'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# prolog to declare some text-formatting roles
rst_prolog = '''
'''

# epilog shows the release number
# and includes a file of external links
rst_epilog = '''
.. include:: includes/external_links.txt

.. role:: strike


.. role:: tech-mand

.. role:: tech-rec

.. role:: tech-opt


.. raw:: html

   <script>
     $(document).ready(function() {
       $('.tech-mand').closest('td').addClass('tech-mand-parent');
       $('.tech-rec').closest('td').addClass('tech-rec-parent');
       $('.tech-opt').closest('td').addClass('tech-opt-parent');
     });
   </script>






.. only:: html

   release: |release|

'''

# numbered figures
numfig = True
numfig_format = {'figure': 'Figure %s', 'table': 'Table %s', 'code-block': 'Listing %s', 'section': 'Section %s'}
numfig_secnum_depth = 1

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'
html_theme = 'bootstrap'
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#

# logo
html_logo = "_static/rssb-white-logo-100mm.png"

# favicon
html_favicon = "_static/favicon.ico"

# sidebar
html_sidebars = {
   '**': ['globaltoc.html', 'searchbox.html'],
}


# extra styles / overrides
def setup(app):
    app.add_stylesheet("imp_rcm_overrides.css") # also can be a full URL
    # app.add_stylesheet("ANOTHER.css")
    # app.add_stylesheet("AND_ANOTHER.css")
	# Include extra javascript for page proofer (https://pageproofer.com/)
    app.add_javascript("pageproofer.js")

html_theme_options = {
    # Navigation bar title. (Default: ``project`` value)
    'navbar_title': " Cross-Industry RCM",

    # Tab name for entire site. (Default: "Site")
    'navbar_site_name': "Site Contents",

    # A list of tuples containing pages or urls to link to.
    # Valid tuples should be in the following forms:
    #    (name, page)                 # a link to a page
    #    (name, "/aa/bb", 1)          # a link to an arbitrary relative url
    #    (name, "http://example.com", True) # arbitrary absolute url
    # Note the "1" or "True" value above as the third argument to indicate
    # an arbitrary url.
    #'navbar_links': [
    #    ("Examples", "examples"),
    #    ("Link", "http://example.com", True),
    #],
	

    # Render the next and previous page links in navbar. (Default: true)
    'navbar_sidebarrel': False,

    # Render the current pages TOC in the navbar. (Default: true)
    'navbar_pagenav': True,

    # Tab name for the current pages TOC. (Default: "Page")
    'navbar_pagenav_name': "On this page",

    # Global TOC depth for "site" navbar tab. (Default: 1)
    # Switching to -1 shows all levels.
    'globaltoc_depth': 1,

    # Include hidden TOCs in Site navbar?
    #
    # Note: If this is "false", you cannot have mixed ``:hidden:`` and
    # non-hidden ``toctree`` directives in the same page, or else the build
    # will break.
    #
    # Values: "true" (default) or "false"
    'globaltoc_includehidden': "true",

    # HTML navbar class (Default: "navbar") to attach to <div> element.
    # For black navbar, do "navbar navbar-inverse"
    # 'navbar_class': "navbar navbar-inverse",

    # Fix navigation bar to top of page?
    # Values: "true" (default) or "false"
    'navbar_fixed_top': "true",

    # Location of link to source.
    # Options are "nav" (default), "footer" or anything else to exclude.
    'source_link_position': "not wanted",

    # Bootswatch (http://bootswatch.com/) theme.
    #
    # Options are nothing (default) or the name of a valid theme
    # such as "cosmo" or "sandstone".
    #
    # The set of valid themes depend on the version of Bootstrap
    # that's used (the next config option).
    #
    # Currently, the supported themes are:
    # - Bootstrap 2: https://bootswatch.com/2
    # - Bootstrap 3: https://bootswatch.com/3
    'bootswatch_theme': "yeti",

    # Choose Bootstrap version.
    # Values: "3" (default) or "2" (in quotes)
    'bootstrap_version': "3",
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# This is required for the alabaster theme
# refs: http://alabaster.readthedocs.io/en/latest/installation.html#sidebars
# html_sidebars = {
#    '**': [
#        'relations.html',  # needs 'show_related': True theme option to display
#        'searchbox.html',
#    ]
#}

html_last_updated_fmt = '%Y/%m/%d at %H:%M:%S'

# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'IMPRCM_doc'


# -- Options for LaTeX output ---------------------------------------------

#  generic options
latex_engine = 'pdflatex'
latex_show_pagerefs = True


#  latex_elements options
latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    'papersize': 'a4paper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    'pointsize': '10pt',

    #'fontpkg': '\\usepackage{opensans}',

    #'fncychap': '\\usepackage[Bjornstrup]{fncychap}',

    'extraclassoptions' : 'openany',

    # Additional stuff for the LaTeX preamble.
    #
    'preamble': r'''
\setcounter{tocdepth}{4}
\setcounter{secnumdepth}{4}
\pagenumbering{arabic} 
''',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    ('IMPRCM_documentation', 'IMPRCM_documentation.tex', 'IMPRCM Documentation', author, 'manual'),
]

latex_toplevel_sectioning = 'part'

# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'IMPRCM', 'IMPRCM Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'IMPRCM', 'IMPRCM Documentation',
     author, 'Vivacity Rail Consulting for RSSB', 'IMPRCM - use of T1010 Cross-industry RCM toolkit',
     'Miscellaneous'),
]

# stuff for redoc swagger renderer
redoc = [
    {
        'name': 'IMP-RCM API',
        'page': 'api',
        'spec': '_openapi/test_larger.yaml',
        'embed': True,
    },
    # {
    #     'name': 'Example API',
    #     'page': 'example/index',
    #     'spec': 'http://example.com/openapi.yml',
    #     'opts' {
    #         'lazy': False,
    #         'nowarnings': False,
    #         'nohostname': False,
    #         'required-props-first': True,
    #         'expand-responses': [200, 201],
    #     }
    # },
]


