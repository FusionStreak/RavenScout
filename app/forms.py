from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired

class fileSubmitForm(FlaskForm):
    name = StringField('Name: ', validators=[DataRequired()])
    team = StringField('Team Number: ', validators=[DataRequired()])
    file = FileField('Upload CSV file here: ', validators=[DataRequired()])
    submit = SubmitField('Submit')