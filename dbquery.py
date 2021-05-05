import mysql.connector
import connection_info


def get_emp():
    cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                  host=connection_info.MyHost,
                                  database=connection_info.MyDatabase)
    cursor = cnx.cursor()
    query = ("SELECT * from employee")

    cursor.execute(query)
    id = [x[0] for x in cursor.fetchall()]

    cursor.close()
    cnx.close()

    return id


def get_man():
    cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                  host=connection_info.MyHost,
                                  database=connection_info.MyDatabase)
    cursor = cnx.cursor()
    query = ("SELECT * from manager")

    cursor.execute(query)
    id = [x[1] for x in cursor.fetchall()]

    cursor.close()
    cnx.close()

    return id


def get_shifts():
    cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                  host=connection_info.MyHost,
                                  database=connection_info.MyDatabase)
    cursor = cnx.cursor()
    query = "SELECT * from shift where shift_id in (select shift_id from shift_position where num_emp_needed > 0); "

    cursor.execute(query)
    id = cursor.fetchall()

    cursor.close()
    cnx.close()

    return id

# returns all positions
def get_positions():
    cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                  host=connection_info.MyHost,
                                  database=connection_info.MyDatabase)
    cursor = cnx.cursor()
    query = "SELECT position_id, position_name, wage from position;"

    cursor.execute(query)
    id = cursor.fetchall()

    cursor.close()
    cnx.close()

    return id

# update the wages
def update_wage(position_id, new_wage):
    cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                  host=connection_info.MyHost,
                                  database=connection_info.MyDatabase)
    cursor = cnx.cursor()
    query = f"UPDATE position SET wage = {new_wage} WHERE position_id = {position_id};"

    cursor.execute(query)

    cnx.commit()
    cursor.close()

    cnx.close()

    return 0


# Remove an open slot for the specified shift
def remove_shifts(id):
    cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                  host=connection_info.MyHost,
                                  database=connection_info.MyDatabase)
    cursor = cnx.cursor()
    query = f"UPDATE shift_position set num_emp_needed = num_emp_needed - 1 where shift_id = {id};"

    cursor.execute(query)

    cnx.commit()
    cursor.close()

    cnx.close()

    return 0


# Insert shift into
def take_shift(empID, shiftId):
    cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                  host=connection_info.MyHost,
                                  database=connection_info.MyDatabase)
    print(shiftId)
    cursor = cnx.cursor()
    query = f"INSERT INTO employee_shift VALUES ({shiftId},{empID});"

    cursor.execute(query)

    cnx.commit()
    cursor.close()
    cnx.close()

    remove_shifts(shiftId)

    return 0


# Gets all of the current shifts for a current employee
def list_shifts(id):
    cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                  host=connection_info.MyHost,
                                  database=connection_info.MyDatabase)
    cursor = cnx.cursor()
    query = f"select * FROM employee_shift WHERE emp_id = {id};"
    cursor.execute(query)

    shifts = cursor.fetchall()

    cursor.close()
    cnx.close()

    return shifts


def get_emp_shifts(empID):
    cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                  host=connection_info.MyHost,
                                  database=connection_info.MyDatabase)
    cursor = cnx.cursor()
    query = f"select * FROM shift WHERE shift_id in (select shift_id from employee_shift where emp_id = {empID});"
    cursor.execute(query)

    shifts = cursor.fetchall()

    cursor.close()
    cnx.close()

    return shifts


def add_shift(start_date, start_time, end_date, end_time):
    cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                  host=connection_info.MyHost,
                                  database=connection_info.MyDatabase)

    start = start_date + " " + start_time + ":00"
    end = end_date + " " + end_time + ":00"

    cursor = cnx.cursor()
    query = f"select max(shift_id) + 1 FROM shift;"
    cursor.execute(query)

    id = cursor.fetchone()[0]
    cursor.close()

    cursor = cnx.cursor()

    query = f"INSERT INTO shift VALUES ({id},{1},\'{start}\',\'{end}\');"

    cursor.execute(query)

    cnx.commit()
    cursor.close()

    cursor = cnx.cursor()

    query = f"INSERT INTO shift_position VALUES ({id},{1},{1});"

    cursor.execute(query)

    cnx.commit()
    cursor.close()

    cnx.close()

    return 0
