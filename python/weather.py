import os
import re
import pathlib
import json
import requests
from datetime import date

# setup
root = pathlib.Path(__file__).parent.parent.resolve()
lat=os.getenv('lat')
lon=os.getenv('lon')
APIKEY = os.getenv('open_weather_key')
url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&exclude=current,minutely,hourly,alerts&units=metric" %(lat,lon,APIKEY)
# headers = {"Authorization":"Bearer %s"%key}

response = requests.get(url)
response_dict = json.loads(response.text)
output_date = date.today()
today_weather = str(response_dict['daily'][0]['temp']['day'])
high_temp = str(response_dict['daily'][0]['temp']['max'])
low_temp = str(response_dict['daily'][0]['temp']['min'])
today_desc = str(response_dict['daily'][0]['weather'][0]['description'])

string_today =  f"Today's date is {output_date}, Here is your daily briefing..."
string_today += f"The average temperature today is {today_weather}˚C with highs of {high_temp}˚C and lows of {low_temp}˚C. "
string_today += f"You can expect {today_desc} for the day."

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
    index_page = root / "index.html"
    index_contents = index_page.open().read()
    final_output = replace_chunk(index_contents, "day_marker", string_today)
    index_page.open("w").write(final_output)
