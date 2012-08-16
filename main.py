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
from google.appengine.api import users

class MainHandler(webapp2.RequestHandler):
	def get(self):
		file="static/listing.html"
		listing=open(file).read()
		self.response.out.write(listing)

class postit(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			file="static/postit.html"
			posting=open(file).read()
			self.response.out.write(posting)
		else:
			self.redirect(users.create_login_url(self.request.uri))
			
app = webapp2.WSGIApplication(
	[
	('/', MainHandler),
	('/postit',postit)
	],debug=True)

def main():
	app.run(app)
	

if __name__ == '__main__':
	main()
