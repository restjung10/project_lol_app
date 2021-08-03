from app import db

class League(db.Model):
    __tablename__ = 'league'
    
    id = db.Column(db.Integer, primary_key=True)
    ids_id = db.Column(db.String(128), db.ForeignKey('ids.id'), nullable=False)
    queueType = db.Column(db.String(128), nullable=False)
    tier = db.Column(db.String(128), nullable=False)
    rank = db.Column(db.String(32), nullable=False)
    wins = db.Column(db.Integer, nullable=False)
    losses = db.Column(db.Integer, nullable=False)
    leaguePoints = db.Column(db.Integer, nullable=False)

    ids = db.relationship('IDs', back_populates='leagues')

    def __repr__(self):
        return f"id_league {self.id}"
