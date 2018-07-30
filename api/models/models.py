import psycopg2
import sys
class DiaryDatabase:
    def __init__(self):
        self.conn_string = "host='localhost' dbname='My-Diary' user='postgres' password='root'"

        self.conn = psycopg2.connect(self.conn_string)

        Users="""create table IF NOT EXISTS tusers (id serial primary key not null,username text not null,
                            password text not null)"""
        Entries="""create table IF NOT EXISTS tdiaryentries  (id serial primary key not null,name text not null,
                            due_date text not null, type text not null, purpose text not null, date_created text not null, user_id int)"""

        cursor = self.conn.cursor()
        try:
            cursor.execute(Users,)
            cursor.execute(Entries,)
            self.conn.commit()
            print("Created Succesfuly\n")
        except:
            print("Already Created\n")

    if __name__ == "__main__":
        DiaryDatabase()
