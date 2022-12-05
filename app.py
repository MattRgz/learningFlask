from flask import Flask, render_template,jsonify,request
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = "Content-type"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mymarket'
mysql = MySQL(app)

if __name__ == '__main__':
    app.run(None, 3000, True)


@app.route('/api/customers/<int:id>')
@cross_origin()
def getCustomer(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM customers WHERE id="+ str(id) + ";")
    data = cur.fetchall()
    for row in data:
        content = { 'id':row[0], 'nombre':row[1],'apellido':row[2] }
    return jsonify(content)

@app.route('/api/customers')
@cross_origin()
def getAllCustomers():
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM customers')
    data = cur.fetchall()
    result=[]
    for row in data:
        content = { 'id':row[0], 'nombre':row[1],'apellido':row[2], 'telefono':row[3], 'mail':row[4]}
        result.append(content)
    return jsonify(result)

@app.route('/api/customers/update/<int:id>', methods=['PUT'])
@cross_origin()
def updateCustomer(id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE customers SET nombre= %s, apellido= %s, telefono= %s, mail= %s WHERE id = %s",
        (request.json['nombre'],
        request.json['apellido'],
        request.json['telefono'],
        request.json['mail'],
        str(id)))
    mysql.connection.commit()
    return "Cliente guardado"

@app.route('/api/customers', methods=['POST'])
@cross_origin()
def saveCustomer():
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO customers (nombre,apellido,telefono,mail) VALUES (%s,%s,%s,%s)",
        (request.json['nombre'],
        request.json['apellido'],
        request.json['telefono'],
        request.json['mail']))
    mysql.connection.commit()
    return "Cliente guardado"

@app.route('/api/customers/<int:id>', methods=['DELETE'])
@cross_origin()
def removeCustomer(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM customers WHERE id ="+ str(id)+ ";")
    mysql.connection.commit()
    return "Cliente eliminado"

@app.route('/')
def index():
    return render_template('index.html')
