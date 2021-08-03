from app import db

class Win(db.Model):
    __tablename__ = 'win'
    
    id = db.Column(db.Integer, primary_key=True)
    acc_id = db.Column(db.String(128), nullable=False)
    win_lose = db.Column(db.String(32), nullable=False)
    ids_id = db.Column(db.String(128), db.ForeignKey('ids.id'))

    accs = db.relationship('IDs', back_populates='wins')

    def __repr__(self):
        return f"Win {self.acc_id}"
