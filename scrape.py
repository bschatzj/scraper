import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

from time import sleep
from random import randint

songs =[]
artists = []

titles = []
artist_name = []
mixes = []
bpms = []
genres = []
years = []

headers = {"Accept-Language": "en-US,en;q=0.5"}



pages = np.arange(1, 10, 1)

for page in pages: 
  page = requests.get("https://www.bpmdatabase.com/music/W?page=" + str(page))

  soup = BeautifulSoup(page.text, 'html.parser')
  movie_div = soup.find_all('a', class_="list-group-item col-sm-6 col-md-4" )
  
  sleep(randint(1,2))

  for container in movie_div:
        chars = ["+", "$", "/", ".", ",", "@", "&", "'", "(", ")"]
        artist = container.text
        artist = artist.replace(" ", "-")
        artist = artist.lower()
        for char in chars:
              artist = artist.replace(char, "")

        artists.append(artist)


for artist in artists: 
  
  page = requests.get("https://www.bpmdatabase.com/music/by/" + str(artist))
  
  soup = BeautifulSoup(page.text, 'html.parser')
  song_pages = soup.find_all('li')
  artist_pages = range(1, len(song_pages) - 4)
  sleep(randint(2,10))

  for page_number in artist_pages:
      url = "https://www.bpmdatabase.com/music/by/" + str(artist) + "/?page=" + str(page_number)
      print(url)
      new_page = requests.get(url)
      new_soup = BeautifulSoup(new_page.text, 'html.parser')

      songs_div = new_soup.find_all("tr",  {"class": ["odd", "even"]})

      
  for song in songs_div:
      title = song.find('td', class_="title").text if song.find('td', class_='title') else ''
      artistt = song.find('td', class_="artist").text  if song.find('td', class_='artist') else ''
      mix = song.find('td', class_="mix").text if song.find('td', class_="mix") else ''
      genre = song.find('td', class_="genre").text if song.find('td', class_="genre") else ''
      bpm = song.find('td', class_="bpm").text if song.find('td', class_="bpm") else ''
      year = song.find('td', class_="year").text if song.find('td', class_="year") else ''



      titles.append(title)
      artist_name.append(artistt)
      mixes.append(mix)
      genres.append(genre)
      bpms.append(bpm)
      years.append(year)


song_formatted = pd.DataFrame({
'title': titles,
'year': years,
'genre': genres,
'mix': mixes,
'bpm': bpms,
'artist': artist_name
})



song_formatted.to_csv('W-songs.csv')