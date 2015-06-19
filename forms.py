from flask_wtf import Form
from wtforms import TextField, TextAreaField, FieldList, FormField, SelectField, HiddenField, BooleanField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from models import TeamsTable, DataTable, ConsultantsTable, getTeams, getConsultants

################
#### forms  ####
################

# some form of factory

class ModelFieldList(FieldList):
    def __init__(self, *args, **kwargs):         
        self.model = kwargs.pop("model", None)
        super(ModelFieldList, self).__init__(*args, **kwargs)
        if not self.model:
            raise ValueError("ModelFieldList requires model to be set")

    def populate_obj(self, obj, name):
        while len(getattr(obj, name)) < len(self.entries):
            newModel = self.model()
            db.session.add(newModel)
            getattr(obj, name).append(newModel)
        while len(getattr(obj, name)) > len(self.entries):
            db.session.delete(getattr(obj, name).pop())
        super(ModelFieldList, self).populate_obj(obj, name)

class ImportData(Form):
    # data_Id = IntegerField('Your Data ID is', default="", validators=[DataRequired()])
    patientData = TextAreaField('Patient data', default="", validators=[DataRequired()])

class TeamSelectSubmitForm(Form):
    """docstring for TeamSelectSubmitForm
This is used in the index view and on index.html. 
It pulls its data from the query factory getTeams
It includes a textbox so that view logic can either add a new team if none existing, or select the appropriate team
    """
    teamSelect = QuerySelectField(u'Team', query_factory=getTeams, get_label='teamName', allow_blank=True, blank_text=(u'Select Team, or enter new team'))
    teamSubmit = TextField('Enter a new team name', default="")

class TeamSelectForm(Form):
    """docstring for TeamSelectSubmitForm
This is used in the index view and on index.html. 
It pulls its data from the query factory getTeams
It includes a textbox so that view logic can either add a new team if none existing, or select the appropriate team
    """
    teamSelect = QuerySelectField(u'Team', query_factory=getTeams, get_label='teamName', allow_blank=False, blank_text=(u'Select Team'))

class ConsultantSelectForm(Form):
    """docstring for TeamSelectSubmitForm
This is used in the index view and on index.html. 
It pulls its data from the query factory getTeams
It includes a textbox so that view logic can either add a new team if none existing, or select the appropriate team
    """
    consultantSelect = QuerySelectField(u'Consultant', query_factory=getConsultants, get_label='consultant', allow_blank=False)



class PatientsForm(Form):
    patientName = HiddenField("Patient Name")
    background = TextAreaField("Background")
    issues = TextAreaField("Issues")
    plan = TextAreaField("Plan")
    jobs = TextAreaField("Jobs")
    reviewBy = SelectField("Review By", choices=[(c, c) for c in ['No Review', 'RMO', 'Registrar', 'Consultant']])
    reviewReason = TextField("Review Reason")
    def __init__(self, csrf_enabled=False, *args, **kwargs):
        super(PatientsForm, self).__init__(csrf_enabled=False, *args, **kwargs)

class DisplayDataForm(Form):
    teamName = TextField("Team Name")
    patients = ModelFieldList(FormField(PatientsForm), model=DataTable)