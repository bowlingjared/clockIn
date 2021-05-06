from flask import Flask, render_template, redirect, url_for, request
import webbrowser
import dbquery

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

userID = None

@app.route('/', methods=['GET', 'POST'])
def login():
    global userID
    error = None
    if request.method == 'POST':
        if int(request.form['username']) in dbquery.get_man():
            userID = request.form['username']
            return redirect(url_for('manager'))
        elif int(request.form['username']) in dbquery.get_emp():
            userID = request.form['username']
            return redirect(url_for('employee'))

        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)



@app.route('/emp', methods=['GET', 'POST'])
def employee():
    global userID
    if request.method == 'POST':
        shiftreq = request.form.getlist('shift')
        for shift in shiftreq:
            dbquery.take_shift(userID, shift)
    return render_template('employee.html', strs=dbquery.get_shifts(userID), working=dbquery.get_emp_shifts(userID))  # render a template

@app.route('/update', methods=['GET','POST'])
def update():
    global userID
    if request.method == 'POST':
        shiftreq = request.form.getlist('delete')
        print(shiftreq)
        for shift in shiftreq:
            dbquery.update_shifts(userID, shift)
    return render_template('employee.html', strs=dbquery.get_shifts(), working=dbquery.get_emp_shifts(userID))  # render a template


@app.route('/man', methods=['GET', 'POST'])
def manager():
    global userID

    if request.method == 'POST':
        if request.form.get("submit_button"):
            dbquery.add_shift(request.form['BeginDate'], request.form['BeginTime'], request.form['EndDate'], request.form['EndTime'], request.form['ShiftType'], userID)
        elif request.form.get("select_shift"):
            shiftreq = request.form.getlist('shift')
            for shift in shiftreq:
                dbquery.take_shift(userID, shift)
        elif request.form.get('add_employee'):
            dbquery.add_employee(request.form['emp_name'], request.form['position'])
        elif request.form.get('remove_employee'):
            dbquery.drop_employee(request.form['emp_id'])
        elif request.form.get('edit_position'):
            dbquery.edit_employee(request.form['emp_id'], request.form['position']) # idk
        elif request.form.get('edit_wages'):
            pos_idreq = request.form.getlist('pos_id')
            newwagereq = request.form.getlist('new_wage')
            index = 0
            for new_wage in newwagereq:
                # if not null, not contains characters, and greater than zero
                if ((not new_wage == '') and 
                    (not new_wage.upper().isupper()) and
                    (float(new_wage) >= 0)):
                    dbquery.update_wage(pos_idreq[index], new_wage)
                index = index + 1
    return render_template('manager.html', strs=dbquery.get_shifts(userID), working=dbquery.get_emp_shifts(userID), pos=dbquery.get_positions()) # render a template

@app.route('/ap', methods=['GET', 'POST'])
def AnnualPayroll():

    return render_template('annualpayroll.html', working=dbquery.get_annual_payroll(), error='Oh no!')

@app.route('/wp', methods=['GET', 'POST'])
def WeeklyPayroll():

    return render_template('WeeklyPayroll.html', working=dbquery.get_weekly_payroll(), error='Oh no!')

@app.route('/tc', methods=['GET', 'POST'])
def WeeklyTimecard():

    return render_template('TimeCard.html', working=dbquery.get_weekly_timecard(userID), error='Oh no!')


if __name__ == '__main__':
    app.run()
