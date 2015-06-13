#rounds.py

# ToDo
#
# 1. Select box for who is going to review people
# 2. 'whole list' view with PDF export and colour for urgency, filtered by ward, review person
# 3. option to add new patients for a team, or ?for replacement of old patients
# done?
#

#################
#### imports ####
#################
from flask import Flask, flash, redirect, render_template, session, url_for, request, make_response
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from functools import wraps
import os.path as op

import pdb

################
#### config ####
################

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from models import TeamsTable, DataTable, Item, getTeams
from forms import TeamSelectSubmitForm, ImportData, DisplayDataForm


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
        return render_template("index.html", form=form)

@app.route('/team_data/<int:team_id>', methods=['GET', 'POST'])
def submitTeamData(team_id):
    print 'runnning'
    pdb.set_trace()
    error = None
    form = ImportData(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            from StringIO import StringIO
            inputIO = StringIO(form.patientData.data)
            import csv
            for line in csv.reader(inputIO, delimiter='\t'):
                if len(line) < 2:
                    continue
                print line  
                new_patient = DataTable(team_id, line[5], line[6], line[7], line[8], line[16], line[15], 'Ward X Bed ' + line[4])            
                db.session.add(new_patient)
                db.session.commit()
            flash('data imported. Now use your app to import')
            return redirect(url_for('reviewTeamData', team_id = new_team.id))
        else:
            return render_template("data_entry.html", form=form, error=error)
    if request.method == 'GET':
        return render_template("data_entry.html", form=form, team_id = team_id)

@app.route('/team_data/review/<int:team_id>', methods=['GET', 'POST'])
def reviewTeamData(team_id):
    pdb.set_trace()
    team = db.session.query(TeamsTable).filter_by(id=team_id).first()
    form = DisplayDataForm(obj = team)
    if request.method == 'POST':
        #if form.validate_on_submit():
        form.populate_obj(team)
        db.session.commit()
        return render_template("data_review.html", form = form, team_id=team_id)
    if request.method == 'GET':
        return render_template("data_review.html", form = form, team_id=team_id)





