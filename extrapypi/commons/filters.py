"""Jinja2 additionnal filters
"""
from docutils.core import publish_parts


def tohtml(s):
    """Convert rst string to raw html

    Used for display long description of releases
    """
    return publish_parts(s, writer_name='html')['body']
