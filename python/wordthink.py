
 # importing modules
import helper
import random
import pathlib
import feedparser

root = pathlib.Path(__file__).parent.parent.resolve()
url = "http://feeds.feedburner.com/wordthink/vIYJ"
entries = feedparser.parse(url)["entries"][:1]
for entry in entries:
    output_word = helper.remove_img_tags(entry['description'])
    output_word = output_word.replace("<p>","")
    output_word = output_word.replace("</p>","")
    print("latest: ", output_word)

# processing
if __name__ == "__main__":
    all_news = ""
    index_page = root / "index.html"
    index_contents = index_page.open().read()
    final_output = helper.replace_chunk(index_contents, "word_marker", f"<blockquote>\n{output_word}\n</blockquote>\n")
    index_page.open("w").write(final_output)