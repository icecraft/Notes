# -*- coding: utf-8 -*
from flask import render_template, redirect, request, url_for, flash, current_app
from flask.ext.login import login_user, logout_user, login_required, \
    current_user
from .. import db
from ..models import Diary, Year, Month, Week
from datetime import datetime
from .forms import DiaryForm
from . import diary

@diary.route('/show_year', defaults={'year':datetime.utcnow().year}, methods=['GET', 'POST'])
@diary.route('/show_year/<int:year>', methods=['GET', 'POST'])
def show_year(year):
    showYear = Year.query.filter_by(year=year).first_or_404()
    return render_template('diary/show_year.html', year=showYear)

@diary.route('/current_week', methods=['GET', 'POST'])
def current_week():
    today = datetime.utcnow()
    indexInYear = Diary.getIndexInYear(today.year, today.month, today.day)
    this_week = reduce(lambda x,y : x if y.week.month.year.year != today.year else y.week,
                    Diary.query.filter_by(indexInYear=indexInYear), None )
    return redirect(url_for('diary.show_week', id=this_week.id))
    

@diary.route('/show_month/<int:id>', methods=['GET', 'POST'])
def show_month(id):
    month = Month.query.filter_by(id=id).first_or_404()
    return render_template('diary/show_month.html', month=month)

@diary.route('/show_week/<int:id>', methods=['GET', 'POST'])
def show_week(id):
    week = Week.query.filter_by(id=id).first_or_404()
    return render_template('diary/show_week.html', week=week)

@diary.route('/show_diary/<int:id>', methods=['GET', 'POST'])
def show_diary(id):
    diary = Diary.query.filter_by(id=id).first_or_404()
    return render_template('diary/show_diary.html', diary=diary)

@diary.route('/edit_diary/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_diary(id):
    diary = Diary.query.filter_by(id=id).first_or_404()
    form = DiaryForm()

    if form.validate_on_submit():
        diary.contents=form.body.data
        diary.lastupdate_timestamp = datetime.utcnow()        
        db.session.add(diary)
        db.session.commit()
        """ only insert data to sql table can trigger the action to generate an unique ID"""
        return redirect(url_for('diary.show_week', id=diary.week.id))
    
    form.body.data = diary.contents
    return render_template("diary/edit_diary.html", form=form)

