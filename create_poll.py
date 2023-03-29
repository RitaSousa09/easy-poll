import locale
from decouple import config
from get_poll_options import set_personalized_poll
import json
import requests

LOCALE = 'pt_PT'
STRAWPOLL_ENDPOINT = "https://api.strawpoll.com/v3"
API_KEY = config('STRAWPOLL_API_KEY', default='')

try:
    locale.setlocale(locale.LC_ALL, LOCALE)
except Exception as e:
    print("FAILED to set ${LOCALE} locale")
    print(e)
    exit(1)

poll_template_string = ""
with open("templates/poll-template.json") as f:
	poll_template_string = f.read()
poll_template = json.loads(poll_template_string)

desired_poll = set_personalized_poll(poll_template)

response = requests.post(STRAWPOLL_ENDPOINT + '/polls', json = desired_poll, headers = { 'X-API-KEY': API_KEY })

if response:
	poll = response.json()
	print("Here's your poll:")
	print(poll["url"])
else:
	error = response.json()
	print(error)
