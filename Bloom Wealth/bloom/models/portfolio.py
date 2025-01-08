from bloom import db
from datetime import datetime, timezone

class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    fund_name = db.Column(db.String(100), nullable=False)
    scheme_code = db.Column(db.String(100), nullable=False)
    units_owned = db.Column(db.Float, nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)
    investment_amount = db.Column(db.Float, nullable=False)
    current_value = db.Column(db.Float, nullable=False)
    purchase_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    last_updated = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f"<id: {self.id}><user: {self.user_id}><fund name: {self.fund_name}>"
