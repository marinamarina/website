from datetime import datetime
from flask import render_template, redirect, url_for, session, flash, current_app
from flask_login import login_required
from . import main
from .forms import NameForm
from .. import db
from ..models import User
from ..email import send_email
from ..decorators_me import permission_required, templated
import os
from ..football_api.football_api_parser import FootballAPIWrapper
from ..models import Permission

@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission, pokus='keek')

#route decorators
@main.route('/')
@main.route('/index')
@templated()
def index():
    #from .. import config
    #print config['default'].FOOTY_ADMIN
    name = None
    return dict(current_time=datetime.utcnow(), name=session.get('name'))

@main.route('/aboutMe', methods=['GET', 'POST'])
@login_required
@templated()
def aboutMe():
    form = NameForm()

    # is the form input valid?
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()

        # add a new user and send an email to the admin
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)

            session['known'] = False
            print 'This is %r' % current_app.config['MAIL_PASSWORD']

            if current_app.config['FOOTY_ADMIN']:
                send_email(current_app.config['FOOTY_ADMIN'], 'New User','mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data

        # prevent form resubmission
        return redirect(url_for('.index'))
    return dict(form=form, name=session.get('name'), known=session.get('known', False))

@main.route('/leagueTable')
@templated()
def leagueTable():
    table = dict()
    # example usage
    wrap = FootballAPIWrapper()
    # set the api key
    wrap.api_key = '2890be06-81bd-b6d7-1dcb4b5983a0'
    league_table = wrap.league_table

    my_team_id = '9427'
    try:
        for key, value in league_table.items():
            print value.position
            return dict(league_table=wrap.league_table)

    except Exception:
        return redirect(url_for('main.index'))


@main.route('/admin', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.ADMINISTER)
@templated()
def admin():
    pass

@main.route('/moderators', methods=['GET', 'POST'])
@login_required
#@permission_required(Permission.MODERATE_COMMENTS)
def moderators():
    return 'Only for moderators'
