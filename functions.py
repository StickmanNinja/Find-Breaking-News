# Importing MySQL module for Python
import pymysql.cursors, os


# (Using OS variables for security. These can be replaced with strings)
password = os.environ['BreakingNewsPassword']
username = os.environ['BreakingNewsUsername']
dbname = os.environ['BreakingNewsDB']
hostname = os.environ['SitegroundHostingIP']

conn = pymysql.connect(host=hostname,
                             user=username,
                             password=password,
                             db=dbname,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


# The DB class enables you to connect to a MySQL server without experiencing timeout exceptions.
class DB:
    conn = None

    def connect(self):
        self.conn = pymysql.connect(host=hostname,
                             user=username,
                             password=password,
                             db=dbname,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    def query(self, sql):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
        except:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(sql)
        return cursor


# Creating new instance of DB class
db = DB()

# Creating a function that creates required data table.
def initTable():
    global db
    query = "CREATE TABLE IF NOT EXISTS `users`( `datanumber` int NOT NULL AUTO_INCREMENT, `username` text NOT NULL, `password` text NOT NULL, `trellotoken` text NULL, `trelloboardid` text NULL, `email` text NULL, PRIMARY KEY (datanumber)) ENGINE=MEMORY;"
    db.query(query)

# This function adds users to database.
def createUser(username, password):
    global db
    query = "INSERT INTO `users` (`username`,`password`) VALUES ('%s', '%s')" % (username, password)
    db.query(query)

# This function checks to see if username is available. If so, it returns True.
def checkUser(username):
    global db
    query = "SELECT * FROM `users` WHERE username = '" + str(username) + "'"    
    cursor = db.query(query)
    row = cursor.fetchone()
    if row == None:
       return True
    else:
        return False;

# This function returns true if the string meets set guidlines for username and password.
def checkString(password):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    alphabet = alphabet.split()
    for i in range(0,9):
        alphabet.append(i)
    if len(password) > 20:
        return False
    for i in password:
        if isinstance(i, (int, long)) == False:
            if i.lower() not in alphabet == True:
                return False
    return True

# This function looks for the username and password combo in database.
def lookupUser(username, password):
    global db
    query = "SELECT password FROM `users` WHERE username = '" + str(username) + "'"
    cursor = db.query(query)
    for row in cursor:
        if row["password"] == password:
            return True
        else:
            return False

# This function helps you find a user's Trello token by username.
def lookupToken(username):
    global db
    query = "SELECT trellotoken FROM `users` WHERE username = '" + str(username) + "'"
    cursor = db.query(query)
    for row in cursor:
        if row["trellotoken"] != None:
            return True
        else:
            return False


# This function sets up the table required for storing news stories.
def setupStoryTable():
    global db
    query = "CREATE TABLE IF NOT EXISTS `stories`( `datanumber` int NOT NULL AUTO_INCREMENT, `source` text NOT NULL, `headline` text NOT NULL, `url` text NOT NULL, PRIMARY KEY (datanumber)) ENGINE=MEMORY;"
    db.query(query)

# This function adds a trello token value to a user's account.
def addToken(username, token):
    global db
    query = "UPDATE `users` SET trellotoken='" + str(token) + "' WHERE username='" + str(username) + "'"
    db.query(query)

# This function gets a user's trello token from the database.
def getToken(username):
    global db
    query = "SELECT trellotoken FROM `users` WHERE username = '" + str(username) + "'"
    cursor = db.query(query)
    for row in cursor:
        if row["trellotoken"] != None:
            return str(row["trellotoken"])

# This function finds the shortlink in a url.
def getShortLink(url):
    newstring = ""
    url = url.replace("https://trello.com/b/", "")
    url = url.replace("/", ".")
    for i in url:
        if str(i) == ".":
            break
        else:
            newstring = newstring + str(i)
    return "https://trello.com/b/" + newstring



# This should always run to ensure the users table exists in the database.
initTable()
