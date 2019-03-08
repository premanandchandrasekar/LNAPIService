from flask import Flask, render_template, request
from flask import jsonify
import pyodbc

app = Flask(__name__)


@app.route('/', )
def func():
    return render_template('index.html')


@app.route('/report', methods=['GET', 'POST'])
def gen_report():
    if request.method == 'POST' or request.method == 'GET':
        cnxn = pyodbc.connect(
            'Driver={ODBC Driver 17 for SQL Server};Server=tcp:tataatsu-server.database.windows.net,1433;Database=tataatsu-database;Uid=tataatsuadmin@tataatsu-server;Pwd=Database@123;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
        cursor = cnxn.cursor()
        key = request.form['key']
        res = cursor.execute("SELECT * FROM QpSector where qp_id=" + key)
        cnxn.commit()
        op = []
        for row in res:
            op.append(list(row))

        return jsonify(op)


app.run(debug=True)
