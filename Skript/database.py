import pandas as pd
import mysql.connector
from secrets import *

db = mysql.connector.connect(
        user = DB_USER,
        password = DB_PW,
        host= DB_HOST,
        port='3306',
        database='Lernzeit_app'
        )
cursor = db.cursor()



def create_table():

    create_table = """CREATE TABLE IF NOT EXISTS Lernzeiten(
                      Modul varchar(50),
                      Zeiten int,
                      Datum date
                      );"""

    cursor.execute(create_table)
    db.commit()



def insert_time(vorlesung: str, dauer: int):


    cursor.execute("INSERT INTO Lernzeiten VALUES('{0}', {1}, CURDATE());".format(vorlesung, dauer))
    db.commit()



def loesche_vorlesung(name: str):

    cursor.execute("DELETE FROM Lernzeiten WHERE Modul = '{0}';".format(name))
    db.commit()




def del_time(name: str, zeit: int):

    cursor.execute("INSERT INTO Lernzeiten VALUES('{0}',{1},CURDATE())".format(name, zeit*(-1), ))
    db.commit()



def zeige():

    sql = "SELECT Modul, SUM(Zeiten) FROM Lernzeiten GROUP BY Modul;"
    cursor.execute(sql)
    list = cursor.fetchall()

    sum = 0
    for i in range(0,len(list)):
        sum += int(list[i][1])

    result = [[] for i in range(0,len(list))]

    for i in range(0,len(list)):
        result[i].append(list[i][0])
        result[i].append(str(round(int(list[i][1])/60,1)) + " h")
        result[i].append(str(round(int(list[i][1])*100/sum,0)) + "%")

    return result



def zeige_woche():

    sql = """SELECT date_format(Datum, '%W') as Tag, SUM(Zeiten) FROM Lernzeiten
           WHERE YEARWEEK(Datum, 1) = YEARWEEK(CURDATE(), 1)
           GROUP BY date_format(Datum, '%W');"""

    cursor.execute(sql)
    list = cursor.fetchall()

    result = [[] for i in range(0,len(list))]

    for i in range(0,len(list)):
        result[i].append(list[i][0])
        result[i].append(str(round(int(list[i][1])/60,1)) + " h")

    return result



def zeige_monat():

    sql = """ SELECT DATE_FORMAT(Datum, "%M") as Monat, SUM(Zeiten)
              FROM Lernzeiten
              GROUP BY DATE_FORMAT(Datum, "%M");"""

    cursor.execute(sql)
    list = cursor.fetchall()

    result = [[] for i in range(0,len(list))]

    for i in range(0,len(list)):
        result[i].append(list[i][0])
        result[i].append(str(round(int(list[i][1])/60,1)) + " h")

    return result



def get_lectures():

    sql = "SELECT Distinct(Modul) FROM Lernzeiten;"
    cursor.execute(sql)

    lectures = cursor.fetchall()

    result = [x[0] for x in lectures]

    return result
