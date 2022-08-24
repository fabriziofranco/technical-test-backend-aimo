from models import User, Note, db

if __name__ == '__main__':
    db.connect()

    if not User.table_exists():
        User.create_table()
    
    if not Note.table_exists():
        Note.create_table()

    db.close()
