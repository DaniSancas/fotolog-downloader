#!/usr/bin/python
# coding=utf-8
"""Python crawler for Fotolog backups."""

import urllib2
from os import path
from sys import argv
from urlparse import urlparse
from bs4 import BeautifulSoup
from threading import Thread

__author__ = 'dani sancas'


class MosaicCrawler:

    def __init__(self, mosaicurl, savepath, offset=None):
        self.basemosaicurl = mosaicurl
        self.savepath = savepath
        parsed_uri = urlparse(self.basemosaicurl)
        self.domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        self.photocount = int(self.setup())  # Inicialization
        self.offset = int(offset) if offset is not None else None

    def urlopener(self, urladdr, referer=None):
        # Create request with headers
        opener = urllib2.build_opener()
        if referer is None:
            referer = self.basemosaicurl
        opener.addheaders = [
                    ('User-agent', 'Mozilla/6.0'),
                    ('Accept', 'application/json, text/javascript, */*; q=0.01'),
                    ('X-Requested-With', 'XMLHttpRequest'),
                    ('Referer', referer),
                    ('Host', 'www.fotolog.com'),
                    ('Content-Type', 'application/json; charset=UTF-8')]
        return opener.open(urladdr)

    def setup(self):
        if not path.isdir(self.savepath):
            print("Directory doesn't exist or hasn't access permission: {}".format(self.savepath))
            exit(1)
        # Finds out how many photos are
        mosaic = self.urlopener(self.basemosaicurl)
        bs = BeautifulSoup(mosaic, "html5lib")
        return bs.find("ul", attrs={"id": "profile_bar"}).find("li").find("a").find("b").string

    def crawl(self):
        # Crawls the 'mosaics', starting from offset
        offset = self.offset
        if not offset:
            # If not set, it's the first one (without number)
            self.crawlmosaic(self.basemosaicurl)
            offset = 30

        # Continue with the other mosaics
        for page in range(offset, self.photocount, 30):
            self.crawlmosaic("{}{}".format(self.basemosaicurl, page))  # It adds 30, 60, etc. to  ".../mosaic/"

    def crawlmosaic(self, mosaicurl):
        print("Entering page {}".format(mosaicurl))
        mosaic = self.urlopener(mosaicurl)
        bs = BeautifulSoup(mosaic, "html5lib")
        htmlmosaic = bs.find("ul", attrs={"id": "list_photos_mosaic"})
        try:
            # Some mosaics could be wrong and don't show links
            mosaiclinks = htmlmosaic.find_all("a")
        except AttributeError:
            print("Inaccesible mosaic {}".format(mosaicurl))
        else:
            # Inside every mosaic there are links (posts), access all at same time
            hilos = []
            for link in mosaiclinks:
                hilo = Thread(target=self.crawlpost, args=(link["href"],))
                hilo.daemon = True
                hilos.append(hilo)

            # Init threads
            for hilo in hilos:
                hilo.start()

            # Max wait of 30secs
            for hilo in hilos:
                hilo.join(30)

    def crawlpost(self, urladdr):
        try:
            # Some links could be broken
            post = self.urlopener(urladdr)
        except (urllib2.HTTPError, urllib2.URLError):
            print("Broken link {}".format(urladdr))
        else:
            bs = BeautifulSoup(post, "html5lib")
            htmlpost = bs.find("div", attrs={"id": "flog_img_holder"})
            htmllink = htmlpost.find("a")
            image = htmllink.find("img")
            full_image_link = image["src"]
            file_name_split = full_image_link.split("/")
            filename = file_name_split[-1]  # Pick just "file.jpg"

            try:
                downloadedfile = self.urlopener(full_image_link, urladdr)
            except (urllib2.HTTPError, urllib2.URLError):
                print("Foto {} no encontrada".format(full_image_link))
            else:
                # Save the photo!
                f = open('{}{}'.format(self.savepath, filename), 'w+')
                f.write(downloadedfile.read())
                f.close()


if __name__ == "__main__":
    url = "http://www.fotolog.com/{}/mosaic/".format(argv[1])
    mc = MosaicCrawler(url, argv[2], argv[3] if len(argv) > 3 else None)
    try:
        mc.crawl()
    except KeyboardInterrupt:
        print("Interrupted.")
    else:
        print("Finished!")
        exit(0)
