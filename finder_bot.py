from NewsFetcher import *
from functions import *

def uploadStories(x):
    global conn
    cursor = conn.cursor()
    import time
    for story in stories:
        query = "INSERT INTO `stories` (website, headline, url) VALUES (%s, %s, %s)"
        cursor.execute(query, [story["source"], story["headline"], story["url"]])
        print "Story uploaded."
        time.sleep(1)

setupStoryTable()
start()
uploadStories(stories)
