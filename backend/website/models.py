from . import db
from sqlalchemy.sql import func

class Schools(db.Model):
    __tablename__ = 'schools' 
    id = db.Column(db.Integer, primary_key=True)
    school = db.Column(db.String(40))

    def __repr__(self):
        return f'<School {self.school}>'
    
    def serialize(self):
        return {
            'id': self.id,
            'school': self.school,
            'table': self.__tablename__ 
        }

class Subjects(db.Model):
    __tablename__ = 'subjects' 
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(60))
    foreign_id_school = db.Column(db.Integer)

    def __repr__(self):
        return f'<Subject {self.subject}>'

    def serialize(self):
        return {
            'id': self.id,
            'subject': self.subject,
            'foreign_id_school': self.foreign_id_school,
            'table': self.__tablename__ 
        }

class Grades(db.Model):
    __tablename__ = 'grades' 
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.String(120))
    foreign_id_subject = db.Column(db.Integer)

    def __repr__(self):
        return f'<Grade {self.grade}>'
    
    def serialize(self):
        return {
            'id': self.id,
            'grade': self.grade,
            'foreign_id_subject': self.foreign_id_subject,
            'table': self.__tablename__ 
        }

class Subsections(db.Model):
    __tablename__ = 'subsections' 
    id = db.Column(db.Integer, primary_key=True)
    subsection = db.Column(db.String(120))
    foreign_id_grade = db.Column(db.Integer)

    def __repr__(self):
        return f'<Subsection {self.subsection}>'
    
    def serialize(self):
        return {
            'id': self.id,
            'subsection': self.subsection,
            'foreign_id_grade': self.foreign_id_grade,
            'table': self.__tablename__ 
        }

class Central_contents(db.Model):
    __tablename__ = 'central_contents' 
    id = db.Column(db.Integer, primary_key=True)
    central_content = db.Column(db.String(450))
    foreign_id_subsection = db.Column(db.Integer)

    def __repr__(self):
        return f'<Central_content {self.central_content}>'
    
    def serialize(self):
        return {
            'id': self.id,
            'central_content': self.central_content,
            'foreign_id_subsection': self.foreign_id_subsection,
            'table': self.__tablename__ 
        }

class Central_requirements(db.Model):
    __tablename__ = 'central_requirements' 
    id = db.Column(db.Integer, primary_key=True)
    central_requirement = db.Column(db.String(450))
    foreign_id_grade = db.Column(db.Integer)

    def __repr__(self):
        return f'<Central_requirement {self.central_requirement}>'
    
    def serialize(self):
        return {
            'id': self.id,
            'central_requirement': self.central_requirement,
            'foreign_id_grade': self.foreign_id_grade,
            'table': self.__tablename__ 
        }


#class Concepts(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    concept = db.Column(db.String(10000))
#    date = db.Column(db.DateTime(timezone=True), default=func.now())
#    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))



