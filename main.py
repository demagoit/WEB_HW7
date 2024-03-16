from alchemy import *
from my_select import SELECT

def init_db():
    session = DBSession()

    Base.metadata.create_all(engine)
    print('------------created-------------')
    fg = Fake_generator()
    fg(session)
    print('------------populated-------------')

    for rqst in SELECT:
        resp = rqst(session)
        for line in resp:
            print(line)
        print('------------')

if __name__ == '__main__':
    init_db()

