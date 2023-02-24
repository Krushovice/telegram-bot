import sqlite3



class Database:
    def __init__(self,db_file):
    #инициализация соедеения с БД
        self.connection = sqlite3.connect('base.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute ('''CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            user_id INTEGER UNIQUE,
            username TEXT UNIQUE,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL UNIQUE);
            ''')

    def user_exists(self,user_id):
        #Проверяем, есть ли юзер в БД
        with self.connection:
            result = self.cursor.execute("SELECT 'id' FROM 'users' WHERE 'user_id' = ?",(user_id,)).fetchall ()
            return bool(len(result))


    def get_user_id(self,user_id):
        #Получаем id юзера в базе по его user_id в телеграме
        result = self.cursor.execute ("SELECT 'id' FROM 'users' WHERE 'user_id' = ?",(user_id,))
        return result.fetchone()[0]


    def get_username(self,user_id,username):
        with self.connection:
            result = self.cursor.execute("SELECT 'username' FROM 'users' WHERE 'user_id = ?", (user_id, username,))
            return result.fetchone()[0]


    def add_user(self, user_id):
        # Добавляем юзера в базу данных
        self.cursor.execute("INSERT INTO 'users' ('user_id') VALUES(?)", (user_id,))
        return self.connection.commit()




    def close(self):
        #Закрытие соединения с БД
        self.connection.close()
