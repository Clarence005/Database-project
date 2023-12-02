from flask import Flask, render_template, request
import cx_Oracle
app = Flask(__name__)
table2 = 'doctor'
table1 = 'patient'
val = []
try:
    oracle_connection_string = 'system/clarence@localhost:1521/XE'
    connection = cx_Oracle.connect(oracle_connection_string)
    cursor = connection.cursor()
except cx_Oracle.DatabaseError as e:
    error, = e.args
    print("Oracle-Error-Code:", error.code)
    print("Oracle-Error-Message:", error.message)
@app.route("/")
def index():
    return render_template("firstpage.html")


@app.route("/process_form",methods = ["Get","post"])
def process_form():
    try:
        if(request.method == "POST"):
            button_clicked = request.form['button_clicked']
            if button_clicked == 'button1':
                # Processing for the first button click
                return render_template("patient_1.html")
            if button_clicked == 'button2':
                # Processing for the second button click
                return render_template("doctor_1.html")
    except Exception as e:
        return f"Error :{e}!\nPlease Contact Developers"
    return "INVALID REQUEST"

@app.route("/insert_patient",methods = ["Get","post"])
def insert_patient():
    try:
        if(request.method == "POST"):
            button_clicked = request.form['button_clicked']
            if button_clicked == "btn1":
                # Processing for the first button click
                return render_template("patient.html")
            elif button_clicked == 'btn2':
                # Processing for the second button click
                return render_template("update_pat.html")
            elif button_clicked == 'btn3':
                # Processing for the second button click
                return render_template("patient_view.html")

    except Exception as e:
        return f"Error :{e}!\nPlease Contact Developers"

    return "INVALID REQUEST"

@app.route("/next_page",methods = ["Get","post"])
def next_page():
    try:
        if(request.method == "POST"):
            button_clicked = request.form['button_clicked']
            if button_clicked == "btn1":
                # Processing for the first button click
                return render_template("doctor.html")
            elif button_clicked == 'btn2':
                # Processing for the second button click
                return render_template("up_doct.html")
            elif button_clicked == 'btn3':
                # Processing for the second button click
                return render_template("doctor_details.html")
    except Exception as e:
        return f"Error :{e}!\nPlease Contact Developers"

    return "INVALID REQUEST"

@app.route("/insert_pat",methods=["post","Get"])
def insert_pat():
    
    try:
        
        if(request.method == "POST"):
            pat_id = request.form['patient_id']
            name = request.form['name']
            personal_details = request.form['personal_details']
            phone = request.form["contact_number"]
            disease = request.form["disease_name"]
            Treatment = request.form["treatments"]
            department = request.form["department"]
            doctor_id = request.form["doctor_id"]
            button_clicked = request.form['button_clicked']
            if(button_clicked == "btn1"):
                print(type(phone))
                query = f"insert into {table1} values('{pat_id}','{name}','{personal_details}','{phone}','{disease}','{Treatment}','{department}','{doctor_id}')"
                print(query)
                cursor.execute(query)
                connection.commit()
                print("Completed")
                return "Submited"
    except Exception as e:
        return f"Error :{e}!\nPlease Contact Developers"
    return "Invalid request"

@app.route("/insert_doctor",methods=["post","Get"])
def insert_doctor():
    global table2
    try:
        
        if(request.method == "POST"):
            doct_id = request.form['doctor_id']
            name = request.form['name']
            phone = request.form["contact_number"]
            department = request.form["department"]
            pat_id = request.form["patient_id"]
            value = pat_id.split(",")
            button_clicked = request.form['button_clicked']
            if(button_clicked == "btn1"):
                query = f"insert into {table2} values('{doct_id}','{name}','{phone}','{department}','{pat_id}')"
                print(query)
                cursor.execute(query)
                connection.commit()
                
            if(len(value) != 0):
                for i in value:
                    query = f"insert into check_datas values('{doct_id}','{i}')"
                    cursor.execute(query)
                    connection.commit()
            else:
                query = f"insert into check_datas values('{doct_id}','{pat_id}')"
                cursor.execute(query)
                connection.commit()
            print("Completed")
            return "Submited"
    except Exception as e:
        return f"Error :{e}!\nPlease Contact Developers"
    return "Invalid request"


@app.route("/view_patient",methods=["post","Get"])
def view_patient():
    global val,table1
    try:
        if(request.method == "POST"):
            pat_id = request.form['patient_id']
            print(pat_id)
            button_clicked = request.form['button_clicked']
            if(button_clicked == "btn1"):
                query = f"select * from  {table1} where pat_id = '{pat_id}' "
                cursor.execute(query)
                result = cursor.fetchall() 
                val = result
                print(val)
                return render_template("details.html",results = val)
            if (button_clicked == "btn2"):
                query = f"delete from {table1} where pat_id = '{pat_id}'"
                cursor.execute(query)
                connection.commit()
                return render_template("del_comp.html")
    except Exception as e:
        return f"Error :{e}!\nPlease Contact Developers"
    return "Invalid request"

@app.route("/details",methods=["post","Get"])
def details():
    global val,table1
    try:
        if(request.method == "POST"):
            button_clicked = request.form['button_clicked']
            if(button_clicked == "btn1"):
                return render_template("firstpage.html")
    except Exception as e:
        return f"Error :{e}!\nPlease Contact Developers"
    return "Invalid request"

@app.route("/view_doctors",methods=["post","Get"])
def view_doctors():
    global val,table2
    try:
        if(request.method == "POST"):
            doct_id = request.form['doctor_id']
            
            button_clicked = request.form['button_clicked']
            if(button_clicked == "btn1"):
                query = f"select * from {table2} where doctor_id = '{doct_id}'"
                cursor.execute(query)
                result = cursor.fetchall() 
                val = result
                print(val)
                return render_template("doct_view.html",results = val)
            if (button_clicked == "btn2"):
                query = f"delete from check_datas where doctor_id = '{doct_id}'"
                cursor.execute(query)
                connection.commit()
                query = f"delete from {table2} where doctor_id = '{doct_id}'"
                cursor.execute(query)
                connection.commit()
                
                return render_template("del_comp.html")
                
    except Exception as e:
        return f"Error :{e}!\nPlease Contact Developers"
    return "Invalid request"

@app.route("/update_pat",methods=["post","Get"])
def update_pat():
    try:
        
        if(request.method == "POST"):
            pat_id = request.form['patient_id']
            name = request.form['name']
            personal_details = request.form['personal_details']
            phone = request.form["contact_number"]
            disease = request.form["disease_name"]
            Treatment = request.form["treatments"]
            department = request.form["department"]
            doctor_id = request.form["doctor_id"]
            button_clicked = request.form['button_clicked']
            if(button_clicked == "btn1"):
                print(type(phone))
                query = f"update {table1} set name = '{name}',personal_details = '{personal_details}',phone = '{phone}',disease = '{disease}',treatment = '{Treatment}',department = '{department}',doctor_id = '{doctor_id}' where pat_id = '{pat_id}'"
                print(query)
                cursor.execute(query)
                connection.commit()
                print("Completed")
                return render_template("updatecompleted.html")
    except Exception as e:
        return f"Error :{e}!\nPlease Contact Developers"
    return "Invalid request"
@app.route("/up_comp",methods=["post","Get"])
def up_comp():
    try:
        if(request.method == "POST"):
            button_clicked = request.form['button_clicked']
            if button_clicked == 'btn1':
                # Processing for the first button click
                return render_template("firstpage.html")
    except Exception as e:
        return f"Error :{e}!\nPlease Contact Developers"
    return "INVALID REQUEST"

@app.route("/up_doc",methods=["post","Get"])
def up_doc():
    try:
        if(request.method == "POST"):
                doct_id = request.form['doctor_id']
                name = request.form['name']
                phone = request.form["contact_number"]
                department = request.form["department"]
                pat_id = request.form["patient_id"]
                button_clicked = request.form['button_clicked']
                if(button_clicked == "btn1"):
                    print(type(phone))
                    query = f"update {table2} set name = '{name}',contact_number = '{phone}',department = '{department}',patient_id ='{pat_id}'"
                    print(query)
                    cursor.execute(query)
                    connection.commit()
                    print("Completed")
                    return render_template("updatecompleted.html")
    except Exception as e:
        return f"Error :{e}!\nPlease Contact Developers"
    return "Invalid request"

@app.route("/direct_page",methods=["post","Get"])
def direct_page():
    try:
        if(request.method == "POST"):
            button_clicked = request.form['button_clicked']
            if(button_clicked == "btn1"):
                return render_template("firstpage.html") 
        
    except Exception as e:
        return f"Error :{e}!\nPlease Contact Developers"
    return "Invalid request"

if(__name__ == "__main__"):
    app.run(debug = True)
