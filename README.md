#Brief for AppEngine

This is a web application built for Google App Engine using webapp2. Its purpose is to help readers quickly research complex topics.
It allows users to search for something and get back summaries of the results from a set list of credible sources.

##Requirements
Google App Engine
webapp2
jinja2
httplib
urllib
base64
json

##Required API keys
Add a file keys.py in the main directory. It should include:

bing_key = 'YOUR_SECRET_KEY'
agolo_key = 'YOUR_SECRET_KEY'

Be aware that API restrictions may limit usage, or require tweaks to the code to limit how many items you pull from Agolo at a time.