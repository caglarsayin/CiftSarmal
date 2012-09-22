# -*- coding: utf-8 -*-
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
from string import replace
from google.appengine.api import images
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

class Subscribers(db.Model):
    email = db.EmailProperty(required=True)
    subscribtion_date = db.DateProperty(auto_now_add=True)

class Article(db.Model):
    title = db.StringProperty(required=True,indexed=False)
    text = db.TextProperty(required=True,indexed=False)
    imgKey = blobstore.BlobReferenceProperty(required=True,indexed=False)
    audioKey = blobstore.BlobReferenceProperty(required=False,indexed=False)
    additionDate = db.DateTimeProperty(auto_now_add=True,indexed=True)
    summary = db.TextProperty(required=True,indexed=False)
    editor = db.UserProperty(required=True,indexed=True)
    tags = db.StringListProperty(indexed=True)
    categ = db.StringProperty(choices=['dbilimleri', 'teknoloji', 'psikoloji', 'ekonomi','saglik','ekoloji','tbilimleri'],required=True,indexed=True )
    count = db.IntegerProperty(indexed=False)
    orjinalLink = db.LinkProperty(indexed=False)
    relatedLinks = db.ListProperty(db.Link,indexed=False)
    videoLings = db.ListProperty(db.Link,indexed=False)
    urlAdress = db.StringProperty(indexed=True)

class Subscribe(webapp2.RequestHandler):
    def get(self):
        mail=self.request.get("email")
        newSubsriber = Subscribers(email=mail)

        newSubsriber.put()
        self.response.out.write("Tesekkur Ederiz.")


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.redirect("list/all/1")

class listing(webapp2.RequestHandler):
    def get(self,page,cat,pageno):
        if pageno:
            pageno=int(pageno)
        else:
            pageno=1
        if cat=="all":
            q = db.GqlQuery("SELECT * FROM Article ORDER BY additionDate DESC")
        else:
            q = db.GqlQuery("SELECT * FROM Article where categ = :1 ORDER BY additionDate DESC",cat)

        template = jinja_environment.get_template('static/listing_jinja.html')
        articles=q.fetch(10,offset=pageno*10-10)
        self.response.out.write(template.render({'articles': articles,'pageno':pageno}))

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
        try:
            postedimg = self.get_uploads('img')  # 'file' is file upload field in the form
            imgBlob = postedimg[0]
            dataModel = Article(title = self.request.get('baslik'),
                            text = db.Text(self.request.get('editor')),
                            orjinalLink = db.Link(self.request.get('link')),
                            tags = [self.request.get('tags'),],
                            rlinks = self.request.get('rlinks'),
                            categ = self.request.get('cate'),
                            summary = self.request.get('summary'),
                            imgKey = imgBlob.key(),
                            editor = users.get_current_user(),
                            urlAdress = self.normalizeIt(self.request.get('baslik')))
            if self.get_uploads("audio"):
                postedaudio = self.get_uploads('audio')
                dataModel.audioKey = postedaudio[0]
            dataModel.put()
        except:
            raise
#            self.redirect("/postit")

    def normalizeIt(self,s):
        valid_chars='-_ abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        reps = {'ç':'c', 'ş':'s', 'ü':'u', 'ğ':'g', 'ı':'i', 'ö':'o','Ç':'C', 'Ş':'S', 'Ü':'U', 'Ğ':'G', 'İ':'I', 'Ö':'O', ' ':'-'}
        s=s.encode("utf8")
        for i, j in reps.iteritems():
            s = s.replace(i, j)
        for i in s:
            if not i in valid_chars:
                s=s.replace(i,"")
        return s


class article(webapp2.RequestHandler):
    def get(self,slub):
        template = jinja_environment.get_template('static/page.html')
        q = db.GqlQuery("SELECT * FROM Article  where urlAdress= :1",slub)
        article = q.fetch(1)[0]
        self.response.out.write(template.render({'article': article}))


class ServeHandler(webapp2.RequestHandler):
    def get(self,blob_key,ext):
        if blob_key:
            blob_info = blobstore.get(blob_key)
            if blob_info:
                img = images.Image(blob_key=blob_key)
                img.resize(width=144, height=81)
                img.im_feeling_lucky()
                thumbnail = img.execute_transforms(output_encoding=images.JPEG)

                self.response.headers['Content-Type'] = 'image/jpeg'
                self.response.out.write(thumbnail)
                return

        # Either "blob_key" wasn't provided, or there was no value with that ID
        # in the Blobstore.
        self.error(404)

class mp3Handler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, audioKey,name,ext):
        if not blobstore.get(audioKey):
            self.error(404)
        else:
            self.send_blob(audioKey)


class debugg(webapp2.RequestHandler):
    def get(self):
        q = db.GqlQuery("SELECT * FROM Article " +"WHERE urlAdress = :1","""Testing---caglar---csi""")
        q=q.fetch(1)
        for i in  q:
            self.response.out.write(i.additionDate)

    def get_old(self):
        s=u"çaş ş'ğ'aü"
        s=self.normalizeIt(s)
        test=self.uri_for('article', _full=True,slub=s)
        self.response.out.write(test)

    def normalizeIt(self,s):
        valid_chars='-_ abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        reps = {'ç':'c', 'ş':'s', 'ü':'u', 'ğ':'g', 'ı':'i', 'ö':'o','Ç':'C', 'Ş':'S', 'Ü':'U', 'Ğ':'G', 'İ':'I', 'Ö':'O', ' ':'_'}
        s=s.encode("utf8")
        self.response.out.write(type(s))
        for i, j in reps.iteritems():
            s = s.replace(i, j)
        s="".join([i for i in s if i in valid_chars])
        return s

class hakkimizda(webapp2.RequestHandler):
    def get(self):
        file="static/about/hakkimizda.html"
        listing=open(file).read().decode('utf8')
        template = jinja_environment.get_template('static/about.html')
        self.response.out.write(template.render({'article': listing}))

class calisin(webapp2.RequestHandler):
    def get(self):
        file="static/about/calisin.html"
        listing=open(file).read().decode('utf8')
        template = jinja_environment.get_template('static/about.html')
        self.response.out.write(template.render({'article': listing}))

class kosullar(webapp2.RequestHandler):
    def get(self):
        file="static/about/kosullar.html"
        listing=open(file).read().decode('utf8')
        template = jinja_environment.get_template('static/about.html')
        self.response.out.write(template.render({'article': listing}))

class gizlilik(webapp2.RequestHandler):
    def get(self):
        file="static/about/gizlilik.html"
        listing=open(file).read().decode('utf8')
        template = jinja_environment.get_template('static/about.html')
        self.response.out.write(template.render({'article': listing}))

class iletisim(webapp2.RequestHandler):
    def get(self):
        file="static/about/iletisim.html"
        listing=open(file).read().decode('utf8')
        template = jinja_environment.get_template('static/about.html')
        self.response.out.write(template.render({'article': listing}))




app = webapp2.WSGIApplication(
    [
    ('/', MainHandler),
    ('/list(/([a-z]*)/([0-9]*))', listing),
    ('/posting', posting),
    ('/postit',postIt),
    ('/hakkimizda/',hakkimizda),
    ('/careers/',calisin),
    ('/privacy/',gizlilik),
    ('/conditions/',kosullar),
    ('/contact/',iletisim),
    ('/serve/([^/]+)?(.jpg)$', ServeHandler),
    ('/mp3/([^/]+)?(/).*(.mp3)$', mp3Handler),
    ('/subscribe', Subscribe),
    webapp2.Route('/article/<slub:([^/]+)?>', article,'article'),
    webapp2.Route('/debug', debugg,"debugg")
    ],debug=True)

def main():
    app.run(app)


if __name__ == '__main__':
    main()
