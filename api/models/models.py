import psycopg2
import sys

def main():
    # Define our connection string
    conn_string = "host='localhost' dbname='My-Diary' user='postgres' password='root'"

    # print the connection string we will use to connect
    print("Connecting to database\n	->%s" % (conn_string))

    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(conn_string)

    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()
    # print ("Connected!\n")gg


    sql= "INSERT INTO diaryentries(name, due_date, type, purpose) VALUES (%s, %s, %s, %s)"
    val =  ("meet john hty", "2017-3-2", "office", "clear issues pending")

    cursor.execute(sql, val)

    conn.commit()

    print(cursor.rowcount, "record inserted.")
# execute our Query
    cursor.execute("SELECT * FROM diaryentries")

    # retrieve the records from the database
    records = cursor.fetchall()

    print(records)


if __name__ == "__main__":
    main()
