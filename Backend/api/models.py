from . import db

class Namespace(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    arn = db.Column(db.String(255), nullable=False)
    value = db.Column(db.String(255))
    resource_type = db.Column(db.String(80))
    namespace = db.Column(db.String(80), db.ForeignKey('namespace.name'), nullable=False)

    def __repr__(self):
        return f'<Resource {self.name}>'
