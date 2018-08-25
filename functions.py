# Importing MySQL module for Python
import pymysql.cursors, os


# (Using OS variables for security. These can be replaced with strings)


password = os.environ['BreakingNewsPassword']
username = os.environ['BreakingNewsUsername']
dbname = os.environ['BreakingNewsDB']
hostname = os.environ['SitegroundHostingIP']


# The DB class enables you to connect to a MySQL server without experiencing timeout exceptions.
class DB:
    conn = None
    cursor = None

    def connect(self):
        self.conn = pymysql.connect(host=hostname,
                             user=username,
                             password=password,
                             db=dbname,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor,
                             port=3306)

    def query(self, sql, para=0):
        try:
            if para!= 0:
                if len(para) == 2:
                    listy = []
                    for i in para:
                        listy.append(i)
                    mytuple = tuple(listy)
                    para = mytuple

                cursor = self.conn.cursor()
                cursor.execute(sql, para)
            else:
                cursor = self.conn.cursor()
                cursor.execute(sql)
        except:
            self.connect()
            if para != 0:
                cursor = self.conn.cursor()
                cursor.execute(sql, para)
            else:
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
    query = "INSERT INTO `users` (`username`,`password`) VALUES (%s, %s)"
    db.query(query, para=(username, password))

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
    query = "SELECT password FROM `users` WHERE username = %s"
    cursor = db.query(query, para=str(username))
    for row in cursor:
        if row["password"] == password:
            return True
        else:
            return False

# This function confirms that a given username exists.
def confirmUser(username):
    global db
    query = "SELECT username FROM `users` WHERE username = %s"
    cursor = db.query(query, para=str(username))
    for row in cursor:
        if row["username"] != None:
            return True
        else:
            return False


# This function helps you find a user's Trello token by username.
def lookupToken(username):
    global db
    query = "SELECT trellotoken FROM `users` WHERE username = %s"
    cursor = db.query(query, para=str(username))
    for row in cursor:
        if row["trellotoken"] != None:
            return True
        else:
            return False


# This function sets up the table required for storing news stories.
def initStoryTable():
    global db
    query = "CREATE TABLE IF NOT EXISTS `stories`( `datanumber` int NOT NULL AUTO_INCREMENT, `source` text NOT NULL, `headline` text NOT NULL, `url` text NOT NULL, PRIMARY KEY (datanumber)) ENGINE=MEMORY;"
    db.query(query)

# This function adds a trello token value to a user's account.
def addToken(username, token):
    global db
    query = "UPDATE `users` SET trellotoken = %s WHERE username = %s"
    db.query(query, para=(str(token), str(username)))

# This function gets a user's trello token from the database.
def getToken(username):
    global db
    query = "SELECT trellotoken FROM `users` WHERE username = %s"
    cursor = db.query(query, para=str(username))
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

# This function sets up the table required for News Finder's API.
def initApiTable():
    global db
    query = "CREATE TABLE IF NOT EXISTS `API`( `datanumber` int NOT NULL AUTO_INCREMENT, `username` text NOT NULL, `apikey` text NULL, `token` text NULL, PRIMARY KEY (datanumber)) ENGINE=MEMORY;"
    db.query(query)

# This function will either return the user's key or return False.
def lookupApiKey(username):
    global db
    query = "SELECT apikey FROM `API` WHERE username = %s"
    cursor = db.query(query, para=str(username))
    row = cursor.fetchone()
    if row != None:
        if row["apikey"] != None and len(row["apikey"]) > 0 and row["apikey"] != "":
            return row["apikey"]
        else:
            return False
    else:
        return False

# This function will either return True or False, depending on if the user has API row in API DB.
def confirmApiUser(username):
    global db
    query = "SELECT username FROM `API` WHERE username = %s"
    cursor = db.query(query, para=str(username))
    row = cursor.fetchone()
    if row != None:
        if row["username"] != None:
            return True
        else:
            return False
    else:
        return False

# This function adds users to database.
def createApiUser(username):
    global db
    query = "INSERT INTO `API` (`username`) VALUES (%s)"
    db.query(query, para=str(username))

# This function adds the api key to the user's row in the data table.
def addApiKey(username, key):
    global db
    query =  "UPDATE `API` SET apikey = %s WHERE username = %s"
    db.query(query, para=(str(key), str(username)))

# This function generates an API key.
def createApiKey(username):
    from binascii import hexlify
    import os
    genkey = str(hexlify(os.urandom(32)))
    global db
    query = "SELECT apikey FROM `API` WHERE apikey = %s"
    cursor = db.query(query, para=str(genkey))
    row = cursor.fetchone()
    if row != None:
        if row["apikey"] != None:
            createApiKey(username)
    else:
        addApiKey(username, genkey)
        return genkey

def checkApiKey(key):
    global db
    query = "SELECT apikey FROM `API` WHERE apikey = %s"
    cursor = db.query(query, para=str(key))
    row = cursor.fetchone()
    if row != None:
        return True
    else:
        return False

# Returns false if no stories can be found - or if no such given source exists.
def getStories(source=0):
    if source != 0:
        if source == "foxnews":
            source = "Fox News"
        if source == "dailywire":
            source = "Daily Wire"
        if source == "gatewaypundit":
            source = "Gateway Pundit"
        if source == "wnd":
            source = "WND"
        if source == "conservativetribune":
            source = "Conservative Tribune"
        if source == "foxnewsinsider":
            source = "Fox News Insider"
        if source == "thehill":
            source = "The Hill"
        if source == "ijreview":
            source = "IJ Review"
        if source == "breitbart":
            source = "breitbart"
        if source == "freebeacon":
            source = "Free Beacon"
        if source == "dennismichaellynch":
            source = "Dennis Michael Lynch"
        if source == "westernjournal":
            source = "Western Journal"
        if source == "judicialwatch":
            source = "Judicial Watch"
        if source == "dailycaller":
            source = "Daily Caller"
        if source == "weaselzippers":
            source = "Weasel Zippers"
        query = "SELECT * FROM `stories` WHERE website = %s"
        cursor = db.query(query, para=str(source))
        stories = []
        for row in cursor:
            rowstory = {}
            rowstory["headline"] = row["headline"]
            rowstory["source"] = row["website"]
            rowstory["url"] = row["url"]
            stories.append(rowstory)
        if len(stories) > 0:
            return stories
        else:
            return False
    else:
        query = "SELECT * FROM `stories` WHERE 1"
        cursor = db.query(query)
        stories = []
        for row in cursor:
            rowstory = {}
            rowstory["headline"] = row["headline"]
            rowstory["source"] = row["website"]
            rowstory["url"] = row["url"]
            stories.append(rowstory)
        if len(stories) > 0:
            return stories
        else:
            return False
