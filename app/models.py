from datetime import datetime
from ravenscout import db

class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, index=True, default=datetime.utcnow)
    fileName = db.Column(db.String(64), index=True, unique=True)
    event = db.Column(db.String(6), index=True, unique=False)
    team = db.Column(db.Integer, index=True, unique=False)
    name = db.Column(db.String(64), index=True, unique= False)
    season = db.Column(db.Integer)
    
    def __repr__(self):
        return '<File {}>'.format(self.fileName)

class infiniteRechargeParsedData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('files.id'))
    file_event = db.Column(db.String(6), db.ForeignKey('files.event'))
    match = db.Column(db.Integer) # Match Number
    alliance = db.Column(db.Boolean) # Alliance, blue is True, red is False
    team = db.Column(db.Integer) # Team number
    driverPos = db.Column(db.Integer) # Driver Position, pulled from FMS
    leftLine = db.Column(db.Boolean) # Left Auto line, pulled from FMS
    autoHigh = db.Column(db.Integer) # How many balls in high goal in auto
    autoMid = db.Column(db.Integer) # How many balls in mid goal in auto
    autoLow = db.Column(db.Integer) # How many balls in low goal in auto
    teleHigh = db.Column(db.Integer) # How many balls in high goal in teleop
    teleMid = db.Column(db.Integer) # How many balls in mid goal in teleop
    teleLow = db.Column(db.Integer) # How many balls in low goal in teleop
    rotateCP = db.Column(db.Boolean) # If they rotated the Control Panel 3-5 times
    positionCP = db.Column(db.Boolean) # If they positioned the Control Panel under right colour
    matchScore = db.Column(db.Integer) # Moatch final score, pulled from FMS
    scoreContributed = db.Column(db.Integer) # Amount of points made by team, calculated

    def __repr__(self):
        return '<InfiniteRechargeData {}>'.format(self.id)