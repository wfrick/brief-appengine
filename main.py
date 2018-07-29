#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from google.appengine.ext import ndb
import os
import jinja2
from keys import bing_key, agolo_key
from api import bing, agolo
from utilities import agolo_to_object
from model import Search, Article
import time
from google.appengine.api import taskqueue
import jinja2
from sources import *

#Set template directory
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
#Set up jinja environment
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)



#Set template directory
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
#Set up jinja environment
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
    	#Render search page
    	template = jinja_env.get_template('jumbotron_narrow_search.html')
    	self.response.write(template.render())

    def post(self):
        #Get search term and sites from webform plus request ID
    	term = str(self.request.get('term'))
        sites = str(self.request.get('sites'))
        request_id = os.environ.get('REQUEST_LOG_ID')
        thinktanks = str(self.request.get('thinktanks'))
        media = str(self.request.get('media'))
        univ_other = str(self.request.get('univ_other'))
        explainers = str(self.request.get('explainers'))

        if not sites:
            sites = ''

        #If checkboxes are checked, add sources to 'sites' list
        if thinktanks and len(sites) > 0:
            sites = sites + "," + sources_thinktanks
        elif thinktanks:
            sites = sites + sources_thinktanks

        if media and len(sites) > 0:
            sites = sites + "," + sources_topmedia
        elif media:
            sites = sites + sources_topmedia

        if univ_other and len(sites) > 0:
            sites = sites + "," + sources_univ_other
        elif univ_other:
            sites = sites + sources_univ_other

        if explainers and len(sites) > 0:
            sites = sites + "," + sources_explainers
        elif explainers:
            sites = sites + sources_explainers

        #Save search info in db
        search = Search(request_id=request_id,search_term=term,sites=sites)
        s = search.put()
        s = s.get()
        search_id = str(s.key.id())

        #Pass search info to BackgroundHandler
        task = taskqueue.add(url='/background',
            params={'search_id': search_id,'sites':sites,
            'term':term})

        #Send user to waiting page while background task is completed
        results_path = "results/" + search_id
        template_variables = {'term' : term, 'path' : results_path }
        template = jinja_env.get_template('jumbotron_narrow_waiting.html')
        self.response.write(template.render(template_variables))
        

class BackgroundHandler(webapp2.RequestHandler):
    def post(self):
        #Get and format search info from MainHandler
        term = str(self.request.get('term'))
        sites = str(self.request.get('sites'))
        sites = sites.split(',')
        search_id = str(self.request.get('search_id'))

        #Set number of search results to retrieve from Bing
    	number_of_results = 30

        #Search Bing for URLs
        urls = bing(bing_key,term,number_of_results,0,news=False,sites=sites)

        #Summarize each URL with Agolo and save results to database
        for url in urls:
            summary = agolo(agolo_key,5,url)
            result = agolo_to_object(summary,search_id,url)
            if result != "Error":
                result.put()
        

class Results(webapp2.RequestHandler):
    def get(self, path):
        query = Article.query(Article.search_id == str(path))
        template_variables = {'results' : query}
        template = jinja_env.get_template('jumbotron_narrow_results.html')
        self.response.write(template.render(template_variables))

app = webapp2.WSGIApplication([
    ('/', MainHandler),('/background', BackgroundHandler),
    ('/results/([0-9a-zA-Z_\-]+)',Results)
], debug=True)