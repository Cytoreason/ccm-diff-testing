# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'py-project-template'
copyright = '2023, ron'
author = 'ron'
release = '0.1.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon', 'sphinxcontrib.confluencebuilder', ]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
root_doc = 'index'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

autoclass_content = 'both'

confluence_publish = True
confluence_space_key = 'AR'
# confluence_root_homepage = True
confluence_parent_page = '3737649246'
# confluence_publish_root="3737681967"
confluence_ask_password = True
# (for Confluence Cloud)
confluence_server_url = 'https://cytoreason.atlassian.net/wiki/'
confluence_server_user = 'ron.poches@cytoreason.com'

