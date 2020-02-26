from flask import render_template, flash, redirect
from app.forms import fileSubmitForm
from ravenscout import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username' : 'ravenPrime'}
    return render_template('index.html', title='Home', user=user)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = fileSubmitForm()
    if form.validate_on_submit():
        flash('File submited under {} team {}'.format(form.name.data, form.team.data))
        return redirect('/index')
    return render_template('fileSubmit.html', title='Submit a file', form=form)
    