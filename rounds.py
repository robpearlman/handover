#rounds.py

# ToDo
#
# 2. 'whole list' view with PDF export and colour for urgency, filtered by ward, review person
# done?
# Filter information entery by location
# Print PDF list for consultant review only, filtered by ward location
# Filter entire list by ward location

#################
#### imports ####
#################
from flask import Flask, flash, redirect, render_template, session, url_for, request, make_response
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from functools import wraps
import os.path as op
from sqlalchemy import desc, asc


import pdb

################
#### config ####
################

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from models import TeamsTable, DataTable, ConsultantsTable
from forms import TeamSelectSubmitForm, ConsultantSelectForm, TeamSelectForm, ImportData, DisplayDataForm


from xhtml2pdf import pisa
from StringIO import StringIO

def create_pdf(pdf_data):
    pdf = StringIO()
    pisa.CreatePDF(StringIO(pdf_data), pdf)
    return pdf



################
#### routes ####
################

@app.route('/', methods=['GET', 'POST'])
def index():
    #pdb.set_trace()
    error = None
    form = TeamSelectSubmitForm(request.form)
    if request.method == 'POST':
        if form.teamSelect.data:
            return redirect(url_for('submitTeamData', team_id = form.teamSelect.data.id))
        elif form.teamSubmit.data:
            # add the team!
            new_team = TeamsTable(form.teamSubmit.data)
            db.session.add(new_team)
            db.session.commit()
            flash('Team added')
            return redirect(url_for('submitTeamData', team_id = new_team.id))
        else:
            return render_template("index.html", form=form, error=error)
    if request.method == 'GET':
        return render_template("index.html", create_form=form, submit_form=TeamSelectForm(), consultant_form=ConsultantSelectForm())


#<!-- For initial import of data, creation of new team, or to 
#  update a list with new patients and remove those who are 
#  not included in the new lost  -->
@app.route('/team_data/<int:team_id>', methods=['GET', 'POST'])
def submitTeamData(team_id):
    #pdb.set_trace()
    error = None
    form = ImportData(request.form)
    skipDelete = False
    team = db.session.query(TeamsTable).filter_by(id=team_id).first()
    if request.method == 'POST':
        if form.validate_on_submit():
            addData(form.patientData.data, team_id, skipDelete)
            flash('data imported and updated')
            return redirect(url_for('reviewTeamData', team_id=team_id))
        else:
            return render_template("data_entry.html", form=form, team=team, error=error)
    if request.method == 'GET':
        return render_template("data_entry.html", form=form, team=team, team_id=team_id)

# <!-- Update the list by adding new patients to the team. Redirects to 'addNewTeamData'-->
@app.route('/add_team_data/', methods=['GET', 'POST'])
def addNewTeamDataFromIndex():
    form = TeamSelectForm(request.form)
    if request.method == 'POST':
        # needs to display a import form
        # then open review data
        if form.teamSelect.data:
            return redirect(url_for('addNewTeamData', team_id = form.teamSelect.data.id))
    else:
        flash('You have not selected a team')
        return redirect(url_for('index'))

@app.route('/team_data/add_new/<int:team_id>', methods=['GET', 'POST'])
def addNewTeamData(team_id):
    #pdb.set_trace()
    error = None
    form = ImportData(request.form)
    team = db.session.query(TeamsTable).filter_by(id=team_id).first()
    skipDelete = True
    if request.method == 'POST':
        if form.validate_on_submit():
            addData(form.patientData.data, team_id, skipDelete)
            flash('data imported and updated')
            return redirect(url_for('reviewTeamData', team_id = team_id))
        else:
            return render_template("data_add_entry.html", form=form, team=team, error=error)
    if request.method == 'GET':
        return render_template("data_add_entry.html", form=form, team=team, team_id = team_id) 

# <!-- Edits patient data for a team -->  
@app.route('/edit_team_data/', methods=['GET', 'POST'])
def reviewTeamDataFromIndex():
    # This endpoint should redirect to the review page, endpoint 'reviewTeamData'
    form = TeamSelectForm(request.form)
    if request.method == 'POST':
        if form.teamSelect.data:
            return redirect(url_for('reviewTeamData', team_id = form.teamSelect.data.id))
    else:
        flash('You have not selected a team')
        return redirect(url_for('index'))

@app.route('/team_data/review/<int:team_id>', methods=['GET', 'POST'])
def reviewTeamData(team_id):
    #pdb.set_trace()
    team = db.session.query(TeamsTable) \
        .filter_by(id=team_id).first()
    if request.method == 'POST':
        form = DisplayDataForm(request.form)
        # by populatingobj with form.populate_obj team name is lost
        # for reasons I can't yet determine
        # so we need to replace it
        teamName = team.teamName
        form.populate_obj(team)
        team.teamName = teamName
        db.session.commit()
        return render_template("data_review.html", form = form, team = team)
    if request.method == 'GET':
        form = DisplayDataForm(obj = team)
        return render_template("data_review.html", form = form, team = team)

# <!-- View List Endpoints -->  
@app.route('/view_complete_list/')
def viewList():
    patients = db.session.query(DataTable) \
        .order_by(DataTable.reviewBy.asc(),DataTable.location.desc()). \
        all()
    pdf = create_pdf(render_template('pdf_complete_list.html', patients=patients))
    response = make_response(pdf.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=%s.pdf' % 'yourfilename'
    return response

#############
@app.route('/view_consultant_list/', methods=['GET', 'POST'])
def redirectConsultantList():
    # This endpoint should redirect to the viewConsultantList page
    form = ConsultantSelectForm(request.form)
    if request.method == 'POST':
        if form.consultantSelect.data:
            return redirect(url_for('viewConsultantList', consultant_id = form.consultantSelect.data.id))
    else:
        flash('You have not selected a consultant')
        return redirect(url_for('index'))

@app.route('/view_consultant_list/<int:consultant_id>')
def viewConsultantList(consultant_id):
    patients = db.session.query(DataTable) \
        .filter_by(consultant_id=consultant_id) \
        .order_by(DataTable.reviewBy.asc(),DataTable.location.desc()). \
        all()
    pdf = create_pdf(render_template('pdf_generic_list.html', patients=patients, title = patients[0].consultant.consultant))
    response = make_response(pdf.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=%s.pdf' % 'yourfilename'
    return response
#############

#############
@app.route('/view_team_list/', methods=['GET', 'POST'])
def redirectTeamList():
    # This endpoint should redirect to the viewTeamList page
    form = TeamSelectForm(request.form)
    if request.method == 'POST':
        if form.teamSelect.data:
            return redirect(url_for('viewTeamList', team_id = form.teamSelect.data.id))
    else:
        flash('You have not selected a team')
        return redirect(url_for('index'))

@app.route('/view_team_list/<int:team_id>')
def viewTeamList(team_id):
    patients = db.session.query(DataTable) \
        .filter_by(team_id=team_id) \
        .order_by(DataTable.reviewBy.asc(),DataTable.location.desc()). \
        all()
    pdf = create_pdf(render_template('pdf_generic_list.html', patients=patients, title = patients[0].team.teamName))
    response = make_response(pdf.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=%s.pdf' % 'yourfilename'
    return response
#############

#################
#### methods ####
#################

def addData(data, team_id, skipDelete):
    #pdb.set_trace()
    from StringIO import StringIO
    inputIO = StringIO(data)
    import csv
    mrnList = [] # collect a list of the patients
    for line in csv.reader(inputIO, delimiter='\t'):
        print line
        patient = db.session.query(DataTable).filter_by(mrn=line[4]).first()
        if patient:
            # The following if consultant and if statement are
            # ripe for optimisation/moving into their own module
            # it checks the consultant name and creates a new one if there's nothing
            # there etc
            consultant = db.session.query(ConsultantsTable).filter_by(consultant=line[5]).first()
            if consultant:
                # costs nothing to re-save existing consultant
                patient.consultant = consultant.id
            else:
                # consultant doesn't exist
                new_consultant = ConsultantsTable(line[5])
                db.session.add(new_consultant)
                db.session.commit()
                patient.consultant = new_consultant.id

            # only update details if the patient already exists
            mrnList.append(line[4])
            patient.los = line[9]
            # patient.attending = line[5]
            patient.location = line[3]
            patient.team_id = team_id
            print 'updated ' + patient.patientName
        else:
            # if the patient doesn't exist then it will add it
            # Order is(team_id, patientName, mrn, los, age, admissionReason, attending, location)
            
            consultant = db.session.query(ConsultantsTable).filter_by(consultant=line[5]).first()
            if consultant:
                # costs nothing to re-save existing consultant
                pass
            else:
                # consultant doesn't exist
                consultant = ConsultantsTable(line[5])
                db.session.add(consultant)
                db.session.commit()

            mrnList.append(line[4])
            new_patient = DataTable(team_id, consultant.id, line[2], line[4], line[9], line[6], line[10], line[3])            
            db.session.add(new_patient)
            db.session.commit()
            print 'added ' + new_patient.patientName
        # now delete all records for the team that are not in MRNList,
        # but only if it is called from submitTeamData
    pdb.set_trace()
    if skipDelete == False:
        team = db.session.query(TeamsTable).filter_by(id=team_id).first()
        for patient in team.patients:
            try:    
                mrnList.index(patient.mrn)
            except ValueError:
                db.session.delete(patient)
                print 'deleted ' + patient.patientName
                db.session.commit()

