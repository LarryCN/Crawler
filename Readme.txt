Python 2.7.5                 |
crawler version 1.0 by larry |
_____________________________|
please see file google.py firstly
_____________________________

How to run it?

Use command line "python crawler.py n keyword1 keyword2..."  (in the same directory with crawler.py)
command should be with at least 2 parameters.
One is n, the number of pages to crawler
One is following keywords, these keywords firstly used to get top10 results from google, then the top10 results used as initial links for the crawler to work.

Output in the command line?
In the file crawler.py, there is DEBUG_LOG could be set to output debug log in the terminal, of course some necessery log still output if it sets Fasle
some log looks like(or exception log):
http://www.ccny.cuny.edu/compsci/                        currently access url
('fetch .....', True)                                    depend on robots.txt could fetch
('fetch .....', False)                                   depend on robots.txt could not fetch
('ok ', 'doc id ', 218, 'size ', 152190, 'depth ', 2)    page successly downloaded with docID 218, size 152190 bytes, depth 2(to the start page)
other log could be read from the words..... file log has similar context


Running time(not include first search top 10 time, cause it`s not part of crawler)?
As python mostly running time diffs quite big depends on cache or .... some thing I could not know .... (from leetcode or other normal test I conclude this)
And this programme write log to other file, it quite costs time, and some code is not that optimatised
Here are two tests:
1. With DEBUG_LOG = True n = 500, keywords = computer science 
    ('run begins ', 'Thu Feb 12 03:06:41 2015')
    storage is full
    ('total size ', 94514135, ' total pages number ', 500)
    Thu Feb 12 03:09:24 2015
  so runtime = 163s, total data size = 90.14 MB 
2. With DEBUG_LOG = False n = 500, keywords = computer science  
    ('run begins ', 'Thu Feb 12 03:24:11 2015')
    storage is full
    ('total size ', 94492739, ' total pages number ', 500)
    Thu Feb 12 03:26:57 2015
  so runtime = 166s(=.=!), total data size = 90.11 MB

storage is full means downloaded pages reach n
 

Other things need to notice
storage path, in the file crawler.py, change default_path change the path to store downloaded pages
log path in the file crawler.py, change default_log_path change the path to record log, and here only record one log, which means if restart crawler, log will be refreshed.
Normally, docID starts from 0, then 1, 2, ....

_________________________________________
files
_________________________________________
html_parser.py
This file is to handle html parser, class MyHTMLParser could be used. Now this is only to parse attribute with "href", and store them in the self.links, function get_links could be used to get parse urls

url_parser.py
This file is to handle parse url, or to check whether or not the url could be used to fetch a page and whether or not it is ligel. 
url itself might be completed with "htpps://...", as this case we keep the result
url might be changed it context because of extracting from downloaded page, then we handle it by urlsplit.
In the end, we use urljoin the get the parsed url and base url together
url parser will exclude some type like .css, .exe, .zip... also only include some basic scheme like htttp, https, ftp....

log
This file is to record operations of the crawler`s working. 
some might be recorded like:
n     : number of pages to be crawlered
url   : accessed url, which is not guaranteed to download related page as other reasons like forbidden, not html...
pages : the pages downloaded, record url, docID, page size, url depth, total downloaded pages size, total downloaded pages number
priority: in this version we just simply to set priority depended on keywords, which initial search in google to get top ranked pages, showed up times. Like, if the keywords are "search engine", we check the number of serach and engine showed up times in the page, then sum up the total count. No doublt that priority value is just the count value.

Here we need to metion that this crawler is use BSF algorithm, so the priority is not cover the whole links needed to crawl, like for depth 1, we got 10 pages to download, after downloading then, we compute these 10 pages priority seperately, then enqueue them by priority. However, in the depth 2, the priority order of page1`s urls should not be crossed by page2`s urls as it`s using BSF

google.py
This file is mainly to provide the interface to search directly from google search engine to get top 10 results.
By the way, to support it`s normally running we also need to instal BeautifulSoup, whose version should not be concerned, I suppose.

crawler.py
This file provides class crawler.
In this version we just realize a simple BSF, single-thread crawler.
It will crawler pages until it reaches the parameter n
term_count, this function is to count keywords showed up times in the target page, mainly use nltk library to handle.
robot_check, to check url satisfied the robot exclusion protocol(robotparser)







