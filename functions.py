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

# Creating a function that creates required data table.
def initTable():
    global conn
    cursor = conn.cursor()
    query = "CREATE TABLE IF NOT EXISTS `users`( `datanumber` int NOT NULL AUTO_INCREMENT, `username` text NOT NULL, `password` text NOT NULL, `trellotoken` text NULL, `trelloboardid` text NULL, `email` text NULL, PRIMARY KEY (datanumber)) ENGINE=MEMORY;"
    cursor.execute(query)

# This function adds users to database.
def createUser(username, password):
    global conn
    cursor = conn.cursor()
    query = "INSERT INTO `users` (`username`,`password`) VALUES (%s, %s)"
    cursor.execute(query, [username, password])

# This function checks to see if username is available. If so, it returns True.
def checkUser(username):
    global conn
    cursor = conn.cursor()
    query = "SELECT * FROM `users` WHERE username = '" + str(username) + "'"
    cursor.execute(query)
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
    global conn
    cursor = conn.cursor()
    query = "SELECT password FROM `users` WHERE username = '" + str(username) + "'"
    cursor.execute(query)
    for row in cursor:
        if row["password"] == password:
            return True
        else:
            return False

def lookupToken(username):
    global conn
    cursor = conn.cursor()
    query = "SELECT trellotoken FROM `users` WHERE username = '" + str(username) + "'"
    cursor.execute(query)
    for row in cursor:
        if row["trellotoken"] != None:
            return True
        else:
            return False


# This function sets up the table required for storing news stories.
def setupStoryTable():
    global conn
    cursor = conn.cursor()
    query = "CREATE TABLE IF NOT EXISTS `stories`( `datanumber` int NOT NULL AUTO_INCREMENT, `source` text NOT NULL, `headline` text NOT NULL, `url` text NOT NULL, PRIMARY KEY (datanumber)) ENGINE=MEMORY;"
    cursor.execute(query)

def addToken(user, token):
    global conn
    cursor = conn.cursor()
    query = "UPDATE `users` SET trellotoken='" + str(token) + "' WHERE username='" + str(username) + "'"
    cursor.execute(query)

# This should always run to ensure the users table exists in the database.
initTable()
