# -*- coding: utf-8 -*
from flask import render_template, redirect, request, url_for, flash, current_app
from flask.ext.login import login_user, logout_user, login_required, \
    current_user
from .. import db
from ..models import Note, Comment
from . import note
from datetime import datetime
from .forms import NoteForm, DEFAULT_NoteBook_Contents,\
    DEFAULT_NoteSource_Contents
from ..comment import CommentForm

@note.route('/show_note/<int:id>', methods=['GET', 'POST'])
def show_note(id):
    note = Note.query.filter_by(id=id).first_or_404()
    form = CommentForm()
    comments = Comment.query.filter_by(note=note).order_by(Comment.timestamp.desc())
    if form.validate_on_submit():
        comment = Comment(contents=form.body.data,
                      note=note)
        db.session.add(comment)
        db.session.commit()
        """ only insert data to sql table can trigger the action to generate an unique ID"""
        return redirect(url_for('note.show_note', id=note.id))    
    return render_template('note/show_note.html', note=note, form=form)

    
@note.route('/notes', methods=['GET', 'POST'])
def notes():
    page = request.args.get('page', 1, type=int)
    pagination = Note.query.order_by(Note.timestamp.desc()).paginate(
        page, per_page=current_app.config['INDEX_NOTES_PER_PAGE'],
        error_out=False)
    notes = pagination.items
    return render_template('note/notes.html', notes=notes,
                           pagination=pagination)


@note.route('/add_note', methods=['GET', 'POST'])
@login_required
def add_note():
    form = NoteForm()
    notetype = request.args.get('NoteType', 'BookNote', type=str)
    if form.validate_on_submit():
        note = Note(contents=form.body.data,
                      notename = form.notename.data,
                      about_this = form.about_this.data,
                      author=current_user._get_current_object())
        db.session.add(note)
        db.session.commit()
        """ only insert data to sql table can trigger the action to generate an unique ID"""
        id = Note.query.order_by(Note.timestamp.desc()).first().id
        return redirect(url_for('note.show_note', id=id))
    if notetype == 'BookNote':
        form.body.data =  DEFAULT_NoteBook_Contents
    else:
        form.body.data = DEFAULT_NoteSource_Contents
    return render_template("note/add_note.html", form=form)

@note.route('/edit_note/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_note(id):
    note = Note.query.filter_by(id=id).first_or_404()
    form = NoteForm()

    if form.validate_on_submit():
        note.contents=form.body.data
        note.notename = form.notename.data
        note.about_this = form.about_this.data
        note.lastupdate_timestamp = datetime.utcnow()        
        db.session.add(note)
        db.session.commit()
        """ only insert data to sql table can trigger the action to generate an unique ID"""
        return redirect(url_for('note.show_note', id=note.id))
    
    form.body.data = note.contents
    form.notename.data = note.notename
    form.about_this.data  = note.about_this
    
    return render_template("note/edit_note.html", form=form)
    



