
from flask import Flask, request, jsonify,render_template
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash,check_password_hash
import jwt,datetime
from functools import wraps

app = Flask(__name__)
#app.config['SECRET_KEY'] = '123456' 目前不知道咋用-------------------------------
# 配置MySQL数据库连接
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'mydatabase'

mysql = MySQL(app)

#Token 密钥
secret_key = "dingtinayi"

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
        # Token的创建(有效的token)
        token = jwt.encode({
            "name":username,
            "exp":datetime.datetime.utcnow()+datetime.timedelta(minutes=30)},
            secret_key,algorithm="HS256")

        return jsonify({'message': 'Login successful',"token":token}), 200
    else:
        # Token的创建(无效的token)防止登录错误的用户使用未过期的token访问商城界面
        token = jwt.encode({
            "exp":datetime.datetime.utcnow()+datetime.timedelta(minutes=30)
        },secret_key,algorithm="HS256")
        return jsonify({'message': 'Invalid username or password',"token":token}), 401


#商城页面API
@app.route("/storeMenu",methods=['GET'])
def menu():
    token = request.headers.get("Authorization")

    if not token:
        return jsonify("Token is missing"),401
    try:
        token = token.split(" ")[1]
        data = jwt.decode(token,secret_key,algorithms=["HS256"])
        username = data.get("name")
        #连接数据库
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()

        #检测token是否有效
        if not user:
            return jsonify({"message":"Token is invalid"}),401
        
        return render_template("store.html"),200
    except jwt.ExpiredSignatureError:
         return jsonify({"message": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token"}), 401
            


        
    
if __name__ == '__main__':
    app.run(debug=True)
