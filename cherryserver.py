#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import webbrowser
from threading import Timer


os.environ["DJANGO_SETTINGS_MODULE"] = "economia_rio.settings"

import django
django.setup()

import cherrypy
from django.conf import settings
from django.core.handlers.wsgi import WSGIHandler

# HOST = "192.168.201.35"
HOST = '0.0.0.0'
# HOST = "127.0.0.1"
PORT = 5000


class DjangoApplication(object):
    def mount_static(self, url, root):
        """
        :param url: Relative url
        :param root: Path to static files root
        """
        config = {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': root,
            'tools.expires.on': True,
            'tools.expires.secs': 86400
        }
        cherrypy.tree.mount(None, url, {'/': config})

    def open_browser(self):
        Timer(3, webbrowser.open,
             ("http://%s:%s" % ('localhost', PORT),)).start()

    def run(self):
        cherrypy.config.update({
            'server.socket_host': HOST,
            'server.socket_port': PORT,
            'engine.autoreload_on': False,
            'log.screen': True
        })
        self.mount_static(settings.STATIC_URL, settings.STATIC_ROOT)

        cherrypy.log("Loading and serving Django application")
        cherrypy.tree.graft(WSGIHandler())
        cherrypy.engine.start()

        webbrowser.open('http://{}:{}'.format(HOST, PORT))

        cherrypy.engine.block()


if __name__ == "__main__":
    print("Your app is running at http://{}:{}".format(HOST, PORT))
    DjangoApplication().run()
