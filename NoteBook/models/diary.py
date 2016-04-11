# -*- coding: utf-8 -*
from .. import db
from datetime import datetime
from markdown import markdown
import bleach

DEFAULT_DIARY_CONTENT = u"""### Miscellanise
### TODO
### 完成情况
### 收获
### 思考
"""

class Year(db.Model):
    __tablename__ = 'years'
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, unique=True, index=True)
    month = db.relationship('Month', backref='year', lazy='dynamic',
                            cascade='all, delete-orphan')
    def __repr__(self):
        return " %d 年" % year

    def dump_year(self):
        for month in self.month:
            month.dump_month()
        
class Month(db.Model):
    __tablename__ = 'months'
    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.Integer, unique=True, index=True)
    year_id     = db.Column(db.Integer, db.ForeignKey('years.id'))
    week = db.relationship('Week', backref='month', lazy='dynamic',
                            cascade='all, delete-orphan')

    def dump_month(self):
        for week in self.week:
            week.dump_diary()
            
    @staticmethod
    def monthName(index):
        return ["Nothing Month check It","January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"][index]
    
    def __repr__(self):
        return "Year %d %s"  % (self.year.year, Month.monthName(self.month )) 
    

class Week(db.Model):
    __tablename__ = 'weeks'
    id = db.Column(db.Integer, primary_key=True)
    week = db.Column(db.Integer,  index=True)
    month_id     = db.Column(db.Integer, db.ForeignKey('months.id'))
    diary = db.relationship('Diary', backref='week', lazy='dynamic',
                            cascade='all, delete-orphan')
    def __repr__(self):
        return " %s "  % (str(self.month))
    
    def dump_diary(self):
        for diary in self.diary:
            diary.dump()
    
class Diary(db.Model):
    __tablename__ = 'diaries'
    id = db.Column(db.Integer, primary_key=True)
    diary = db.Column(db.Integer)
    indexInWeek = db.Column(db.Integer)
    indexInYear = db.Column(db.Integer)    
    contents =  db.Column(db.Text())
    contents_html = db.Column(db.Text())
    timestamp     = db.Column(db.DateTime, default=datetime.utcnow)
    lastupdate_timestamp     = db.Column(db.DateTime, default=datetime.utcnow)
    
    author_id     = db.Column(db.Integer, db.ForeignKey('users.id'))
    week_id     = db.Column(db.Integer, db.ForeignKey('weeks.id'))    


    def weekDayName(self, index):
        return ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', \
                'SATURDAY', 'SUNDAY'][index]

    def __repr__(self):
        return "%s %d " % (str(self.week), self.diary)

    def dump(self):
        print self
        
    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                    'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                    'h1', 'h2', 'h3', 'p']
        target.contents_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))
    @staticmethod
    def getIndexInYear(year, month, day):
        import calendar
        monthday = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        monthday[1] = 29 if  calendar.isleap(year) else 28
        return reduce(lambda r, (x,y) : r+y if x < month-1 else r,
                  enumerate(monthday),
                  0) + day
        
    @staticmethod
    def creat_newdiary(yearDiary, user):
        """
           creat new diary by year and user!
        """
        import calendar
        def add_commit(data):
            db.session.add(data)
            db.session.commit()
            
        year = Year.query.filter_by(year=yearDiary).first()
        
        if year:
            import sys
            print "alreay have diary of year %d" % yearDiary
            return None
        else:
            year = Year(year=yearDiary)
            add_commit(year)
            
        for mindex in range(1, 13):

            month = Month(month=mindex, year=year)
            add_commit(month)
            
            value = [ j for j in calendar.Calendar().itermonthdays(yearDiary, mindex) ]
            value, weekStartNum = (value, 1)  if value[0] != 0 else (value[7:], 2)
            tmp = 1
            for k,j in enumerate(value):
                if value[k] == 0:
                    value[k] = tmp
                    tmp += 1

            for weekIndex, mondayIndex in enumerate(value[::7]):
                week = Week(week=weekIndex+weekStartNum, month=month)
                add_commit(week)
                for index, data in enumerate(range(mondayIndex, mondayIndex+7)):
                    diary = Diary(diary=data, week=week, indexInWeek=index,
                                  indexInYear=Diary.getIndexInYear(year.year, mindex, data), 
                                  contents=DEFAULT_DIARY_CONTENT, author=user)
                    add_commit(diary)
                    
                
                
db.event.listen(Diary.contents, 'set', Diary.on_changed_body)
    

    
