#!/usr/bin/python3

import feedparser
import pickle
import os.path
import time
import datetime
import sys

a = [ 'krowod', 'morel', 'bazow', 'rudaw', 'telefon', 'justowsk' ]
urls = [ 'https://www.bip.krakow.pl/feeds/rss/komunikatynowe/30700', #RSS wszczecie LICP
	'https://www.bip.krakow.pl/feeds/rss/komunikatynowe/30707', #RSS postanowienia LICP
	'https://www.bip.krakow.pl/feeds/rss/komunikatynowe/30708', #RSS decyzje LICP
	'https://www.bip.krakow.pl/feeds/rss/komunikatynowe/30711', #RSS WZ dla przeds. mog. znaczaco oddz na sr
	'https://www.bip.krakow.pl/feeds/rss/komunikatynowe/68705', #RSS zgloszenia budowy
	'https://www.bip.krakow.pl/feeds/rss/komunikatynowe/30616', #RSS postepowanie dec srod
	'https://www.bip.krakow.pl/feeds/rss/komunikatynowe/30618', #RSS dec srod
	'https://www.bip.krakow.pl/feeds/rss/komunikatynowe/30612' ] #RSS planowanie przestrzenne
#	'https://www.bip.krakow.pl/feeds/rss/komunikatynowe/30593' ]

if os.path.exists('rss.pickle'):
	with open('rss.pickle', 'rb') as f:
		old_entries = pickle.load(f)
else:
	old_entries = []

start_time = datetime.datetime.now()

while (1) :
	entries = []
	for url in urls:
		d = feedparser.parse(url)
		entries += [ entry for entry in d.entries if any(x in entry.title.lower() or x in entry.summary.lower() for x in a) ]

	now = datetime.datetime.now()
	now_str = now.strftime('%Y-%m-%d %H:%M:%S')
	if entries != old_entries:
		with open('rss.pickle', 'wb') as f:
			pickle.dump(entries, f)
		text_to_add = ''
		added = 0
		for kom in entries:
			if kom not in old_entries:
				link_text = kom.summary if kom.summary else (' ' + kom.title)
				text_to_add += kom.published
#				text_to_add += (' <a href="' + kom.title_detail.base + '">' + kom.title_detail.base + '</a><br>')
				text_to_add += ('<a href="' + kom.link + '">' + link_text + '</a>')
				added += 1
		header = ('<tr><td><b>' + now_str + ' (' + str(added) + ')</b></td><td>')
		text_to_add += '</td></tr>'
		if added > 0:
			with open('../../web/index.html', 'a') as f:
				f.write(header)
				f.write(text_to_add)
		old_entries = entries
	
	with open('../../web/activity.html', 'w') as f:
		f.write('<p><center><b>Last run on: ' + now_str + ' Up: ' + str(now - start_time) + '</b><br>Search criteria: ')
		for word in a:
			f.write(word + ' ')
		f.write('<br>Search urls:')
		for url in urls:
			f.write('<a href="' + url + '">' + url + '</a>, ')
		f.write('</center></p>')
	time.sleep(24*60*60)




