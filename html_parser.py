from HTMLParser import HTMLParser as Parser

class MyHTMLParser(Parser):
    def __init__(self):
        Parser.__init__(self)
        self.links = []

    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if attr[0] == "href":
                self.links.append(attr[1])

    def get_links(self):
        return self.links
