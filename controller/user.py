from database.mysql import get_db
from model import user
from fastapi import Depends
from mysql.connector import cursor


def Select_user(users: user.User, mysql: cursor.MySQLCursor = Depends(get_db)):
    try:

        # sql
        sql = '''SELECT id, user_name, password, uid, sys, last_date FROM `user` WHERE user_name=%s AND password=%s'''

        # 查询
        mysql.execute(sql, (users.username, users.password))

        data = mysql.fetchall()

        # 赋值
        user.id = data[0][0]
        user.username = data[0][1]
        user.password = data[0][2]
        user.user_info = user.UserInfo(
            uid=data[0][3],
            sys=data[0][4],
            last_date=data[0][5]
        )
        # 返回数据
        return user

    except Exception as e:
        print(e)

        # 抛出异常返回 none
        return None
