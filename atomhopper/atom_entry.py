import json

from lxml import etree


class AtomEntry(object):
    def __init__(
        self,
        title,
        author_name,
        author_email,
        content,
        entry_id=None,
        link=None,
        updated_ts=None,
        published_ts=None
    ):
        self.title = title
        self.author_name = author_name
        self.author_email = author_email
        self.content = content
        self.entry_id = entry_id
        self.link = link
        self.updated_ts = updated_ts
        self.published_ts = published_ts

        self.categories = []

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        # Check if value is JSON
        try:
            json.loads(value)
            self._content = value
            self._content_type = 'application/json'
            return
        except Exception:
            pass

        # check if value is XML
        try:
            etree.fromstring(value)
            self._content = value
            self._content_type = 'application/xml'
            return
        except Exception:
            pass

        # Value was neither JSON nor XML
        self._content = str(value)
        self._content_type = 'text'

    @property
    def content_type(self):
        return self._content_type

    @content_type.setter
    def content_type(self, value):
        raise TypeError('Content type is based on content attribute.')

    @property
    def categories(self):
        return self._categories

    @categories.setter
    def categories(self, value):
        if value != []:
            raise TypeError('Use add_category to append new categories.')
        else:
            self._categories = value

    def add_category(self, category):
        """Adds a category to the entry - cannot be set directly."""

        self.categories.append(category)

    def to_dict(self):
        return {
            'title': self.title,
            'name': self.author_name,
            'email': self.author_email,
            'content': self.content,
            'content_type': self.content_type,
            'id': self.entry_id,
            'link': self.link,
            'updated_ts': self.updated_ts,
            'published_ts': self.published_ts,
            'categories': self.categories,
        }
