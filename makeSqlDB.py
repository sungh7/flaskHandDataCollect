import sqlite3

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def main():
    database = r'/Users/csh/data/makepage/static/database.db'
    sql_create_patients_table = '''CREATE TABLE IF NOT EXISTS patients (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        age integer NOT NULL,
                                        sex integer NOT NULL,
                                        disease text NOT NULL,
                                        hand text NOT NULL,
                                        finger_num integer NOT NULL,
                                        description text
                                    );'''
                                    

    sql_create_files_table = '''CREATE TABLE IF NOT EXISTS files (
                                id integer PRIMARY KEY,
                                patient_id integer NOT NULL,
                                filepath text NOT NULL,
                                file_blob GLOB NOT NULL,
                                video_type text NOT NULL,
                                upload_date text NOT NULL,
                                FOREIGN KEY (patient_id) REFERENCES patients (id)
                            );'''

    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_patients_table)
        create_table(conn, sql_create_files_table)
    else:
        print(error)

if __name__ == '__main__':
    main()