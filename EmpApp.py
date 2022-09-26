from logging import exception
from unittest import result
from flask import Flask, render_template, request, flash, send_file
from pymysql import connections
import os
import boto3
from config import *
# from tables import Results

app = Flask(__name__, static_folder="templates")
app.secret_key = "super secret key"

bucket = custombucket
region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb

)
output = {}
table = 'employee'
table1 = 'leaveApp'
table2 = 'payroll'

headings=("emp_id","emp_email","emp_name","emp_DoB","emp_contact", "emp_department", "emp_address", "emp_image", "emp_resume" )
headings1=("leave_id","leave_emp_id","leave_emp_name","leave_date","leave_days", "leave_reason")
headings2=("payroll_id","payroll_emp_id","payroll_emp_name","payroll_month","payroll_salary", "payroll_overtime", "payroll_netsalary")

@app.route("/", methods=['GET', 'POST'])
def home():
    read_sql  = "SELECT * FROM employee"
    cursor = db_conn.cursor()
    print("testing")

    try:
        cursor.execute(read_sql)
        db_conn.commit()
        data = cursor.fetchall()


    except Exception as e: 
        return str(e)
    finally:
        cursor.close()
    
    read_sql  = "SELECT * FROM leaveApp"
    cursor = db_conn.cursor()
    print("testing")

    try:
        cursor.execute(read_sql)
        db_conn.commit()
        data1 = cursor.fetchall()


    except Exception as e: 
        return str(e)
    finally:
        cursor.close()        

    read_sql  = "SELECT * FROM payroll"
    cursor = db_conn.cursor()

    try:
        cursor.execute(read_sql)
        db_conn.commit()
        data2 = cursor.fetchall()


    except Exception as e: 
        return str(e)
    finally:
        cursor.close()
    return render_template('index.html', headings = headings, data = data, headings1 = headings1, data1 = data1, headings2 = headings2, data2 = data2)

@app.route("/templates/view-employee.html", methods=['GET'])
def ReadEmp():
    read_sql  = "SELECT * FROM employee"
    cursor = db_conn.cursor()
    print("testing")

    try:
        cursor.execute(read_sql)
        db_conn.commit()
        data = cursor.fetchall()


    except Exception as e: 
        return str(e)
    finally:
        cursor.close()
    return render_template('view-employee.html', headings = headings, data = data)

@app.route("/templates/view-leave.html", methods=['GET'])
def ReadLeave():
    read_sql  = "SELECT * FROM leaveApp"
    cursor = db_conn.cursor()

    try:
        cursor.execute(read_sql)
        db_conn.commit()
        data1 = cursor.fetchall()


    except Exception as e: 
        return str(e)
    finally:
        cursor.close()
    return render_template('view-leave.html', headings1 = headings1, data1 = data1)    

@app.route("/templates/view-payroll.html", methods=['GET'])
def ReadPayroll():
    read_sql  = "SELECT * FROM payroll"
    cursor = db_conn.cursor()

    try:
        cursor.execute(read_sql)
        db_conn.commit()
        data2 = cursor.fetchall()


    except Exception as e: 
        return str(e)
    finally:
        cursor.close()
    return render_template('view-payroll.html', headings2 = headings2, data2 = data2)    



@app.route("/templates/remove-employee.html/<emp_id>", methods=['GET','POST'])
def RemoveEmp(emp_id):
    cursor = db_conn.cursor()

    try:
        emp_image_file_name_in_s3 = "emp-id-" + str(emp_id) + "_image_file"
        emp_resume_file_name_in_s3 = "emp-id-" + str(emp_id) + "_resume_file"

        s3 = boto3.client('s3')
        s3.delete_object(Bucket= bucket, Key= emp_image_file_name_in_s3)
        s3.delete_object(Bucket= bucket, Key= emp_resume_file_name_in_s3)
        remove_sql =("DELETE FROM employee WHERE emp_id= %s")
        cursor.execute(remove_sql,emp_id)
        db_conn.commit()

    except Exception as e: 
        print (str(e))
    finally:
        cursor.close()

    flash("Employee Successfully Removed")
    return render_template('remove-employee.html', name = emp_id)

@app.route("/templates/remove-leave.html/<leave_id>", methods=['GET','POST'])
def RemoveLeave(leave_id):
    cursor = db_conn.cursor()

    try:
        remove_sql =("DELETE FROM leaveApp WHERE leave_id= %s")
        cursor.execute(remove_sql,leave_id)
        db_conn.commit()

    except Exception as e: 
        print (str(e))
    finally:
        cursor.close()

    flash("Leave Successfully Removed")
    return render_template('remove-leave.html', name = leave_id)    

@app.route("/templates/remove-payroll.html/<payroll_id>", methods=['GET','POST'])
def RemovePayroll(payroll_id):
    cursor = db_conn.cursor()

    try:
        remove_sql =("DELETE FROM payroll WHERE payroll_id= %s")
        cursor.execute(remove_sql,payroll_id)
        db_conn.commit()

    except Exception as e: 
        print (str(e))
    finally:
        cursor.close()

    flash("Payroll Successfully Removed")
    return render_template('remove-payroll.html', name = payroll_id)    




@app.route("/templates/update-employee.html/<emp_id>", methods=['GET'])
def SearchEmp(emp_id):

    search_sql =("SELECT * FROM employee WHERE emp_id = %s")
    cursor = db_conn.cursor()
    try: 
        cursor.execute(search_sql,emp_id)
        db_conn.commit()
        row = cursor.fetchone() 
            
    except Exception as e: 
        print(str(e))
    finally:
        cursor.close()
    return render_template('update-employee.html',row = row)


@app.route("/templates/update-leave.html/<leave_id>", methods=['GET'])
def SearchLeave(leave_id):

    search_sql =("SELECT * FROM leaveApp WHERE leave_id = %s")
    cursor = db_conn.cursor()
    try: 
        cursor.execute(search_sql,leave_id)
        db_conn.commit()
        row = cursor.fetchone() 
            
    except Exception as e: 
        print(str(e))
    finally:
        cursor.close()
    return render_template('update-leave.html',row = row)

@app.route("/templates/update-payroll.html/<payroll_emp_name>", methods=['GET'])
def SearchPayroll(payroll_emp_name):

    search_sql =("SELECT * FROM payroll WHERE payroll_emp_name = %s")
    cursor = db_conn.cursor()
    try: 
        cursor.execute(search_sql,payroll_emp_name)
        db_conn.commit()
        row = cursor.fetchone() 
            
    except Exception as e: 
        print(str(e))
    finally:
        cursor.close()
    return render_template('update-payroll.html',row = row)





@app.route("/templates/update-employee.html/<emp_id>", methods=['POST'])
def UpdateEmp(emp_id):
    emp_email = request.form['emp_email']
    emp_name = request.form['emp_name']
    emp_DoB = request.form['emp_DoB']
    emp_contact = request.form['emp_contact']
    emp_department = request.form['emp_department']
    emp_address = request.form['emp_address']
    emp_image = request.files['emp_image']
    emp_resume = request.files['emp_resume']    
    update_sql = ("UPDATE employee SET emp_email=%s, emp_name=%s, emp_DoB=%s, emp_contact=%s, emp_department=%s, emp_address=%s, emp_image=%s, emp_resume=%s   WHERE emp_id=%s")
    cursor = db_conn.cursor()


    if emp_id == "": 
        return "Please enter Employee ID"
    elif emp_email == "":
        return "Please enter First Name"
    elif emp_name =="":
        return "Please enter Last Name"
    elif emp_DoB =="":
        return "Please enter Primary Skill"
    elif emp_contact =="":
        return "Please enter Location"
    elif emp_department == "":
        return "Please enter department"
    elif emp_address == "":
        return "Please enter address"
    elif emp_image == "":
        return "Please select an Image"
    elif emp_resume == "":
        return "Please select an resume"                
    try:
        emp_image_file_name_in_s3 = "emp-id-" + str(emp_id) + "_image_file"
        emp_resume_file_name_in_s3 = "emp-id-" + str(emp_id) + "_resume_file"
        try:
            s3 = boto3.resource('s3')
            s3.Bucket(custombucket).put_object(Key=emp_image_file_name_in_s3, Body=emp_image)
            s3.Bucket(custombucket).put_object(Key=emp_resume_file_name_in_s3, Body=emp_resume)
            bucket_location = boto3.client('s3').get_bucket_location(Bucket = custombucket)
            s3_location = (bucket_location['LocationConstraint'])

            if s3_location is None: 
                s3_location = ''
            else: 
                s3_location = '-' + s3_location

            image_object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
                s3_location,
                custombucket,
                emp_image_file_name_in_s3)

            resume_object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
                s3_location,
                custombucket,
                emp_resume_file_name_in_s3)

            cursor.execute(update_sql, (emp_email, emp_name, emp_DoB, emp_contact, emp_department, emp_address, image_object_url, resume_object_url, emp_id))
            db_conn.commit()

        except Exception as e:
            return str(e)
    finally:
        cursor.close()
    
    print("Update Succesfully")
    return render_template('update-employee-output.html', name = emp_name)


@app.route("/templates/update-leave.html/<leave_id>", methods=['POST'])
def UpdateLeave(leave_id):
    leave_date = request.form['leave_date']
    leave_days = request.form['leave_days']
    leave_reason = request.form['leave_reason']    
    update_sql = ("UPDATE leaveApp SET leave_date=%s, leave_days=%s, leave_reason=%s   WHERE leave_id=%s")
    cursor = db_conn.cursor()
            
    
    try:

        cursor.execute(update_sql, (leave_date, leave_days, leave_reason, leave_id))
        db_conn.commit()

    except Exception as e:
        return str(e)
        cursor.close()
    
    print("Update Succesfully")
    return render_template('update-leave-output.html', name = leave_id)


@app.route("/templates/update-payroll.html/<payroll_emp_name>", methods=['POST'])
def UpdatePayroll(payroll_emp_name):

    payroll_month = request.form['payroll_month']
    payroll_salary = float(request.form['payroll_salary'])
    payroll_overtime = float(request.form['payroll_overtime'])
    epf = float(0.11)
    socso = float(0.05)


      
    update_sql = ("UPDATE payroll SET payroll_month=%s, payroll_salary=%s, payroll_overtime=%s   WHERE payroll_emp_name=%s")
    cursor = db_conn.cursor()
            
    
    try:


        total_salary = payroll_salary + payroll_overtime
        total_salary = float(total_salary)
        payroll_salary = float(payroll_salary)
            
        total_epf = total_salary * epf
        total_socso = total_salary * socso
            
        payroll_netsalary = total_salary - float(total_epf) - float(total_socso)
        payroll_netsalary = float(payroll_netsalary)        

        cursor.execute(update_sql, (payroll_month, payroll_salary, payroll_overtime, payroll_emp_name))
        db_conn.commit()

    except Exception as e:
        return str(e)
        cursor.close()
    
    print("Update Succesfully")
    return render_template('update-payroll-output.html', name = payroll_emp_name, name1=payroll_netsalary)





@app.route("/templates/add-employee.html", methods=['GET'])
def ViewAddEmp():
    return render_template('add-employee.html')

@app.route("/templates/add-leave.html", methods=['GET'])
def ViewAddLeave():
    return render_template('add-leave.html')
    
@app.route("/templates/add-payroll.html", methods=['GET'])
def ViewAddPayroll():
    return render_template('add-payroll.html')

@app.route("/templates/view-employee.html", methods=['GET'])
def ViewViewEmp():
    ReadEmp()
    return render_template('view-employee.html')

@app.route("/templates/view-leave.html", methods=['GET'])
def ViewViewLeave():
    ReadLeave()
    return render_template('view-leave.html')

@app.route("/templates/view-payroll.html", methods=['GET'])
def ViewViewPayroll():
    ReadPayroll()
    return render_template('view-payroll.html')

@app.route("/templates/remove-employee.html/<emp_id>", methods=['GET'])
def ViewRemoveEmp(emp_id):
    RemoveEmp(emp_id)
    return render_template('remove-employee.html')


@app.route("/templates/add-employee.html", methods=['POST'])
def AddEmp():
    emp_id= request.form['emp_id']
    emp_email = request.form['emp_email']
    emp_name = request.form['emp_name']
    emp_DoB = request.form['emp_DoB']
    emp_contact = request.form['emp_contact']
    emp_department = request.form['emp_department']
    emp_address = request.form['emp_address']
    emp_image = request.files['emp_image']
    emp_resume = request.files['emp_resume']        

    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    if emp_image.filename == "":
        return "Please select an image file"
    
    if emp_resume.filename == "":
        return "Please select an PDF file"
    try:

        # Uplaod image file in S3 #
        emp_image_file_name_in_s3 = "emp-id-" + str(emp_id) + "_image_file"
        emp_resume_file_name_in_s3 = "emp-id-" + str(emp_id) + "_resume_file"
        s3 = boto3.resource('s3')

        try:
            print("Data inserted in MySQL RDS... uploading image to S3...")
            s3.Bucket(custombucket).put_object(Key=emp_image_file_name_in_s3, Body=emp_image)
            s3.Bucket(custombucket).put_object(Key=emp_resume_file_name_in_s3, Body=emp_resume)
            bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
            s3_location = (bucket_location['LocationConstraint'])

            if s3_location is None:
                s3_location = ''

            else:
                s3_location = '-' + s3_location

            image_object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
                s3_location,
                custombucket,
                emp_image_file_name_in_s3)

            resume_object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
                s3_location,
                custombucket,
                emp_resume_file_name_in_s3)
            cursor.execute(insert_sql, (emp_id, emp_email, emp_name, emp_DoB, emp_contact, emp_department, emp_address, image_object_url, resume_object_url))
            db_conn.commit()

        except Exception as e:
            return str(e)

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('add-employee-output.html', name=emp_name)

@app.route("/templates/add-leave.html", methods=['POST'])
def AddLeave():
    leave_emp_id= request.form['leave_emp_id']
    leave_emp_name= request.form['leave_emp_name']
    leave_date = request.form['leave_date']
    leave_days = request.form['leave_days']
    leave_reason = request.form['leave_reason']

    insert_sql = "INSERT INTO leaveApp(leave_emp_id,leave_emp_name,leave_date,leave_days,leave_reason) VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    try:

        try:
            print("Data inserted in MySQL RDS... ")

            cursor.execute(insert_sql, (leave_emp_id, leave_emp_name, leave_date, leave_days, leave_reason))
            db_conn.commit()

        except Exception as e:
            return str(e)

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('add-leave-output.html', name=leave_emp_name)


@app.route("/templates/add-payroll.html", methods=['POST'])
def AddPayroll():
    payroll_emp_id= request.form['payroll_emp_id']
    payroll_emp_name= request.form['payroll_emp_name']
    payroll_month = request.form['payroll_month']
    payroll_salary = float(request.form['payroll_salary'])
    payroll_overtime = float(request.form['payroll_overtime'])
    epf = float(0.11)
    socso = float(0.05)

    insert_sql = "INSERT INTO payroll(payroll_emp_id,payroll_emp_name,payroll_month,payroll_salary,payroll_overtime, payroll_netsalary) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    try:
            total_salary = payroll_salary + payroll_overtime
            total_salary = float(total_salary)
            payroll_salary = float(payroll_salary)
            
            total_epf = total_salary * epf
            total_socso = total_salary * socso
            
            payroll_netsalary = total_salary - float(total_epf) - float(total_socso)
            payroll_netsalary = float(payroll_netsalary)
            print("Data inserted in MySQL RDS... ")

            cursor.execute(insert_sql, (payroll_emp_id, payroll_emp_name, payroll_month, payroll_salary, payroll_overtime, payroll_netsalary))
            db_conn.commit()

    except Exception as e:
        return str(e)

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('add-payroll-output.html', name=payroll_emp_name, name1=payroll_netsalary)


@app.route("/updateprofile/<empid>")
def updateprofile(empid):
    row = empid
    select_sql = "SELECT * from employee WHERE emp_id = %s"
    cursor = db_conn.cursor()
    cursor.execute(select_sql, row)
    row = cursor.fetchone()
    return render_template('UpdateEmpOutput.html', row = row)

@app.route("/removeprofile/<empid>")
def removeprofile(empid):
    id = empid
    return render_template('RemoveEmp.html', id=id)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
    app.debug = True
    app.run()