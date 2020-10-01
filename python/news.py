
 # importing modules
import os
import re
import random
import pathlib
import json
import requests
import feedparser
import datefinder
from datetime import datetime
from urllib.parse import urlparse
from operator import itemgetter, attrgetter, methodcaller

# setup
root = pathlib.Path(__file__).parent.parent.resolve()
with open( root / "config/websites.json", 'r') as filehandle:
  url_list = json.load(filehandle)

# Replacer function
def replace_chunk(content, marker, chunk):
    replacer = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    chunk = "<!-- {} starts -->\n{}\n<!-- {} ends -->".format(marker, chunk, marker)
    return replacer.sub(chunk, content)

class article:
        def __init__(self, published, title, url):
                self.published = published
                self.title = title
                self.url = url
                self.domain = self.get_hostname(url)
        def __repr__(self):
            return repr((self.published, self.title, self.url, self.domain))

        def get_hostname(self, url):
            domain = urlparse(url).hostname
            return domain

# Get Entries Function
def get_entries(url_list):
    articles = list()
    for working_url in url_list:
        print(working_url)
        entries = feedparser.parse(working_url)["entries"][:5]
        for entry in entries:
            try:
                published_matches = list(datefinder.find_dates(entry['published']))
                if len(published_matches) > 0:
                    published_str_dt = published_matches[0].strftime("%Y-%m-%d %H:%M:%S")
                else:
                    published_str_dt = ""
            except KeyError:
                print("error with publishing " + entry['link'])
                published_str_dt = ""
            articles.append(article(published_str_dt,entry["title"],entry["link"].split("#")[0]))
    return articles

# processing
if __name__ == "__main__":
    all_news = ""
    index_page = root / "index.html"
    index_contents = index_page.open().read()
    entries_data = sorted(get_entries(url_list), key=attrgetter('published'), reverse=True)
    for output_articles in entries_data[:15]:
        all_news += f'<li>{output_articles.title}<br/><small><a href="{output_articles.url}" target="new">{output_articles.domain}</a> | Published {output_articles.published}</small></li>\n'
    final_output = replace_chunk(index_contents, "content_marker", f"<ul>\n{all_news}</ul>")
    index_page.open("w").write(final_output)