import json
import requests

def get_all_channels():
    channels = requests.get('http://hackathon.lab.watchmi.tv/api/example.com/channels'
                            ).json()['results']

    processed = {}

    for channel in channels:
        channel_name = channel['DName']['Long']['value']
        processed[channel_name] = channel['id']

    return json.dumps(sorted(processed))

