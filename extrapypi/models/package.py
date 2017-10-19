import datetime
from pkg_resources import parse_version

from extrapypi.extensions import db


package_maintainers = db.Table(
    'package_maintainers',
    db.Column('package_id', db.Integer, db.ForeignKey('package.id', name='_fk_package_maintainers_package')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', name='_fk_package_maintainers_user')),
)


class Package(db.Model):
    """Represent a simple package
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255, convert_unicode=True), nullable=False, unique=True)
    summary = db.Column(db.String(255, convert_unicode=True))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)

    maintainers = db.relationship('User', secondary=package_maintainers, lazy='dynamic', backref='packages')

    @property
    def sorted_releases(self):
        releases = self.releases.all()
        return sorted(
            releases,
            key=lambda r: parse_version(r.version),
            reverse=True
        )

    @property
    def latest_release(self):
        return next(iter(self.sorted_releases), None)

    def __repr__(self):
        return "<Package {0.name}>".format(self)
