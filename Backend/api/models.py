from datetime import datetime
from . import db

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    arn = db.Column(db.String(255), nullable=False)
    value = db.Column(db.String(255))
    resource_type = db.Column(db.String(255), nullable=False)
    namespace = db.Column(db.String(255), nullable=False)  # Add this line
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Resource {self.name}>"
