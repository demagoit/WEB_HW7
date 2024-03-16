import sqlalchemy
from alchemy import Student, Subject, Mark, Group, Proffessor

def rqst(session, qry):
    return session.execute(qry).all()

def select_1(session):
    print('Знайти 5 студентів із найбільшим середнім балом з усіх предметів.')
    qry = sqlalchemy.select(Student.name, Student.surname, sqlalchemy.func.avg(Mark.mark).label('avg_mark'))\
                .select_from(Student).join(Mark).group_by(Student.name, Student.surname).order_by(sqlalchemy.desc('avg_mark')).limit(5) #.all()
    return rqst(session, qry)

def select_2(session):
    print('Знайти студента із найвищим середнім балом з певного предмета.')
    qry = sqlalchemy.select(Subject.title, Student.name, Student.surname, sqlalchemy.func.avg(Mark.mark).label('avg_mark'))\
        .select_from(Student).join(Mark).join(Subject).where(Subject.title == 'Math').group_by(Subject.title, Student.name, Student.surname)\
            .order_by(sqlalchemy.desc('avg_mark')).limit(1) #.all()
    return rqst(session, qry)

def select_3(session):
    print('Знайти середній бал у групах з певного предмета.')
    qry = sqlalchemy.select(Subject.title, Group.name, sqlalchemy.func.avg(Mark.mark).label('avg_mark'))\
        .select_from(Student).join(Group).join(Mark).join(Subject).where(Subject.id == 1).group_by(Subject.title, Group.name)\
            .order_by(sqlalchemy.desc('avg_mark')) #.all()
    return rqst(session, qry)

def select_4(session):
    print('Знайти середній бал на потоці (по всій таблиці оцінок).')
    qry = sqlalchemy.select(sqlalchemy.func.avg(Mark.mark).label('avg_mark')).select_from(Mark)
    return rqst(session, qry)

def select_5(session):
    print('Знайти які курси читає певний викладач.')
    qry = sqlalchemy.select(Proffessor.name, Proffessor.surname, Subject.title)\
        .select_from(Subject).join(Proffessor).where(Proffessor.id == 1)
    return rqst(session, qry)

def select_6(session):
    print('Знайти список студентів у певній групі.')
    qry = sqlalchemy.select(Student.name, Student.surname, Group.name)\
        .select_from(Student).join(Group).where(Group.id == 2).order_by(Student.surname)
    return rqst(session, qry)

def select_7(session):
    print('Знайти оцінки студентів у окремій групі з певного предмета.')
    qry = sqlalchemy.select(Student.name, Student.surname, Subject.title, Group.name, sqlalchemy.func.avg(Mark.mark).label('avg_mark'))\
        .select_from(Student).join(Group).join(Mark).join(Subject).where(sqlalchemy.and_(Subject.id == 1), (Group.id == 3))\
            .group_by(Student.name, Student.surname, Subject.title, Group.name).order_by(sqlalchemy.desc('avg_mark'))
    return rqst(session, qry)

def select_8(session):
    print('Знайти середній бал, який ставить певний викладач зі своїх предметів.')
    qry = sqlalchemy.select(Proffessor.name, Proffessor.surname, Subject.title, sqlalchemy.func.avg(Mark.mark).label('avg_mark'))\
        .select_from(Proffessor).join(Mark).join(Subject).where(Proffessor.id == 2).group_by(Proffessor.name, Proffessor.surname, Subject.title)
    return rqst(session, qry)

def select_9(session):
    print('Знайти список курсів, які відвідує певний студент.')
    qry = sqlalchemy.select(Student.name, Student.surname, Subject.title)\
        .select_from(Student).join(Mark).join(Subject).where(Student.id == 5).group_by(Student.name, Student.surname, Subject.title)
    return rqst(session, qry)

def select_10(session):
    print('Список курсів, які певному студенту читає певний викладач.')
    qry = sqlalchemy.select(Student.name, Student.surname, Subject.title, Proffessor.name, Proffessor.surname)\
        .select_from(Student).join(Mark).join(Subject).join(Proffessor).where(sqlalchemy.and_(Student.id == 4), (Proffessor.id == 2))\
            .group_by(Student.name, Student.surname, Subject.title, Proffessor.name, Proffessor.surname)
    return rqst(session, qry)

def select_11(session):
    print('Середній бал, який певний викладач ставить певному студентові.')
    qry = sqlalchemy.select(Student.name, Student.surname, sqlalchemy.func.avg(Mark.mark).label('avg_mark'), Proffessor.name, Proffessor.surname)\
        .select_from(Student).join(Mark).join(Proffessor).where(sqlalchemy.and_(Student.id == 4), (Proffessor.id == 2))\
            .group_by(Student.name, Student.surname, Proffessor.name, Proffessor.surname)
    return rqst(session, qry)

def select_12(session):
    print('Оцінки студентів у певній групі з певного предмета на останньому занятті.')
    qry = sqlalchemy.select(Student.name, Student.surname, Subject.title, Mark.mark, Mark.set_at )\
        .select_from(Student).join(Mark).join(Subject).join(Group)\
            .where(sqlalchemy.and_(Group.id == 2), (Subject.id == 1),(Mark.set_at == (
                sqlalchemy.select(sqlalchemy.func.max(Mark.set_at)).select_from(Student).join(Mark).join(Subject).join(Group)\
                .where(sqlalchemy.and_(Group.id == 2), (Subject.id == 1))).scalar_subquery()
            ))\
            .order_by(Student.surname)
    return rqst(session, qry)

SELECT = [select_1, select_2, select_3, select_4, select_5, select_6, select_7, select_8, select_9, select_10, select_11, select_12]
