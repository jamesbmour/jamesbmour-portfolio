import requests
import json
import datetime
import dateutil.parser
from os import path
from typing import List

class ArticleStats(object):
    def __init__(self, date: str, page_views_count: int, public_reactions_count: int, comments_count: int):
        self.date = date
        self.page_views_count = page_views_count
        self.public_reactions_count = public_reactions_count
        self.comments_count = comments_count

class Article(object):
    def __init__(self, title: str, published: str, stats: List[ArticleStats] = []):
        self.title = title
        self.published = published
        self.stats = stats

class DevStats(object):
    def __init__(self, articles: List[Article]):
        self.articles = articles

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


url = "https://dev.to/api/articles/me"
headers = {
    'api-key': 'YOUR-PRIVATE-API-KEY-HERE', # You have to put your own api-key here. How to get a api-key: https://docs.dev.to/api/#section/Authentication/api_key
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'
}

statsFilename = "devToArticleStats.json"
if(path.exists(statsFilename)): # If the statistics json file already exist then read it so we later can append the retrieved data to it
    statsFile = open(statsFilename, 'r')
    devToStatsJson = str(statsFile.read())
    statsFile.close()
else:
    devToStatsJson = '{ "articles": []  }'

devToJson = requests.get(url, headers=headers).json() # Call the api to retrieve the statustics
devToStatsDict = json.loads(devToStatsJson)
devToStats = DevStats(**devToStatsDict)

articleStats = ""
for articleFromDev in devToJson:
    publishedObj = dateutil.parser.isoparse(articleFromDev['published_at'])
    publishedStr = datetime.datetime.strftime(publishedObj, "%d-%m-%Y %H:%M:%S")
    title = articleFromDev['title']
    pageViews = articleFromDev['page_views_count']
    reactions = articleFromDev['public_reactions_count']
    comments = articleFromDev['comments_count']
    existingArticle = next((article for article in devToStats.articles if article['title'] == title), None) # Get the article from the dictionary if it exists else add a new instance
    if existingArticle == None:
      existingArticle = {'title': title, 'published': publishedStr, 'stats': []}
      devToStats.articles.append(existingArticle)

    today = str(datetime.date.today())
    articleStats = next((stats for stats in existingArticle['stats'] if stats['date'] == today), None)  # Get the stats for today from the dictionary if it exists else add a new instance
    if articleStats == None:
      articleStats = ArticleStats(today, pageViews, reactions, comments)
      existingArticle['stats'].append(articleStats)
    else:
      articleStats['page_views_count'] = pageViews
      articleStats['public_reactions_count'] = reactions
      articleStats['comments_count'] = comments

statsFile = open(statsFilename, 'w') # Save the article stats to the statistics json file
statsFile.write(devToStats.toJSON())
statsFile.close()
