
 # importing modules
import helper
import random
import pathlib
import json


# setup
root = pathlib.Path(__file__).parent.parent.resolve()
with open( root / "config/quotes.json", 'r') as filehandle:
  random_quote = random.choice(json.load(filehandle))
  random_quote = random_qutoe.replace("-","<br/> -")

# processing
if __name__ == "__main__":
    all_news = ""
    index_page = root / "index.html"
    index_contents = index_page.open().read()
    final_output = helper.replace_chunk(index_contents, "quote_marker", f"<blockquote>\n{random_quote}\n</blockquote>\n")
    index_page.open("w").write(final_output)