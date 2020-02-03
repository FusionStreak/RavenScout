from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, SelectField
from wtforms.validators import DataRequired

class fileSubmitForm(FlaskForm):
    name = StringField('Name: ', validators=[DataRequired()])
    email = StringField('E-mail: ', validators=[DataRequired()])
    team = StringField('Team Number: ', validators=[DataRequired()])
    event = StringField('Event Code(ex: ONOTT): ', validators=[DataRequired()])
    file = FileField('Upload CSV file here: ', validators=[DataRequired()])
    season = SelectField('Season: ', choices=[('Deep Space','2019'), ('Infinit Recharge', '2020')])
    submit = SubmitField('Submit')