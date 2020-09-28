import os
import re
import pathlib
import json
import requests
from datetime import date

# setup
root = pathlib.Path(__file__).parent.parent.resolve()
location = os.getenv('city_code')+','+os.getenv('country_code')
APIKEY = os.getenv('open_weather_key')
url = "http://api.openweathermap.org/data/2.5/find?q=%s&units=metric&APPID=%s" %(location,APIKEY)
# headers = {"Authorization":"Bearer %s"%key}

response = requests.get(url)
response_dict = json.loads(response.text)
output_date = date.today()
my_loc = response_dict['list'][0]
today_weather = str(my_loc['main']['temp'])
high_temp = str(my_loc['main']['temp_max'])
low_temp = str(my_loc['main']['temp_min'])
rain = str(my_loc['rain'])
today_desc = str(my_loc['weather'][0]['description'])

if(rain == "None"):
    rain = "0"

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
