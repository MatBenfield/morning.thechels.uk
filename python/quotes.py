
 # importing modules
import re
import random
import pathlib
import json


# setup
root = pathlib.Path(__file__).parent.parent.resolve()
with open( root / "config/quotes.json", 'r') as filehandle:
  random_quote = random.choice(json.load(filehandle))

# Replacer function
def replace_chunk(content, marker, chunk):
    replacer = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    chunk = "<!-- {} starts -->\n{}\n<!-- {} ends -->".format(marker, chunk, marker)
    return replacer.sub(chunk, content)

# processing
if __name__ == "__main__":
    all_news = ""
    index_page = root / "index.html"
    index_contents = index_page.open().read()
    final_output = replace_chunk(index_contents, "quote_marker", f"<blockquote>\n{random_quote}\n</blockquote>\n")
    index_page.open("w").write(final_output)