"""Extract inert vendor-document text and links; never execute downloaded code."""
from html.parser import HTMLParser
from pathlib import Path
import re


class Document(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.links, self.hidden = [], [], 0
        self.link = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ('script', 'style'):
            self.hidden += 1
        if not self.hidden:
            if tag == 'a' and attrs.get('href'):
                self.link = [attrs['href'], []]
            if tag in ('p', 'div', 'li', 'tr', 'br', 'h1', 'h2', 'h3', 'h4'):
                self.parts.append('\n')

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.hidden = max(0, self.hidden - 1)
        if tag == 'a' and self.link is not None:
            self.links.append((self.link[0], ' '.join(self.link[1]).strip()))
            self.link = None

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)
            if self.link is not None:
                self.link[1].append(data)

    @property
    def text(self):
        return '\n'.join(x for line in ''.join(self.parts).splitlines()
                         if (x := re.sub(r'\s+', ' ', line).strip()))


def read(path):
    result = Document()
    result.feed(Path(path).read_text(errors='replace'))
    return result
