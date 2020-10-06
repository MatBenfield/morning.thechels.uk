# import
import helper
import random
import json
import pathlib
from yahoo_fin import stock_info as si

root = pathlib.Path(__file__).parent.parent.resolve()
with open( root / "config/stocks.json", 'r') as filehandle:
  stocks_list = json.load(filehandle)


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
    final_output = helper.replace_chunk(index_contents, "stocks_marker", f"<ul>\n{string_output}</ul>")
    index_page.open("w").write(final_output)