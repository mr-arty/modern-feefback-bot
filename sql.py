import pymysql
from log import log
from config import HOSTD, USER, PASS, DB


sql_log = log('sql', 'sql.log', 'ERROR')


def get_connection():
    """
    Function for getting connection data
    :return: <pymysql.connections.Connection>
    """
    return pymysql.connections.Connection(host=HOSTD, user=USER, password=PASS, db=DB, charset='utf8mb4')


def add_user(user_id, first_name, last_name, username):
    """
    Function for adding a user to DB
    :param user_id: <int> - a id of a user
    :param first_name: <str> or <None> - user's first name
    :param last_name: <str> or <None> - user's last name
    :param username: <str> or <None> - user's  nickname
    :return: <bool>
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM users WHERE user_id = %s;', (user_id,))
            if cursor.fetchone() is None:
                if username is not None and len(username) > 35:
                    username = username[0:35]
                if first_name is not None and len(first_name) > 50:
                    first_name = first_name[0:35]
                if last_name is not None and len(last_name) > 50:
                    last_name = last_name[0:35]
                cursor.execute(
                    'INSERT INTO `users` (user_id, username, first_name, last_name) VALUES (%s, %s, %s, %s);',
                    (user_id, username, first_name, last_name))
            connection.commit()
            return True
    except Exception as error:
        sql_log.error(error.with_traceback(None))
        return False
    finally:
        connection.close()


def user_count():
    """
    Function for getting a count of users
    :return: <int> or <boll: False>
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT COUNT(id) FROM users;')
            return cursor.fetchone()[0]
    except Exception as error:
        sql_log.error(error.with_traceback(None))
        return False
    finally:
        connection.close()


def get_users():
    """
    Function for getting a list of users
    :return: <list> like [<int>, <int>, <int>] or <bool: False>
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT user_id FROM users;')
            users = cursor.fetchall()
            return [user[0] for user in users] or []
    except Exception as error:
        sql_log.error(error.with_traceback(None))
        return False
    finally:
        connection.close()


def get_admins():
    """
    Function for getting list of admins
    :return: <list> like [<int>, <int>, <int>] or <bool: False>
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT admin_id FROM admins;')
            admins_id = cursor.fetchall()
            return [admin_id[0] for admin_id in admins_id] or []
    except Exception as error:
        sql_log.error(error.with_traceback(None))
        return False
    finally:
        connection.close()


"""
############################################ These function isn't using now ############################################
"""


def ban_user(user_id):
    """
    Function for banning a user
    :param user_id: <int> - a id of a user
    :return: <list> or <bool: False>
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO bans (user_id) VALUES (%s);', (user_id,))
            cursor.execute('SELECT user_id FROM bans;')
            users_bans = cursor.fetchall()
            return [user_ban[0] for user_ban in users_bans] or []
    except Exception as error:
        sql_log.error(error.with_traceback(None))
        return False
    finally:
        connection.close()


def un_ban(user_id):
    """
    Function for unbanning a user
    :param user_id: <int> - a id of a user
    :return: <list> or <bool: False>
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM bans WHERE user_id = %s;', (user_id,))
            cursor.execute('SELECT user_id FROM bans;')
            users_bans = cursor.fetchall()
            return [user_ban[0] for user_ban in users_bans] or []
    except Exception as error:
        sql_log.error(error.with_traceback(None))
        return False
    finally:
        connection.close()


def get_ban_list():
    """
    Function for getting list of users which in ban
    :return: <list> or <bool: False>
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT user_id FROM bans;')
            users_bans = cursor.fetchall()
            return [user_ban[0] for user_ban in users_bans] or []
    except Exception as error:
        sql_log.error(error.with_traceback(None))
        return False
    finally:
        connection.close()
