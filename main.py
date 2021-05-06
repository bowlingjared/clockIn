from flask import Flask, render_template, redirect, url_for, request

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
        print(shiftreq)
        for shift in shiftreq:
            dbquery.take_shift(userID, shift)
    return render_template('employee.html', strs=dbquery.get_shifts(), working=dbquery.get_emp_shifts(userID))  # render a template

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
        if request.form['submit_button'] == 'Add Shift':
            dbquery.add_shift(request.form['BeginDate'], request.form['BeginTime'], request.form['EndDate'], request.form['EndTime'])
        elif request.form['submit_button'] == 'Select Shift':
            shiftreq = request.form.getlist('shift')
            for shift in shiftreq:
                dbquery.take_shift(userID, shift)
        elif request.form['submit_button'] == 'Add Employee':
            dbquery.add_employee(request.form['emp_name'], request.form['position'])
        elif request.form['submit_button'] == 'Remove Employee':
            dbquery.drop_employee(request.form['emp_id'])
        elif request.form['submit_button'] == 'Edit Position':
            dbquery.edit_employee(request.form['emp_id'], request.form['position'])
    return render_template('manager.html', strs=dbquery.get_shifts(), working=dbquery.get_emp_shifts(userID)) # render a template


if __name__ == '__main__':
    app.run()
