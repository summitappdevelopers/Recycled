Recycled
========

A webapp to encourage school recycling.

[Summit Recycled App](http://www.recycled-app.appspot.com)

Special thanks to Summit student Alexander Nguyen and [The City of San Jose](http://www.sanjoseca.gov/index.aspx?NID=1525) for bringing recycling to our campus, free of cost.

##How it Works##

QR codes encoded with the URL endpoint of `/point?special=somekey` are attached to recycling bins. Students scan the QR codes with their smartphones and are are redirected to the special endpoint. Currently, the only way to verify that the student came from the QR code is by verifying a URL variable that's an awkward MD5 hash. This variable only comes from the link encoded by the QR. After verification and authentication, the program updates the property `Player.points` and `Player.updateTime` in the Google Datastore. Every time a user tries to scan a code, the program checks if an hour has passed between scans by comparing the current time and the `Player.updateTime` property, before proceeding to update the Datastore. Additionally, there are `cron` jobs that wipe the Datastore every month to restart the game.

##Use Recycled in Your Own School##

Recycled was built using the [webapp2](http://webapp-improved.appspot.com/) Python framework [documented](https://developers.google.com/appengine/docs/python/gettingstartedpython27/introduction) by Google. The views are created with [Jinja2](http://jinja.pocoo.org/docs/) and styled with [Bootstrap3](http://getbootstrap.com/)

* Download the [Google App Engine SDK for Python](https://developers.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python), which comes with a handy deployment and debug tool, as well as all the necessary libraries.

* Register the application for your own school by creating an [AppEngine](https://appengine.google.com/) account. Make sure you pick a unique name.

* Edit the `app.yaml` file to reflect your app's name by changing the `application:` field.

```YAML
application: recycled-app
version: 1
runtime: python27
api_version: 1
threadsafe: true
```

* Edit the `recycled-app.py` file with your own hash. Replace the `SPECIAL_KEY = 'yourhash'` with your own authorization string. This is just a minimal measure to check if a user came from a QR code.

* Deploy, fork, and make Recycled your own!

###Creating the QR Code###

Create a QR code linking to your `/point` URL. You can use a site like [QRStuff](http://www.qrstuff.com/) to do this. Format the link like so:

`http://www.url-to-my-site.appspot.com/point?special=yourhash`

`yourhash` should be replaced by whatever hash you assigned `SPECIAL_KEY` in `recylced-app.py`


##MIT License##
Copyright © 2014 Ajay Ramesh

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


