import mysql.connector
import connection_info


def get_emp():
    cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                  host=connection_info.MyHost,
                                  database=connection_info.MyDatabase)
    cursor = cnx.cursor(prepared=True)
    query = "SELECT * from employee"


    cursor.execute(query)
    id = [x[0] for x in cursor.fetchall()]

    cursor.close()
    cnx.close()

    return id


def get_man():
    cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                  host=connection_info.MyHost,
                                  database=connection_info.MyDatabase)
    cursor = cnx.cursor(prepared=True)
    query = "SELECT * from manager"

    cursor.execute(query)
    query = ()

    cursor.execute(query)
    id = [x[1] for x in cursor.fetchall()]

    cursor.close()
    cnx.close()

    return id


def get_shifts(id):
    cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                  host=connection_info.MyHost,
                                  database=connection_info.MyDatabase)

    query = "SELECT * from shift where shift_id in (select shift_id from shift_position where num_emp_needed > 0 and position_id = (select position_id from employee where emp_id = %s)); "
    cursor = cnx.cursor(prepared=True)

    cursor.execute(query, (id,))

    id = cursor.fetchall()

    cursor.close()
    cnx.close()

    return id

# returns all positions
def get_positions():
    cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                  host=connection_info.MyHost,
                                  database=connection_info.MyDatabase)
    cursor = cnx.cursor(prepared=True)
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
    cursor = cnx.cursor(Prepared = True)
    query = "UPDATE position SET wage = %s WHERE position_id = %s;"

    cursor.execute(query, (position_id, new_wage))

    cnx.commit()
    cursor.close()

    cnx.close()

    return 0


# Remove an open slot for the specified shift
def remove_shifts(id):
    cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                  host=connection_info.MyHost,
                                  database=connection_info.MyDatabase)
    
    cnx.start_transaction(isolation_level='REPEATABLE READ')  
    cursor = cnx.cursor(prepared=True)
    query = "UPDATE shift_position set num_emp_needed = num_emp_needed - 1 where shift_id = %s;"

    cursor.execute(query,(id,))

    cnx.commit()
    cursor.close()

    cnx.close()

    return 0


# Insert shift into
def take_shift(empID, shiftId):
    cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                  host=connection_info.MyHost,
                                  database=connection_info.MyDatabase)


    cursor = cnx.cursor(prepared=True)
    query = f"INSERT INTO employee_shift VALUES (%s,%s);"

    cursor.execute(query, (empID,shiftId))


    cnx.commit()
    cursor.close()
    cnx.close()

    remove_shifts(shiftId)

    return 0

#Update shifts in order to remove a shift from an employee
def update_shifts(empID, shiftId):
    cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                  host=connection_info.MyHost,
                                  database=connection_info.MyDatabase)
    cursor = cnx.cursor()
    query = f"UPDATE shift_position set num_emp_needed = num_emp_needed + 1 where shift_id = {shiftId};"
    cursor.execute(query)
    cnx.commit()

    query = f"DELETE from employee_shift where shift_id={shiftId} and emp_id={empID}"
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()
    return 0

# Gets all of the current shifts for a current employee
def list_shifts(id):
    cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                  host=connection_info.MyHost,
                                  database=connection_info.MyDatabase)
    cursor = cnx.cursor(prepared=True)
    query = "select * FROM employee_shift WHERE emp_id = %s;"
    cursor.execute(query, (id,))

    shifts = cursor.fetchall()

    cursor.close()
    cnx.close()

    return shifts


def get_emp_shifts(empID):
    cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                  host=connection_info.MyHost,
                                  database=connection_info.MyDatabase)
    cursor = cnx.cursor(prepared=True)
    query = "select * FROM shift WHERE shift_id in (select shift_id from employee_shift where emp_id = %s);"
    cursor.execute(query,(empID,))

    shifts = cursor.fetchall()

    cursor.close()
    cnx.close()

    return shifts


def add_shift(start_date, start_time, end_date, end_time, pos_id, manID):
    cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                  host=connection_info.MyHost,
                                  database=connection_info.MyDatabase)

    start = start_date + " " + start_time + ":00"
    end = end_date + " " + end_time + ":00"

    cnx.start_transaction(isolation_level='SERIALIZABLE')
    
    cursor = cnx.cursor()
    query = f"select max(shift_id) + 1 FROM shift;"
    cursor.execute(query)

    id = cursor.fetchone()[0]
    cursor.close()

    cursor = cnx.cursor(prepared=True)
    query = "INSERT INTO shift VALUES (%s,%s,%s,%s);"

    cursor.execute(query, (id, manID, start, end))

    cnx.commit()
    cursor.close()

    cursor = cnx.cursor(prepared=True)

    query = "INSERT INTO shift_position VALUES (%s,%s,1);"

    cursor.execute(query, (id, pos_id))

    cnx.commit()
    cursor.close()

    cnx.close()

    return 0

def add_employee(name, position):
    cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                  host=connection_info.MyHost,
                                  database=connection_info.MyDatabase)

    cnx.start_transaction(isolation_level='SERIALIZABLE')

    cursor = cnx.cursor()
    query = f"select max(emp_id) + 1 FROM employee;"
    cursor.execute(query)
    id = cursor.fetchone()[0]
    cursor.close()

    cursor = cnx.cursor()
    query = f"INSERT INTO employee VALUES ({id},'{name}',{position});"
    cursor.execute(query)

    cnx.commit()
    cursor.close()

    cnx.close()

    return 0

def drop_employee(emp_id):
    cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                  host=connection_info.MyHost,
                                  database=connection_info.MyDatabase)

    cursor = cnx.cursor()
    query = f"DELETE FROM employee WHERE emp_id={emp_id};"
    cursor.execute(query)
    cnx.commit()
    cursor.close()

    #remove employee from shifts
    cursor = cnx.cursor()
    query = f"DELETE FROM employee_shift WHERE emp_id={emp_id};"
    cursor.execute(query)
    cnx.commit()
    cursor.close()

    cnx.close()

    return 0

def edit_employee(emp_id, position_new):
    cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                  host=connection_info.MyHost,
                                  database=connection_info.MyDatabase)

    cursor = cnx.cursor()
    query = f"UPDATE employee SET position_id={position_new}  WHERE emp_id = {emp_id};"
    cursor.execute(query)
    cnx.commit()
    cursor.close()


    #check if position 1, make manager
    if (position_new==1):
        cursor = cnx.cursor()
        query = f"INSERT INTO manager VALUES ({emp_id},{emp_id});"
        cursor.execute(query)
        cnx.commit()
        cursor.close()

    cnx.close()
    return 0

def get_annual_payroll():
    cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                  host=connection_info.MyHost,
                                  database=connection_info.MyDatabase)
    cursor = cnx.cursor(prepared=True)
    query = "call GetAnnualHours();"

    cursor.execute(query)
    hours = [x for x in cursor.fetchall()]

    return hours

def get_weekly_payroll():
    cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                  host=connection_info.MyHost,
                                  database=connection_info.MyDatabase)
    cursor = cnx.cursor(prepared=True)
    query = "call GetWeeklyHours();"

    cursor.execute(query)
    hours = [x for x in cursor.fetchall()]

    return hours

def get_weekly_timecard(id):
    cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
                                  host=connection_info.MyHost,
                                  database=connection_info.MyDatabase)
    cursor = cnx.cursor(prepared=True)
    query = "call GetWeeklyTimeCard(%s);"

    cursor.execute(query, (id,))
    hours = [x for x in cursor.fetchall()]

    return hours
