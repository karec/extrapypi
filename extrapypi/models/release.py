import datetime

from extrapypi.extensions import db
from extrapypi.models.types import UnicodeText


class Release(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(UnicodeText, nullable=False)
    download_url = db.Column(db.String(2048, convert_unicode=True))
    home_page = db.Column(db.String(2048, convert_unicode=True))
    version = db.Column(db.String(80, convert_unicode=True))
    keywords = db.Column(db.String(255, convert_unicode=True))
    md5_digest = db.Column(db.String(32), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)

    package_id = db.Column(
        db.Integer,
        db.ForeignKey('package.id', name='_fk_release_package'), nullable=False
    )

    package = db.relationship(
        'Package',
        backref=db.backref(
            'releases',
            lazy='dynamic',
            cascade='all, delete-orphan'
        ),
        lazy='joined',
    )

    def __repr__(self):
        return "<Release {0.version} for package {0.package.name}>".format(self)
