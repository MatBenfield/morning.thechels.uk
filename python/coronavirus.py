# import
from requests import get
import re
import json
import pathlib
import os

root = pathlib.Path(__file__).parent.parent.resolve()
city = os.getenv('city_code')

# Methods
def replace_chunk(content, marker, chunk):
    replacer = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    chunk = "<!-- {} starts -->\n{}\n<!-- {} ends -->".format(marker, chunk, marker)
    return replacer.sub(chunk, content)


def get_covid_data(num_days):
    endpoint = (
        f'https://api.coronavirus.data.gov.uk/v1/data?filters=areaType=ltla;areaName={city}&'
        'structure={"date":"date","newCases":"newCasesByPublishDate","deaths":"newDeathsByDeathDate"}'
    )
    response = get(endpoint, timeout=10)
    if response.status_code >= 400:
        raise RuntimeError(f'Request failed: { response.text }')
    string_builder = ""
    data = response.json()['data'][:num_days]
    for i in range(0, num_days):
        string_builder += (f"<li>{0 if data[i]['newCases'] == None else data[i]['newCases']} new cases & "
        f"{0 if data[i]['deaths'] == None else data[i]['deaths']} deaths ")
        if i == 0:
            string_builder += "today"
        elif i == 1:
            string_builder += "yesterday"
        else:
            string_builder += f"on {data[i]['date']}"
        string_builder += "</li>\n"
    return string_builder


# output
if __name__ == "__main__":
    index_page = root / "index.html"
    index_contents = index_page.open().read()
    string_output = get_covid_data(5)

    final_output = replace_chunk(index_contents, "covid_marker", f"<ul>\n{string_output}</ul>")
    index_page.open("w").write(final_output)
