from html_parser import MyHTMLParser
from url_parser import Myurlparser
import urllib, urllib2

import os
from collections import deque
import nltk
import time

default_path = "/Users/larry/Code/wsn/data/"
default_log_path = "/Users/larry/Code/wsn/crawler/log"
DEBUG_LOG = False

import codecs, robotparser
from urlparse import urlparse as urlp

class crawler:
    def __init__(self, max_n, keywords, path = default_path, docID = 0):
        self.q = deque()
        self.max_n = max_n
        self.count = 0
        self.path = default_path
        self.docID = docID
        self.visit = {}
        self.doc = {}
        self.keywords = keywords
        self.size = 0
        self.robot = {}
    
    """check allow to access depended on robots.txt"""
    def robot_check(self, url):
        par = urlp(url)
        if par.netloc in self.robot:
            rp = self.robot[par.netloc]
        else:
            robot_url = par.scheme + "://" + par.netloc + "/robots.txt"
            if DEBUG_LOG:
                print(robot_url)
                print(url)
            rp = robotparser.RobotFileParser()
            rp.set_url(robot_url)
            try:
                rp.read()
                self.robot[par.netloc] = rp
            except Exception as e:
                print(e)
                return True
        try:
            ret = rp.can_fetch("*", url)
        except Exception as e:
            print(e)
            ret = False
        if DEBUG_LOG:
            print("fetch .....", ret)
        return ret

    """ just simply compute keywords show up times totally"""    
    def term_count(self, filepath):
        raw = open(filepath).read()
        try:
            tokens = nltk.word_tokenize(raw)
            text = nltk.Text(tokens)
            count = 0
            #print('key     ', self.keywords)
            for w in self.keywords:
                #print(w, text.count(w))
                count += text.count(w)
        except Exception as e:
            print(e)
            count = -1
        return count

    def fetch_html(self, links, depth):
        doc = []
        log = open(default_log_path, 'a')
        for l in links:
            if self.count >= self.max_n:
                log.close()
                return 
            """check the links whether or not be accessed before"""
            if l not in self.visit:
                if DEBUG_LOG:
                    print(l)
                if not self.robot_check(l):
                    continue
                log.write("visit url " + l + " " + time.ctime() + "\n")
                self.visit[l] = 1
                filepath = self.path + str(self.docID)
                req = urllib2.Request(l)
                try:
                    response = urllib2.urlopen(req)
                    """ download html """
                    if response.info().type == 'text/html':
                        html = response.read()
                        f = codecs.open(filepath, 'w', encoding = 'utf-8')
                        f.write(html)
                        """compute file size"""
                        size = os.path.getsize(filepath)
                        self.size += size
                        self.doc[self.docID] = [filepath, size, depth + 1, l]
                        doc.append([self.docID, filepath])
                        log.write("download page " + l + " docID " + str(self.docID) + " size " + str(size) + " depth " + str(depth) + " total size: " + str(self.size) + " total num: " + str(self.count + 1) + " " + time.ctime() + '\n')
                        if DEBUG_LOG:
                            print('ok ', "doc id ", self.docID, "size ", size, 'depth ', depth + 1)
                        self.docID += 1
                        self.count += 1
                    else:
                        print(response.info().type)
                except urllib2.URLError as e:
                    print(e.reason)
                except Exception as e:
                    print(e)

        """depends on the keywords priority to decide enqueue order"""
        for item in doc:
            count = self.term_count(item[1])
            #print(item[0], count)
            item.append(count)
        doc.sort(key = lambda x:x[2], reverse = True)
        for item in doc:
            if item.count >= 0:
                self.q.append(item[0])
                self.doc[item[0]].append(item[2])
                log.write("docID " + str(item[0]) + " priority is " + str(item[2]) + "\n")
        log.close()

    def bfs(self):
        while self.q and self.count < self.max_n:
            docID = self.q.popleft()
            doc = self.doc[docID]
            data = open(doc[0]).read()
            parser = MyHTMLParser()
            parser.feed(data)
            links = parser.get_links()
            links = Myurlparser(doc[3], links)
            log = open(default_log_path, 'a')
            log.write(" \n")
            log.write("crawl url on page(docID) " + str(docID) + " priority is " + str(doc[-1]) + "\n")
            log.write(" \n")
            log.close()
            if DEBUG_LOG:
                print("crawl ", docID, 'priority ', doc[-1])
            self.fetch_html(links, doc[2])
        if self.count >= self.max_n:
            print("storage is full")
            print("total size ", self.size, " total pages number ", self.count)
        else:
            print("run done")
            print("total size ", self.size, " total pages number ", self.count)
        print(time.ctime())

    def run(self, links):
        print("run begins ", time.ctime())
        self.fetch_html(links, -1)
        self.bfs()

import sys
import google

if __name__ == '__main__':
    print("crawler ...... larry")
    if len(sys.argv) < 3:
        print("should set at least two parameters: 1. number n: pages to be crawled 2. keywords (1, 2, or ...).")
        exit()

    try:
        max_n = int(sys.argv[1])
    except:
        print("First parameter should be digital")
        exit()
    keywords = sys.argv[2:]
    reload(sys)
    sys.setdefaultencoding("utf-8")
    print(max_n, keywords)
    context = ""
    for s in keywords:
        context += s + ' '
    context = context[:-1]
    print("search :", context)
    re = []
    for url in google.search(context, stop = 10):
        re.append(url)
    top_url = re[:10]
    print("top 10 url:")
    for u in top_url:
        print(u)
    log = open(default_log_path, 'w')
    log.write("larry crawler..... fetch " + str(max_n) + " pages\n")
    log.close()
    c = crawler(max_n, keywords)
    c.run(top_url)

