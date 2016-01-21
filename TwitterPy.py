# Author: TheLeopards (samantha Krawczyk, Georgios Anastasiou)
# 21 January 2016
# Harvesting twitter feed using REST API

from twython import Twython
import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


## codes to access twitter API. 
APP_KEY =  "hrRaPEjOxQZzwZ0Nbws5U51p9"
APP_SECRET =  "mJ6nfD4DgkxR8DqRO8ubxlyd9EYtPelfyUbTb7vftemwlspX3t"
OAUTH_TOKEN = "4479100752-t8V910nwN8BNfiBoKxSRDc8z3KPr3P7TBC4W0ER"
OAUTH_TOKEN_SECRET = "Pv8dNmD5RaVAfpHNq1sKd4Amlp9cBuK2Atvptkt3YWjSq"

## initiating Twython object 
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

## setting filter of tweets
geocode = "52.373056,4.893333,50km"
search_results = twitter.search(q='koffie', count=500, geocode = geocode)

## Creating lists to later create an array
CoordLat = list()
CoordLon = list()

## parsing out tweets that include coordinate data
for tweet in search_results["statuses"]:
    username =  tweet['user']['screen_name']
    followers_count =  tweet['user']['followers_count']
    tweettext = tweet['text']
    place =  tweet['place']

    coordinates = tweet['coordinates']
    if coordinates != None:
        coordinates = coordinates['coordinates']
        lat, lon = (coordinates[0], coordinates[1])
        CoordLat.append(lat)
        CoordLon.append(lon)
    
CoordArray = np.array([CoordLat, CoordLon])

## plotting the coordinate data
fig = plt.figure()
plt.subplots_adjust(left=0.05,right=0.95,top=0.90,bottom=0.05,wspace=0.15,hspace=0.05)
ax = plt.subplot(111)

m = Basemap(resolution='i',projection='merc', llcrnrlat=51.5,urcrnrlat=53.0,llcrnrlon=4.,urcrnrlon=6.0,lat_ts=51.0)
m.drawcountries(linewidth=0.5)
m.drawcoastlines(linewidth=0.5)

m.drawparallels(np.arange(49.,54.,1.),labels=[1,0,0,0],color='black',dashes=[3,1],linewidth=0.2) # draw parallels
m.drawmeridians(np.arange(1.,9.,1.),labels=[0,0,0,1],color='black',dashes=[3,1],linewidth=0.2)

x,y = m(CoordArray[0], CoordArray[1])
m.plot(x, y, 'bo', markersize=5)
plt.title("Tweets about coffee within 50km of Amsterdam, NL")
plt.show()

fig.savefig("CoffeeTweets.jpg")
