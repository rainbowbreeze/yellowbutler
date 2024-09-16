# YELLOWBOT GAE AND PYTHON SPECIFIC CONFIGURATIONS


### Testing

#### Run Unit tests
Resources:
- Using PyTest: https://docs.pytest.org/en/latest/
- http://pytest.readthedocs.io/en/latest/goodpractices.html
- why using self.assertXXXX vs assert: https://stackoverflow.com/a/45947566

from bot/src folder
```
pip install -r requirements-dev.txt
pytest
```

Unfortunately, PyTest fixtures feature do not work when pytest is used in unittest.TestCase subclasses, apart from Auto-use fixtures. [Source](https://docs.pytest.org/en/stable/unittest.html#pytest-features-in-unittest-testcase-subclasses)

Fixtures:
- [Pytext fixtures](https://docs.pytest.org/en/stable/fixture.html#fixture-function)
- [Responses as pytest fixture](https://github.com/getsentry/responses#responses-as-a-pytest-fixture)
- [UnitTest and fixtures](https://docs.pytest.org/en/stable/unittest.html#mixing-pytest-fixtures-into-unittest-testcase-subclasses-using-marks)



#### Mock requests call
[Responses](https://github.com/getsentry/responses) seems a good library to mock Requests calls.



### Manage configurations
https://martin-thoma.com/configuration-files-in-python/
https://hackernoon.com/4-ways-to-manage-the-configuration-in-python-4623049e841b

I put in the configuration class logic to obtain the file both via a relative path (relative to the root folder when the python is lauched), and also looking inside of the folder where the specific class is, as fallback. This is particuarly useful with tests, so I can pass different configuration files while running tests.



### Flask
```
pip install flask
```
Add flask to requirements.txt

To put all Flask logic in a specific place, separated from the main app logic, create a folder wsgi, as source folder.
Then, create app.py under wsgi folder
```
#!flask/bin/python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"


if __name__ == '__main__':
    app.run(debug=True)
```

and run the app with
```
FLASK_APP=wsgi/flaskapp.py flask run
```



## App Engine notes


### GAE and data storing
https://cloud.google.com/datastore/docs/reference/libraries#client-libraries-install-python



### Testing

#### GAE and Unit Testing
Reference links
- [Local Unit Testing for Python 2](https://cloud.google.com/appengine/docs/standard/python/tools/localunittesting)- For python 2.x, and testbed is not supported on python 3.x runtime [post](https://groups.google.com/g/google-appengine/c/yuAofPuxYtE/m/z4rRIggECgAJ)
- [Concepts, use and testing Cloud Datastore in local](https://groups.google.com/g/google-appengine/c/cBXfhk3HfRI)
- [Datastore emulator for unit testing](https://groups.google.com/g/google-appengine/c/yuAofPuxYtE/m/KQYeFUcBCgAJ), with a link to a repo with unit test examples

To emulate the Datastore, it's necessary to launch the GAE project using the local app server, dev_appserver.py, configured to provide [Datastore emulation](https://cloud.google.com/datastore/docs/tools/datastore-emulator)
```
dev_appserver.py --application=%YOUR_APPLICATION_ID --support_datastore_emulator=true --dev_appserver_log_level=debug app.yaml
```


#### Running the local development server, also for testing purposes
The GAE [local development server](https://cloud.google.com/appengine/docs/standard/python3/testing-and-deploying-your-app#local-dev-server) can be used to run this project, emaulating an application running in production, and potentially also emulate services like Cloud Datastore, Cloud Bigtable and Cloud Pub/Sub locally.
To run the local development server, _from bot/src_
```
dev_appserver.py --application=%PROJECT_ID% app.yaml
```

GAE_ENV environmental var distinguishes between local development server and real GAE environment
```
import os
print(os.getenv('GAE_ENV', ''))
```
- 'localdev' when the local development server is used
- '' when launched with python and with gunicorn
- 'standard' when in production

[Advanced commands](https://cloud.google.com/appengine/docs/standard/python3/tools/local-devserver-command) for the local development server.
[Old reference](https://cloud.google.com/appengine/docs/standard/python/tools/using-local-server) for python 2.x, but still has good example that work with python 3.



### Local Datastore emulator
The local development server launches also the datastore emulator. To check local datastore content: http://localhost:8000/datastore (there is also the scheduler, task manager, etc)

To clear the local datastore for an application: dev_appserver.py --clear_datastore=yes app.yaml



### Scheduler
Create a cron.yaml following
https://cloud.google.com/appengine/docs/flexible/python/scheduling-jobs-with-cron-yaml
or
https://cloud.google.com/appengine/docs/standard/python/config/cron

To deploy new tasks, without redeploying the whole app:
```
gcloud app deploy cron.yaml --verbosity debug --quiet
```
Check for log on Cloud console: https://console.cloud.google.com/appengine/taskqueues/cron


### Flask and App Engine local runtime
Changed app.yaml adding the right module name, using dotted notation
```
entrypoint: gunicorn -b :$PORT wsgi.flaskapp:app
```

Added gunicorn to requirements.txt, so App Engine can be launched locally



## YouTube notes

Resouces:
- [YouTube Developers Live: Getting a Channel's Uploads in v3](https://www.youtube.com/watch?v=RjUlmco7v2M)
- [YouTube API to fetch all videos on a channel](https://stackoverflow.com/questions/18953499/youtube-api-to-fetch-all-videos-on-a-channel) - one of the last [replies](https://stackoverflow.com/a/36387404) is the best one, as the solution consumes only 2 quota token, and not 100 as a normal search

[Official reference doc](https://developers.google.com/youtube/v3/docs/channels/list) to get the "upload" playlist from the channel:
```
curl 'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&id=UCSbdMXOI_3HGiFviLZO6kNA&key=[YOUR_API_KEY]' --header 'Accept: application/json' --compressed
```
Result:
```
{
  "kind": "youtube#channelListResponse",
  "etag": "nhLskkHElB2KEuMHsB1MCvcS39M",
  "pageInfo": {
    "totalResults": 1,
    "resultsPerPage": 5
  },
  "items": [
    {
      "kind": "youtube#channel",
      "etag": "_4gfGDJgf5GGfG3wN_Vo-ANkiyE",
      "id": "UCSbdMXOI_3HGiFviLZO6kNA",
      "contentDetails": {
        "relatedPlaylists": {
          "likes": "",
          "favorites": "",
          "uploads": "UUSbdMXOI_3HGiFviLZO6kNA"
        }
      }
    }
  ]
}
```

[Official reference doc](https://developers.google.com/youtube/v3/docs/playlistItems/list) to get the items of a playlist:
```
curl 'https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=20&playlistId=UUSbdMXOI_3HGiFviLZO6kNA&key=[YOUR_API_KEY]' --header 'Accept: application/json' --compressed
```
Result:
```
{
  "kind": "youtube#playlistItemListResponse",
  "etag": "7NNslmCQmNZ4HyiQCWOoH2uPwlk",
  "nextPageToken": "CAIQAA",
  "items": [
    {
      "kind": "youtube#playlistItem",
      "etag": "AbWaqKJEbkfBpDbUqSkbvM2whno",
      "id": "VVVTYmRNWE9JXzNIR2lGdmlMWk82a05BLnZlVngwQXVoSEZ3",
      "snippet": {
        "publishedAt": "2021-01-27T20:00:10Z",
        "channelId": "UCSbdMXOI_3HGiFviLZO6kNA",
        "title": "Valve's next VR projects are SCARILY similar to Sword Art Online",
        "description": "Hello and welcome to Tuesday Newsday! Your number one resource for the entire weeks worth of VR news. Today is actually a CRAZY week for VR news. Between Valve announcing a partnership with a BCI company, new haptic gloves, Quest 2 news, and Doom Eternal maybe coming to VR... I hope you enjoy! \n\n\nMy links-\nTwitch Stream TODAY!\nhttps://www.twitch.tv/thrilluwu\nJoin my discord for good times\nhttps://discord.gg/thrill\nPatreon link:Join\nhttps://www.patreon.com/Thrillseeker\nGAMERSUPPS Discount Code: THRILL\nhttp://gamersupps.gg/?afmc=thrill\n\n\nSources-\nhttps://www.roadtovr.com/bethesda-vr-pc-2021-project/\nhttps://www.classification.gov.au/titles/project-2021a\nhttps://www.roadtovr.com/valve-openbci-immersive-vr-games/\nhttps://www.roadtovr.com/gabe-newell-brain-computer-interfaces-way-closer-matrix-people-realize/\nhttps://www.tvnz.co.nz/one-news/new-zealand/gabe-newell-says-brain-computer-interface-tech-allow-video-games-far-beyond-human-meat-peripherals-can-comprehend\nhttps://www.roadtovr.com/bethesda-vr-pc-2021-project/\nhttps://vrscout.com/news/haptx-true-contact-haptic-gloves-vr/\nhttps://vrscout.com/news/haptx-true-contact-haptic-gloves-vr/\nhttps://haptx.com/virtual-reality/",
        "thumbnails": {
          "default": {
            "url": "https://i.ytimg.com/vi/veVx0AuhHFw/default.jpg",
            "width": 120,
            "height": 90
          },
          "medium": {
            "url": "https://i.ytimg.com/vi/veVx0AuhHFw/mqdefault.jpg",
            "width": 320,
            "height": 180
          },
          "high": {
            "url": "https://i.ytimg.com/vi/veVx0AuhHFw/hqdefault.jpg",
            "width": 480,
            "height": 360
          },
          "standard": {
            "url": "https://i.ytimg.com/vi/veVx0AuhHFw/sddefault.jpg",
            "width": 640,
            "height": 480
          },
          "maxres": {
            "url": "https://i.ytimg.com/vi/veVx0AuhHFw/maxresdefault.jpg",
            "width": 1280,
            "height": 720
          }
        },
        "channelTitle": "ThrillSeeker",
        "playlistId": "UUSbdMXOI_3HGiFviLZO6kNA",
        "position": 0,
        "resourceId": {
          "kind": "youtube#video",
          "videoId": "veVx0AuhHFw"
        }
      }
    },
    {
      "kind": "youtube#playlistItem",
      "etag": "3DUxmtnDvgj2vJdH_stgWRzY4hQ",
      "id": "VVVTYmRNWE9JXzNIR2lGdmlMWk82a05BLmxJTGxXTUxUbjBj",
      "snippet": {
        "publishedAt": "2021-01-23T19:15:01Z",
        "channelId": "UCSbdMXOI_3HGiFviLZO6kNA",
        "title": "What Happened to my Valve Index After 2000 Hours?",
        "description": "Hello! Here is an updated video as promised of my Valve index after 2000 hours and about a year and a half of usage. I have been through a lot and I have learned a lot about the index and how to make it last a long time, so buckle up and enjoy!\n\nBTW, im super sorry, this this video took me way longer to do than normal, Im using multiple different camera setups with different lighting etc, definitely is not my best video ever, but It will get better. Thank you!\n\nMy links-\nTwitch Stream TODAY!\nhttps://www.twitch.tv/thrilluwu\nJoin my discord for good times\nhttps://discord.gg/thrill\nPatreon link:Join\nhttps://www.patreon.com/Thrillseeker\nGAMERSUPPS Discount Code: THRILL\nhttp://gamersupps.gg/?afmc=thrill\n\nMusic- Protostar Overdrive",
        "thumbnails": {
          "default": {
            "url": "https://i.ytimg.com/vi/lILlWMLTn0c/default.jpg",
            "width": 120,
            "height": 90
          },
          "medium": {
            "url": "https://i.ytimg.com/vi/lILlWMLTn0c/mqdefault.jpg",
            "width": 320,
            "height": 180
          },
          "high": {
            "url": "https://i.ytimg.com/vi/lILlWMLTn0c/hqdefault.jpg",
            "width": 480,
            "height": 360
          },
          "standard": {
            "url": "https://i.ytimg.com/vi/lILlWMLTn0c/sddefault.jpg",
            "width": 640,
            "height": 480
          },
          "maxres": {
            "url": "https://i.ytimg.com/vi/lILlWMLTn0c/maxresdefault.jpg",
            "width": 1280,
            "height": 720
          }
        },
        "channelTitle": "ThrillSeeker",
        "playlistId": "UUSbdMXOI_3HGiFviLZO6kNA",
        "position": 1,
        "resourceId": {
          "kind": "youtube#video",
          "videoId": "lILlWMLTn0c"
        }
      }
    }
  ],
  "pageInfo": {
    "totalResults": 157,
    "resultsPerPage": 2
  }
}
```
