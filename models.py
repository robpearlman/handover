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
    consultants = ConsultantsTable.query
    return consultants

class ConsultantsTable(db.Model):
    __tablename__ = "consultantsTable"
    id = db.Column(db.Integer, primary_key=True)
    consultant = db.Column(db.String, nullable=False)
    patients = db.relationship('DataTable', backref = db.backref('consultant'), order_by='DataTable.location') # many to one

    def __init__(self, consultant):
        self.consultant = consultant

    def __repr__(self):
        return '<Team ID %r>' % (self.id) #debugging purposes

class DataTable(db.Model):
    __tablename__ = "dataTable"
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teamsTable.id'))
    consultant_id = db.Column(db.Integer, db.ForeignKey('consultantsTable.id'))
    patientName = db.Column(db.String, nullable=False)
    mrn = db.Column(db.String, nullable=False)
    los = db.Column(db.String, nullable=True)
    age = db.Column(db.String, nullable=True)
    admissionReason = db.Column(db.String, nullable=True)
    location = db.Column(db.String, nullable=True)
    background = db.Column(db.String, nullable=True)
    issues = db.Column(db.String, nullable=True)
    plan = db.Column(db.String, nullable=True)
    jobs = db.Column(db.String, nullable=True)
    reviewBy = db.Column(db.String, nullable=True)
    reviewReason = db.Column(db.String, nullable=True)

    def __init__(self, team_id, consultant_id, patientName, mrn, los, age, admissionReason, location):
        self.team_id = team_id
        self.consultant_id = consultant_id
        self.patientName = patientName
        self.mrn = mrn
        self.los = los
        self.age = age
        self.admissionReason = admissionReason
        self.location = location

    def __repr__(self):
        return '<Patient ID %r>' % (self.id) #debugging purposes
