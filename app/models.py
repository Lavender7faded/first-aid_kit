from app import db
from datetime import datetime, timezone

class Medicine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    expiration_date = db.Column(db.Date, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)

    def __repr__(self):
        return f'<Medicine {self.name}>'

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), default=datetime.now(timezone.utc))
