import MySQLdb
def table():
    db=MySQLdb.connect("localhost","root","w999123321","flight")
    cursor = db.cursor()
    sql = "SELECT * FROM route"
    cursor.execute(sql)
    results = cursor.fetchall()
    print results

if __name__ == '__main__':
    table()