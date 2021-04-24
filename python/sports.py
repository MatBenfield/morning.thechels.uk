
 # importing modules
import os
import helper
import pathlib
import requests
import json
from datetime import date


# setup
fixtures = set()
pre_content = ""
date = date.today()
today_date_string = helper.dtStylish(date.today(), '%A-{th}-%B')
root = pathlib.Path(__file__).parent.parent.resolve()
url = f"https://push.api.bbci.co.uk/data/bbc-morph-football-scores-match-list-data/endDate/{date}/startDate/{date}/todayDate/{date}/tournament/full-priority-order/version/2.4.6?timeout=5"
response_dict = json.loads(requests.get(url).text)
print(url)
with open( root / "config/tournaments.json", 'r') as filehandle:
  tournament_slug = json.load(filehandle)

for md_events in list(response_dict['matchData']):
    for tournaments in (t_item for t_item in md_events if md_events['tournamentMeta']['tournamentSlug'] in tournament_slug):
        for events in md_events['tournamentDatesWithEvents'][today_date_string]:
            for games in events['events']:
                home_name = games['homeTeam']['name']['first']
                away_name = games['awayTeam']['name']['first']
                kick_off = games['startTimeInUKHHMM']
                record = f"<li>({kick_off}) {home_name} - {away_name}</li>\n"
                if(record not in fixtures):
                    fixtures.add(record)

if not fixtures:
    fixtures.add("<li>No fixtures today</li>")

for fixture in sorted(fixtures):
    pre_content += fixture

# processing
if __name__ == "__main__":
    all_news = "<h2>Fixtures</h2>\n"
    index_page = root / "index.html"
    index_contents = index_page.open().read()
    final_output = helper.replace_chunk(index_contents, "fixtures_marker", f"<ul>\n{pre_content}</ul>")
    index_page.open("w").write(final_output)
