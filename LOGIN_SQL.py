
# from flask import Flask, request, jsonify
# from flask_mysqldb import MySQL
#
# app = Flask(__name__)
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = '123456'
# app.config['MYSQL_DB'] = 'mydatabase'
# mysql = MySQL(app)
# #登录api
# @app.route("/login",methods=["POST"])
# def login():
#     data = request.get_json()
#     username = data["username"]
#     psw = data["psw"]
#     #检测账号密码是否存在
#     cursor = mysql.connection.
#
# # 注册API
# @app.route('/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     username = data['username']
#     password = data['password']
#     #检测
# if __name__=="__main__":
#     app.run()
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL


app = Flask(__name__)

# 配置MySQL数据库连接
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'mydatabase'

mysql = MySQL(app)

# 登录API
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    # 验证用户
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()

    if user :
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

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



    # 创建新用户
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'User registered successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)