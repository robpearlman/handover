from rounds import db


################
#### models ####
################

class TeamsTable(db.Model):
    __tablename__ = "teamsTable"
    id = db.Column(db.Integer, primary_key=True)
    teamName = db.Column(db.String, nullable=False)
    patients = db.relationship('DataTable', backref = db.backref('team'), order_by='DataTable.patientName') # many to one

    def __init__(self, teamName):
        self.teamName = teamName

    def __repr__(self):
        return '<Team ID %r>' % (self.id) #debugging purposes

# create teamsQuery to feed to SelectTeamsDropdown
def getTeams():
    teams = TeamsTable.query
    return teams

def getConsultants():
    consultants = DataTable.query
    return consultants

class DataTable(db.Model):
    __tablename__ = "dataTable"
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teamsTable.id'))
    patientName = db.Column(db.String, nullable=False)
    mrn = db.Column(db.String, nullable=False)
    los = db.Column(db.String, nullable=True)
    age = db.Column(db.String, nullable=True)
    admissionReason = db.Column(db.String, nullable=True)
    attending = db.Column(db.String, nullable=True)
    location = db.Column(db.String, nullable=True)
    background = db.Column(db.String, nullable=True)
    issues = db.Column(db.String, nullable=True)
    plan = db.Column(db.String, nullable=True)
    reviewBy = db.Column(db.String, nullable=True)
    reviewReason = db.Column(db.String, nullable=True)

    def __init__(self, team_id, patientName, mrn, los, age, admissionReason, attending, location):
        self.team_id = team_id
        self.patientName = patientName
        self.mrn = mrn
        self.los = los
        self.age = age
        self.admissionReason = admissionReason
        self.attending = attending
        self.location = location

    def __repr__(self):
        return '<Patient ID %r>' % (self.id) #debugging purposes

# to delete
class Item(db.Model):
    

    item_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    mrn = db.Column(db.String, nullable=False)
    patientNotes = db.Column(db.String, nullable=True)
    attending = db.Column(db.String, nullable=True)
    ward = db.Column(db.String, nullable=True)
    bed = db.Column(db.String, nullable=True)
    data_id = db.Column(db.Integer, nullable=False)

    def __init__(self, firstname, mrn, patientNotes, attending, ward, bed, data_id):
        self.firstname = firstname
        self.mrn = mrn
        self.patientNotes = patientNotes
        self.attending = attending
        self.ward = ward
        self.bed = bed
        self.data_id = data_id