import datetime
import mysql.connector

class libSQL():
    def __init__(self):
        self.db = mysql.connector.connect(
            host = '1.1.1.1',
            user = 'daka',
            passwd = '123456',
            database = 'daka'
        )
        self.cur = self.db.cursor(dictionary=True)
    
    def get(self, sql):
        self.cur.execute(sql)
        return self.cur.fetchall()
    
    def put(self, sql):
        self.cur.execute(sql)
        self.db.commit()
        return self.cur.rowcount

    def getUsers(self):
        result = {}
        successList = []
        today = datetime.datetime.now().strftime("%Y%m%d")
        users = self.get(r'select * from user where disabled="false"')
        for user in users:
            uid = str(user["id"])
            result[uid] = { "id": uid, "name": user["username"], "url": user["url"] }
            if today == user["lasttime"].strftime("%Y%m%d"):
                successList.append(uid)
        return result, successList


    def setUser(self, id, temp, status = None):
        if status is None:
            status = 'safety' if (temp < 37.3) else 'warning'
        self.cur.execute(r'UPDATE user SET status = "%s", lasttime = NOW() WHERE id = "%s"' % (status, id))
        self.cur.execute(r'INSERT INTO `log` (`id`, `uid`, `temp`, `time`) VALUES (NULL, "%s", "%s", NOW())' % (id, temp))
        self.db.commit()
        return self.cur.rowcount

if __name__ == "__main__":
    db = libSQL()
    print(db.getUsers())
