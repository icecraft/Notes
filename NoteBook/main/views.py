from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..models import User, Topic, Note
from . import main
from flask.ext.login import login_required, current_user


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST' :
        keyword = "%" + request.form['search'] + "%"
        if keyword in "%%":
                return render_template("main/search.html", notepage=-1, topicpage=-1)
        notepage = request.args.get('notepage', 1, type=int)
        notepagination = Note.query.filter(Note.title.like(keyword)).order_by(\
                           Note.timestamp.desc()).paginate(notepage,\
                           per_page=current_app.config['SEARCH_NOTE_PER_PAGE'], error_out=False)
        notes = notepagination.items

        topicpage = request.args.get('topicpage', 1, type=int)
        topicpagination = Topic.query.filter(Topic.title.like(keyword)).order_by(\
                          Topic.timestamp.desc()).paginate(topicpage,\
                          per_page=current_app.config['SEARCH_TOPIC_PER_PAGE'], error_out=False)
        topics = topicpagination.items
        
        return render_template("main/search.html", notes=notes, topics=topics,\
                               notepagin=notepagination, topicpagin=topicpagination,\
                               keyword=keyword[1:-1])
    return render_template("main/search.html", notepage=-1, topicpage=-1)


