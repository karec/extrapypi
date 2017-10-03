from extrapypi.extensions import db


class Classifier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255, convert_unicode=True), nullable=False)
    category = db.Column(db.String(80, convert_unicode=True), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('classifier.id', name='_fk_classifier_parent'))

    parent = db.relationship("Classifier", remote_side=[id], backref="childs")

    def __repr__(self):
        return "<Classifier {} :: {}>".format(self.category, self.name)
