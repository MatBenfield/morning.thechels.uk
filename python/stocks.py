# import
import re
import random
import json
import pathlib
from yahoo_fin import stock_info as si

root = pathlib.Path(__file__).parent.parent.resolve()
with open( root / "config/stocks.json", 'r') as filehandle:
  stocks_list = json.load(filehandle)

# Methods
def replace_chunk(content, marker, chunk):
    replacer = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    chunk = "<!-- {} starts -->\n{}\n<!-- {} ends -->".format(marker, chunk, marker)
    return replacer.sub(chunk, content)

def get_stocks(set_of_tickers):
    string_builder = ""
    for ticker in list(set_of_tickers):
        string_builder += f"<li>{ticker} : {round(si.get_live_price(ticker),5)}</li>\n"
    return string_builder

# output
if __name__ == "__main__":
    index_page = root / "index.html"
    index_contents = index_page.open().read()
    string_output = get_stocks(stocks_list)
    final_output = replace_chunk(index_contents, "stocks_marker", f"<ul>\n{string_output}</ul>")
    index_page.open("w").write(final_output)