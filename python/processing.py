 # importing modules
"""
Build and Process
"""
import os
import re
import random
import pathlib
import json
import requests
import feedparser
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
    return [
        {
            "domain": get_hostname(entry["link"].split("#")[0]),
            "title": entry["title"],
            "url": entry["link"].split("#")[0],
            "published": get_published_info(entry),
        }
        for entry in entries
    ]

# Get url parse
def get_hostname(url):
    domain = urlparse(url).hostname
    return domain

# publish date
def get_published_info(entry):
    if(entry["published"] is not none):
        return entry["published"].split("T")[0]
    elif(entry["pubDate"] is not none):
        return entry["pubDate"].split("T")[0]
    else:
        return "unknown"


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

# get array from Json
# foreach url in Json get feed
# get last item from eat feed and add them into the html
# get weather
# provide some links