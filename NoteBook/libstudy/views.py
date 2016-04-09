# -*- coding: utf-8 -*
from flask import render_template, redirect, request, url_for, flash, current_app
from flask.ext.login import login_user, logout_user, login_required, \
    current_user
from .. import db
from ..models import LibStudy
from . import libstudy
from datetime import datetime
from .forms import LibStudyForm, DEFAULT_LibStudy_Contents

@libstudy.route('/show_libstudy/<int:id>', methods=['GET', 'POST'])
def show_libstudy(id):
    libstudy = LibStudy.query.filter_by(id=id).first_or_404()
    return render_template('libstudy/show_libstudy.html', libstudy=libstudy)

@libstudy.route('/libstudies', methods=['GET', 'POST'])
def libstudies():
    page = request.args.get('page', 1, type=int)
    pagination = LibStudy.query.order_by(LibStudy.timestamp.desc()).paginate(
        page, per_page=current_app.config['INDEX_LIBSTUDIES_PER_PAGE'],
        error_out=False)
    libstudies = pagination.items
    return render_template('libstudy/libstudies.html', libstudies=libstudies,
                           pagination=pagination)


@libstudy.route('/add_libstudy', methods=['GET', 'POST'])
@login_required
def add_libstudy():
    form = LibStudyForm()
    if form.validate_on_submit():
        libstudy = LibStudy(contents=form.body.data,
                      libstudyname = form.libstudyname.data,
                      about_this = form.about_this.data,
                      author=current_user._get_current_object())
        db.session.add(libstudy)
        db.session.commit()
        """ only insert data to sql table can trigger the action to generate an unique ID"""
        id = LibStudy.query.order_by(LibStudy.timestamp.desc()).first().id
        return redirect(url_for('libstudy.show_libstudy', id=id))
    
    form.body.data =  DEFAULT_LibStudy_Contents
    return render_template("libstudy/add_libstudy.html", form=form)

@libstudy.route('/edit_libstudy/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_libstudy(id):
    libstudy = LibStudy.query.filter_by(id=id).first_or_404()
    form = LibStudyForm()

    if form.validate_on_submit():
        libstudy.contents=form.body.data
        libstudy.libstudyname = form.libstudyname.data
        libstudy.about_this = form.about_this.data
        libstudy.lastupdate_timestamp = datetime.utcnow()        
        db.session.add(libstudy)
        db.session.commit()
        """ only insert data to sql table can trigger the action to generate an unique ID"""
        return redirect(url_for('libstudy.show_libstudy', id=libstudy.id))
    
    form.body.data = libstudy.contents
    form.libstudyname.data = libstudy.libstudyname
    form.about_this.data  = libstudy.about_this
    
    return render_template("libstudy/edit_libstudy.html", form=form)
    



