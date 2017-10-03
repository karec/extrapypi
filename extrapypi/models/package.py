import os
import datetime

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
    def package_path(self, config):
        """Utility property, used to find directory of a package on the server,
        based on current app config

        :param dict config: current app configuration
        :return: path of the package on the server
        :rtype: str
        """
        return os.path.join(config['PACKAGES_ROOT'], self.name)

    def __repr__(self):
        return "<Package {name}>".format(self)
