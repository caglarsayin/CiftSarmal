#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#	 http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# -*- coding: utf-8 -*-

import webapp2
import datetime
import jinja2
import os
import urllib

from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import users

jinja_environment = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class Article(db.Model):
	title = db.StringProperty(required=True,indexed=False)
	text = db.TextProperty(required=True,indexed=False)
	imgKey = blobstore.BlobReferenceProperty(required=True,indexed=False)
	additionDate = db.DateProperty(required=True,indexed=True)
	summary = db.TextProperty(required=True,indexed=False)
	editor = db.UserProperty(required=True,indexed=True)
	tags = db.StringListProperty(indexed=True)
	categ = db.StringProperty(choices=['dbilimleri', 'teknoloji', 'psikoloji', 'ekonomi','saglik','ekoloji','tbilimleri'],required=True,indexed=True )
	count = db.IntegerProperty(indexed=False)
	orjinalLink = db.LinkProperty(indexed=False)
	relatedLinks = db.ListProperty(db.Link,indexed=False)
	videoLings = db.ListProperty(db.Link,indexed=False)


class MainHandler(webapp2.RequestHandler):
	def get(self):
		filed="static/listing.html"
		listing=open(filed).read()
		self.response.out.write(listing)

class jinja(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('static/listing_jinja.html')
		articles = Article.all()
		self.response.out.write(template.render({'articles': articles}))

class postIt(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			postpage = blobstore.create_upload_url('/posting')
			template = jinja_environment.get_template('static/postit.html')
			self.response.out.write(template.render({'postpage':postpage}))
		else:
			self.redirect(users.create_login_url(self.request.uri))

class posting(blobstore_handlers.BlobstoreUploadHandler):
	def post(self):
		postedimg = self.get_uploads('img')  # 'file' is file upload field in the form
		postedaudio = self.get_uploads('audio')
		imgBlob = postedimg[0]
		audioBlob = postedaudio[0]
		dataModel = Article(title = unicode(self.request.get('baslik')),
						text = db.Text(self.request.get('editor')),
						orjinalLink = db.Link(self.request.get('link')),
						tags = [self.request.get('tags'),],
						rlinks = self.request.get('rlinks'),
						categ = self.request.get('cate'),
						summary = self.request.get('summary'),
						imgKey = imgBlob.key(),
						additionDate = datetime.datetime.now().date(),
						editor = users.get_current_user()
						)
		dataModel.put()

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
	def get(self, resource):
		"""
		Blob store middle_ware
		"""
		resource = str(urllib.unquote(resource))
		blob_info = blobstore.BlobInfo.get(resource)
		self.send_blob(blob_info)


app = webapp2.WSGIApplication(
	[
	('/orjinal', MainHandler),
	('/', jinja),
	('/posting', posting),
	('/postit',postIt),
	('/serve/([^/]+)?', ServeHandler)
	],debug=True)

def main():
	app.run(app)


if __name__ == '__main__':
	main()
