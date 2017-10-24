"""Custom SQLAlchemy types / variants

Use mysql.LONGTEXT instead of mysql.TEXT for UnicodeText type
"""
from sqlalchemy.dialects import mysql

from extrapypi.extensions import db


UnicodeText = db.Text(convert_unicode=True)
UnicodeText = UnicodeText.with_variant(mysql.LONGTEXT(convert_unicode=True), 'mysql')
