import mysql.connector
import connection_info


def get_emp():
    cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                  host=connection_info.MyHost,
                                  database=connection_info.MyDatabase)
    cursor = cnx.cursor()
    query = ("SELECT * from emp")


    cursor.execute(query)
    id = [x[0] for x in cursor.fetchall()]

    cursor.close()
    cnx.close()

    return id


def get_shifts():
    cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                  host=connection_info.MyHost,
                                  database=connection_info.MyDatabase)
    cursor = cnx.cursor()
    query = "SELECT * from shifts"


    cursor.execute(query)
    id = [x[0] for x in cursor.fetchall()]

    cursor.close()
    cnx.close()

    return id

def remove_shifts(id):
    cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                  host=connection_info.MyHost,
                                  database=connection_info.MyDatabase)
    cursor = cnx.cursor()
    query = f"DELETE FROM shifts WHERE shiftID = {id};"
    cursor.execute(query)

    cnx.commit()
    cursor.close()
    cnx.close()

    return 0;

def take_shift(empID,shiftId):

    cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                  host=connection_info.MyHost,
                                  database=connection_info.MyDatabase)
    cursor = cnx.cursor()
    query = f"INSERT INTO takenShifts VALUES ({empID},{shiftId});"
    print(query)
    cursor.execute(query)

    cnx.commit()
    cursor.close()
    cnx.close()

    remove_shifts(shiftId)

    return 0;




def list_shifts(id):
    cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                  host=connection_info.MyHost,
                                  database=connection_info.MyDatabase)
    cursor = cnx.cursor()
    query = f"select shiftId FROM takenShifts WHERE empID = {id};"
    cursor.execute(query)

    shifts = [x[0] for x in cursor.fetchall()]

    cnx.commit()
    cursor.close()
    cnx.close()

    return shifts;


