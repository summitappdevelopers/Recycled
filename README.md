Recycled
========

A webapp to encourage school recycling.

[Summit Recycled App](http://www.recycled-app.appspot.com)

##How it Works##

QR codes encoded with the URL endpoint of `/point?special=somekey` are attached to recycling bins. Students scan the QR codes with their smartphones and are are redirected to the special endpoint. Currently, the only way to verify that the student came from the QR code is by verifying a URL variable that's an awkward MD5 hash. This variable only comes from the link encoded by the QR. After verification and authentication, the program updates the property `Player.points` and `Player.updateTime` in the Google Datastore. Every time a user tries to scan a code, the program checks if an hour has passed between scans by comparing the current time and the `Player.updateTime` property, before proceeding to update the Datastore. Additionally, there are `cron` jobs that wipe the Datastore every month to restart the game.

##Use Recycled in Your Own School##

Recycled was built using the `webapp2` Python framework documented by Google [here](https://developers.google.com/appengine/docs/python/gettingstartedpython27/introduction). The Views are created with [Jinja2](http://jinja.pocoo.org/docs/).

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
    
* Deploy and make Recycled your own!


##MIT License##
Copyright © 2014 Ajay Ramesh

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


