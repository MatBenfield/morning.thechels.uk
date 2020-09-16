"""
Build and Process
"""

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

# setup
root = pathlib.Path(__file__).parent.parent.resolve()
with open( root / "websites.json", 'r') as filehandle:
  url_list = json.load(filehandle)

# Replacer function
def replace_chunk(content, marker, chunk):
    replacer = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    chunk = "<!-- {} starts -->\n{}\n<!-- {} ends -->".format(marker, chunk, marker)
    return replacer.sub(chunk, content)

# Get Entries Function
def fetch_blog_entries(working_url):
    entries = feedparser.parse(working_url)["entries"]
    entries_data = []
    for entry in entries:

        try:
            published_matches = list(datefinder.find_dates(entry['published']))
            if len(published_matches) > 0:
                published_str_dt = published_matches[0].strftime("%d %b %Y")
            else:
                published_str_dt = ""
        except KeyError:
            print("published" + entry['link'])
            published_str_dt = ""

        entries_data.append({
            "domain": get_hostname(entry["link"].split("#")[0]),
            "title": entry["title"],
            "url": entry["link"].split("#")[0],
            "published": published_str_dt,
        })
    return entries_data
    #return entries_data.sort(key=lambda x: x["published_str_dt"], reverse=True)

# Get url parse
def get_hostname(url):
    domain = urlparse(url).hostname
    return domain

# processing
if __name__ == "__main__":
    all_news = "<h2>News</h2>\n"
    index_page = root / "index.html"
    index_contents = index_page.open().read()

    for url in url_list:
        entries = fetch_blog_entries(url)[:1]
        domain = get_hostname(url)
        data_item_text = "\n\n".join(["<p><a href='{url}' target='new'>{title}</a><br/><small>{domain} | Published: {published}</small></p>\n"
                                    .format(**entry) for entry in entries])
        all_news += data_item_text
    final_output = replace_chunk(index_contents, "content_marker", all_news)
    index_page.open("w").write(final_output)
