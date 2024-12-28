
from flask import Flask, request, jsonify,session,render_template
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)
app.secret_key = "123456"
# 配置MySQL数据库连接
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'mydatabase'

mysql = MySQL(app)

# 注册API
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']

    # 检查用户名是否已存在
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    existing_user = cursor.fetchone()
    cursor.close()

    if existing_user:
        return jsonify({'message': 'Username already exists'}), 400

    #密码加密
    hashed_password = generate_password_hash(password)

    # 创建新用户
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'User registered successfully'}), 201

# 登录API
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    # 验证用户
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s ", (username,))
    user = cursor.fetchone()
    cursor.close()

    if user and check_password_hash(user[2],password) :
        session["username"]=username
        return jsonify({'message': 'Login successful'}), 200
    else:
        session.clear()
        return jsonify({'message': 'Invalid username or password'}), 401


#商城页面API
@app.route("/storeMenu",methods=['GET'])
def menu():
    if "username" in session and session["username"] is not None:
        return render_template("store.html")
    else:
        return render_template("404.html")
if __name__ == '__main__':
    app.run(debug=True)
