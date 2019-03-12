from flask import Flask, render_template, request
from flask import jsonify
import json
import pypyodbc as pyodbc
from datetime import datetime

app = Flask(__name__)
cnxn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:tataatsu-server.database.windows.net,1433;Database=tataatsu-database;Uid=tataatsuadmin@tataatsu-server;Pwd=Database@123;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
cursor = cnxn.cursor()


@app.route('/',)
def func():
   return "api service"

@app.route('/qp', methods = ['GET', 'POST'])
def op_api1():
    if request.method == 'POST' or request.method == 'GET':
        
        key = request.form['key']
        res = cursor.execute("SELECT * FROM QpSector where qp_id="+key)
        op = []
        for row in res:
            opdict = {}
            opdict['qp_id'] = row[0]
            opdict['qp_code'] = row[1]
            opdict['qp_name'] = row[2]
            opdict['sector'] = row[3]
            op.append(opdict)
        return jsonify(op)

@app.route('/candidate', methods = ['GET', 'POST'])
def op_api2():
    if request.method == 'POST' or request.method == 'GET':
        key = request.form['key']
        datetime_key = str(datetime.strptime(key, '%Y-%m-%d'))
        datetime_key = datetime_key[0:10]+'T00:00:00.0000000'
        print(datetime_key)
        res = cursor.execute("SELECT * FROM api2 where end_date <= '"+datetime_key+"'")
        op = []
        for row in res:
            op.append(list(row))
        for row in op:
            res = cursor.execute("SELECT center_id FROM CenterMaster where center_name ='"+row[0]+"'")
            for x in res:
                print(x[0])
                row.append(x[0])
                break
        return jsonify(op)

@app.route('/attendance', methods = ['GET', 'POST'])
def op_api3():
    if request.method == 'POST' or request.method == 'GET':
      key = request.form['key']
      datetime_key = str(datetime.strptime(key, '%Y-%m-%d'))
      datetime_key = datetime_key[0:10]+'T00:00:00.0000000'
      print(datetime_key)
      res = cursor.execute("SELECT AttendanceMaster.*, BatchMaster.center_name,BatchMaster.course_code,QpMaster.level_code,CenterMaster.center_id FROM AttendanceMaster inner join BatchMaster on AttendanceMaster.batch_id = BatchMaster.batch_code inner join QpMaster on AttendanceMaster.level_name=QpMaster.level_name inner join CenterMaster on BatchMaster.center_name=CenterMaster.center_name where AttendanceMaster.session_attendance_taken_date = '"+datetime_key+"'")
      print(res)
      op = []
      for row in res:
         opdict = {}  
         opdict['batch_id'] = row[0]
         #opdict['course_name'] = row[1]
         #opdict['qp_name'] = row[2]
         opdict['date'] = row[3]
         opdict['status'] = row[4]
         opdict['count'] = row[5]
         #opdict['center_name'] = row[6]
         opdict['course_code'] = row[7]
         opdict['qp_code'] = row[8]
         opdict['center_code'] = row[9]
         op.append(opdict)
      print(op)
      return jsonify(op)


app.run(host='0.0.0.0',debug=True)
#app.run(host='0.0.0.0',port=8000)
