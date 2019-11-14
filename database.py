from sqlalchemy import create_engine

def init_db():
    engine = create_engine(
        'mysql+pymysql://username:password@localhost:3306/vuvln_app')
    print (engine)
if __name__ == '__main__':
    init_db()
