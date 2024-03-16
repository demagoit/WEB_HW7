import sqlalchemy
import sqlalchemy.orm
import datetime
import faker
import random

database = '/alchemy.db'

# engine = sqlalchemy.create_engine('sqlite:///:memory:', echo=False)
engine = sqlalchemy.create_engine(f'sqlite://{database}', echo=False)
DBSession = sqlalchemy.orm.sessionmaker(bind=engine)

Base = sqlalchemy.orm.declarative_base()

class Student(Base):
    __tablename__ = 'students'
    id:sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(primary_key=True, autoincrement='auto')
    name:sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(sqlalchemy.String(10))
    surname:sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(sqlalchemy.String(30))
    group_id:sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(
        sqlalchemy.Integer, 
        sqlalchemy.ForeignKey('groups.id', onupdate='CASCADE'),
        nullable=True)

class Proffessor(Base):
    __tablename__ = 'proffessors'

    id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(primary_key=True, autoincrement='auto')
    name: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(sqlalchemy.String(10), nullable=False)
    surname: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(sqlalchemy.String(30), nullable=False)
    
class Group(Base):
    __tablename__ = 'groups'
    id:sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(primary_key=True, autoincrement='auto')
    name:sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(sqlalchemy.String(10), nullable=False)

class Subject(Base):
    __tablename__ = 'subjects'
    id:sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(primary_key=True, autoincrement='auto')
    title:sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(sqlalchemy.String(30), nullable=False)
    proffessor_id:sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(
        sqlalchemy.Integer, 
        sqlalchemy.ForeignKey(
            'proffessors.id', 
            onupdate='CASCADE'), 
            nullable=True
    )

class Mark(Base):
    __tablename__ = 'marks'
    id:sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(primary_key=True, autoincrement='auto')
    student_id:sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(
        sqlalchemy.Integer, 
        sqlalchemy.ForeignKey('students.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False)
    subject_id:sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(
        sqlalchemy.Integer, 
        sqlalchemy.ForeignKey('subjects.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False)
    proffessor_id:sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(
        sqlalchemy.Integer, 
        sqlalchemy.ForeignKey('proffessors.id', onupdate='CASCADE'),
        nullable=True)
    mark:sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column()
    set_at:sqlalchemy.orm.Mapped[datetime.datetime] = sqlalchemy.orm.mapped_column(sqlalchemy.DateTime, default=datetime.datetime.now)

class Fake_generator:
    def __init__(self):
        self.n_students = 50
        self.n_groups = 3
        self.l_subjects = ['Math', 'Phisics', 'Chemistry', 'English', 'Ukrainian', 'History']
        self.n_proffessors = 5
        self.n_marks = 20

    def generate_fake_data(self, n_students:int=1, n_groups:int=1, n_proffessors:int=1, l_subjects:list = ['Math'], n_marks:int = 1):
        '''generates fake data to fill self.database tables'''
        students = []
        groups = []
        proffessors = []
        subjects = []
        marks = []

        fake_data = faker.Faker()

        for i in range(n_groups):
            groups.append({'name': f'Group_{i}'})

        for _ in range(n_students):
            group_id = random.randint(1, n_groups)
            students.append({'name': fake_data.first_name(), 
                            'surname': fake_data.last_name(), 
                            'group_id': group_id
                            })

        for _ in range(n_proffessors):
            proffessors.append({'name': fake_data.first_name(), 
                                'surname': fake_data.last_name()
                                })

        for subject in l_subjects:
            subjects.append({'title': subject, 
                            'proffessor_id': random.randint(1, n_proffessors)
                            })

        for student in range(1, n_students+1):
            for subject in enumerate(subjects,1):
                if random.randint(0,2) == 0:
                    continue
                subj = subject[0]
                proffessor = subject[1]['proffessor_id']
                for _ in range(n_marks):
                    mark = random.randint(random.randint(1, 5),random.randint(6, 13))
                    set_at = fake_data.date_between(start_date="-1y", end_date='today')
                    marks.append({'student_id': student, 
                                'subject_id': subj, 
                                'proffessor_id': proffessor, 
                                'mark': mark, 
                                'set_at': set_at
                                })

        return students, groups, proffessors, subjects, marks

    def __call__(self, session):
        students, groups, proffessors, subjects, marks = self.generate_fake_data(
            self.n_students, self.n_groups, self.n_proffessors, self.l_subjects, self.n_marks)

        session.bulk_insert_mappings(Student, students)
        session.bulk_insert_mappings(Group, groups)
        session.bulk_insert_mappings(Proffessor, proffessors)
        session.bulk_insert_mappings(Subject, subjects)
        session.bulk_insert_mappings(Mark, marks)
        session.commit()
