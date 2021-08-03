import requests
import csv
import json
import datetime


exp_file = 'data/polcompass.csv'

try:
    with open(exp_file) as f:
        file_size = f.tell()
        f.seek(max(file_size, 0))
        # this will get rid of trailing newlines, unlike readlines()
        latestts = int(f.read().splitlines()[-1].split(',')[0])
except:
    latestts = 1570491626

def fmt(str):
    if str is not None: return str.split(':')[1]
    else: return 'None'

def getPushshiftData(a, b):
    url = 'https://api.pushshift.io/reddit/comment/search/?size=1000&after='+str(a)+'&before='+str(b)+'&subreddit=PoliticalCompassMemes&filter=id,author,author_flair_text,created_utc'
    print(url)
    r = requests.get(url)
    data = json.loads(r.text)
    return data['data']

after, before = latestts, 1586948796
data = getPushshiftData(after, before)

# from the 'after' date up until before date

while len(data) > 0:
    exp_data = [[c['created_utc'], c['id'], c['author'], fmt(c['author_flair_text'])] for c in data]
    for c in data:
        print(c)
    with open(exp_file, 'a', newline='\n') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(exp_data)
    print("Saved " + str(len(exp_data)) + " new comments @ " + exp_file)


    # Calls getPushshiftData() with the created date of the last submission
    after = data[-1]['created_utc']
    print(str(len(data)) + " comments until " + str(datetime.datetime.fromtimestamp(after)))

    data = getPushshiftData(after, before)
