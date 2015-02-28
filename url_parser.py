from urlparse import urlparse as urlp
from urlparse import urlsplit as urls
from urlparse import urljoin as urlj

def Myurlparser(base_url, links):
    result = []
    
    for l in links:
        if ('.py' in l) or ('cgi' in l) or ('.css' in l) or ('.aspx' in l) or ('.zip' in l) or ('.exe' in l) or ('.msi' in l) or ('.chm' in l) or ('.asc' in l) or ('.pkg' in l) or ('png' in l) or ('.svg' in l):
            continue
        parse = urlp(l)
        """check https// """
        if parse.scheme:
            s = parse.scheme
            if ('http' in s) or ('https' in s) or ('ftp' in s) or ('cap' in s) or ('nfs' in s):
                result.append(l)
        else:
            """split to normalize url"""
            s = urls(l)
            try:
                result.append(urlj(base_url, s.geturl()))
            except Exception as e:
                print(e)

    return result
