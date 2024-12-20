如何使用(需要git,postman,python3)
1.新建文件夹，打开命令行并导航到该文件夹
2.输入 git clone https://github.com/sh1c/1.git将相关文件复制到文件夹
3.输入myenc\Scripts\activate激活虚拟环境
4.输入pip install -r requirements.txt安装api所需的包
5.输入python LOGIN_SQL.py 激活api 记录路径(有用)
6.启动postman,选择POST，json
7.注册:在postman输入API URP 路径+/register  输入框内输入{"username":"任意内容","password":"任意密码"} 若重复会返回{"message": "Username already exists"},否则返回{"message": "User registered successfully"}
8:登录:在postman输入API URP 路径+/login  输入框内输入{"username":"任意内容","password":"任意密码"} 若重复会返回{ "message": "Invalid username or password"},否则返回{"message": "Login successful"}
