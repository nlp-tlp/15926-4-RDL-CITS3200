from app import db


class ApiData(db.Model):
    id = db.Column(db.String, primary_key=True)  # Primary key
    label = db.Column(db.String, nullable=False)  # Not nullable
    type = db.Column(db.String, nullable=False)  # Not nullable
    definition = db.Column(db.Text)  # Optional text field
    parentId = db.Column(db.String)  # Optional field
    spreadsheetId = db.Column(db.String)  # Optional field
    spreadsheetLabel = db.Column(db.String)  # Optional field
    deprecationDate = db.Column(db.String)  # Optional field

    def __repr__(self):
        return f"<ApiData {self.label}>"
