# -*- coding: utf-8 -*
from flask import render_template, redirect, request, url_for, flash,\
           current_app
from flask.ext.login import  login_required,  current_user
from .. import db
from ..models import  Topic, Comment
from .forms import TopicForm
from . import topic
from ..comment import CommentForm
from datetime import datetime

@topic.route('/topic/<int:id>', methods=['GET', 'POST'])
def show_topic(id):
    topic = Topic.query.filter_by(id=id).first_or_404()
    form = CommentForm()
    comments = Comment.query.filter_by(topic=topic).order_by(Comment.timestamp.desc())
    if form.validate_on_submit():
        comment = Comment(contents=form.body.data,
                      topic=topic)
        db.session.add(comment)
        db.session.commit()
        """ only insert data to sql table can trigger the action to generate an unique ID"""
        return redirect(url_for('topic.show_topic', id=topic.id))
    return render_template('topic/show_topic.html', topic=topic, form=form,
                           comments=comments)

    
@topic.route('/topics', methods=['GET', 'POST'])
def topics():
    page = request.args.get('page', 1, type=int)
    pagination = Topic.query.order_by(Topic.timestamp.desc()).paginate(
        page, per_page=current_app.config['INDEX_TOPICS_PER_PAGE'],
        error_out=False)
    topics = pagination.items
    return render_template('topic/topics.html', topics=topics,
                           pagination=pagination)


@topic.route('/add_topic', methods=['GET', 'POST'])
@login_required
def add_topic():
    form = TopicForm()
    if form.validate_on_submit():
        topic = Topic(contents=form.body.data,
                      topicname = form.topicname.data,
                      about_this = form.about_this.data,
                      author=current_user._get_current_object())
        db.session.add(topic)
        db.session.commit()
        """ only insert data to sql table can trigger the action to generate an unique ID"""
        id = Topic.query.order_by(Topic.timestamp.desc()).first().id
        return redirect(url_for('topic.show_topic', id=id))
    form.body.data = "Hello"
    return render_template("topic/add_topic.html", form=form)

@topic.route('/edit_topic/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_topic(id):
    topic = Topic.query.filter_by(id=id).first_or_404()
    form = TopicForm()

    if form.validate_on_submit():
        topic.contents=form.body.data
        topic.topicname = form.topicname.data
        topic.about_this = form.about_this.data
        topic.lastupdate_timestamp = datetime.utcnow()        
        db.session.add(topic)
        db.session.commit()
        """ only insert data to sql table can trigger the action to generate an unique ID"""
        return redirect(url_for('topic.show_topic', id=topic.id))
    
    form.body.data = topic.contents
    form.topicname.data = topic.topicname
    form.about_this.data  = topic.about_this
    
    return render_template("topic/edit_topic.html", form=form)
    



