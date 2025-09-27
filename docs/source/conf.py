<<<<<<< HEAD
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

project = 'Assgn3'
copyright = '2025, Nour Shammaa'
author = 'Nour Shammaa'
version = '1.0'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',]
autodoc_default_options = {
    'members': True,
    'undoc-members': True,      
    'show-inheritance': True,
}
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme' 
html_static_path = ['_static']
=======
import os
import sys

# Add the Lab4 root (where pyqt_app_database.py, models.py, database.py are)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


project = 'School Management System'
copyright = '2025, Riwa El Kari'
author = 'Riwa El Kari'
release = '1.0.0'

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
]

# Default options for autodoc
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}

# Mock PyQt5 so docs build without GUI
autodoc_mock_imports = ["PyQt5"]

templates_path = ["_templates"]
exclude_patterns = []
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
>>>>>>> main
