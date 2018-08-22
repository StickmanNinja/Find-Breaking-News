from NewsFetcher import *
from functions import *

def uploadStories(stories):
    import time
    global db
    for story in stories:
        query = "INSERT INTO `stories` (website, headline, url) VALUES (%s, %s, %s)"
        db.query(query, (story["source"], story["headline"], story["url"]))
        print "Story uploaded."
        time.sleep(1)
start()
uploadStories(stories)
