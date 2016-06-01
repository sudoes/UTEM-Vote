from flask import render_template, flash, redirect, session, url_for, request
from app import app, db
from .forms import LoginForm
from datetime import datetime


from app.models.appmodels import Admins, Candidate

voteEnable = False
campaign = 'UTeM 2016'


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title='Page Not Found'), 404

@app.route('/')
def index():
    if (voteEnable):
        sdata = {
            'name': campaign,
            'voting': voteEnable,
            'time': datetime.now()
        }
        return render_template("index.html", title='Home', posts=sdata)
    else:
        sdata = {'name': None, 'voting': voteEnable, 'time': datetime.now()}
        return render_template("index.html", title='Home', posts=sdata)


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', title='Admin Login')


@app.route('/vote')
def vote():
    candidates = db.session.query(Candidate).all()
    return render_template('vote.html', title='Vote', vote=voteEnable, users=candidates)

@app.route('/disable')
def disableVote():
    global voteEnable
    voteEnable = False
    flash('Voting is disabled')
    return redirect(url_for('index'))

@app.route('/enable')
def enableVote():
    global voteEnable
    voteEnable = True
    flash('Voting is enabled')
    return redirect(url_for('index'))

@app.route('/admin')
def adminPanel():
    global voteEnable
    global campaign
    candidates = db.session.query(Candidate).all()

    return render_template('admin_panel.html', title='Admin Panel', voteStatus=voteEnable, campaign=campaign, users=candidates)

@app.route('/updatecamp', methods=['POST'])
def updateCampaign():
    global campaign
    campaign = request.form['campaignName']
    flash('Campaign Name changed succesfully')
    return redirect(url_for('adminPanel'))

@app.route('/delcandidate', methods=['POST'])
def deleteCandidate():
    userid = request.form['userid']
    name = Candidate.query.filter(Candidate.id==userid).all()
    Candidate.query.filter(Candidate.id==userid).delete()
    flash('User ' + str(name[0]) + ' deleted!')
    db.session.commit()
    return redirect(url_for('adminPanel'))