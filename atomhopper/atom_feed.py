from lxml import etree
import uuid

import requests
from six.moves.urllib import parse  # pylint: disable=E0611

from atomhopper import atom_entry


class AtomFeed(object):

    def __init__(self, endpoint, token, options=None):
        self._headers = {
            'Content-Type': 'application/atom+xml',
        }
        self.endpoint = endpoint
        self.token = token

        self.namespaces = {
            'atom': 'http://www.w3.org/2005/Atom'
        }

        if options:
            self.opts = str(options)

    @property
    def endpoint(self):
        return self._endpoint

    @endpoint.setter
    def endpoint(self, value):
        # Have we already set the endpoint?
        if getattr(self, 'endpoint', False):
            raise TypeError('Atom Feeds are fixed to one endpoint.')
        else:
            self._endpoint = value
            try:
                split_url = parse.urlsplit(value)
            except Exception:
                # Bad URL
                raise ValueError

            self.scheme = split_url.scheme
            self.host = split_url.netloc
            self.path = split_url.path
            self.opts = split_url.query
            self.fragment = split_url.fragment  # Unused

            # We only support http and https
            if self.scheme not in ('http', 'https'):
                raise ValueError

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value):
        self._token = value
        self._headers['X-Auth-Token'] = self._token

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, value):
        raise TypeError('Headers are determined via token.')

    @property
    def link_next(self):
        return self._extract_link('next')

    @link_next.setter
    def link_next(self, value):
        raise ValueError

    @property
    def link_previous(self):
        return self._extract_link('previous')

    @link_previous.setter
    def link_previous(self, value):
        raise ValueError

    @property
    def link_self(self):
        return self._extract_link('self')

    @link_self.setter
    def link_self(self, value):
        raise ValueError

    @property
    def link_current(self):
        return self._extract_link('current')

    @link_current.setter
    def link_current(self, value):
        raise ValueError

    @property
    def link_last(self):
        return self._extract_link('last')

    @link_last.setter
    def link_last(self, value):
        raise ValueError

    @property
    def id(self):
        return self._last_xml.xpath(
            '/atom:feed/atom:id',
            namespaces=self.namespaces
        )[0].text

    @id.setter
    def id(self, value):
        raise ValueError

    @property
    def updated_ts(self):
        return self._last_xml.xpath(
            '/atom:feed/atom:updated',
            namespaces=self.namespaces
        )[0].text

    @updated_ts.setter
    def updated_ts(self, value):
        raise ValueError

    @property
    def title(self):
        return self._last_xml.xpath(
            '/atom:feed/atom:title',
            namespaces=self.namespaces
        )[0].text

    @title.setter
    def title(self, value):
        raise ValueError

    @property
    def entries(self):
        # Grab all entries in XMl format
        xml_entries = self._last_xml.xpath(
            '/atom:feed/atom:entry',
            namespaces=self.namespaces
        )
        atom_entries = []
        # Convert to list of atom entries
        for e in xml_entries:
            title = e.xpath(
                'atom:title',
                namespaces=self.namespaces
            )[0].text

            author_name = e.xpath(
                'atom:author/atom:name',
                namespaces=self.namespaces
            )[0].text

            author_email = e.xpath(
                'atom:author/atom:email',
                namespaces=self.namespaces
            )[0].text

            # Kind of a hack for now - hard to get rid of the namespace
            # and guarantee json/xml/text ambiguous serialization
            content_element = e.xpath(
                'atom:title',
                namespaces=self.namespaces
            )[0]
            content = etree.tostring(
                content_element,
                with_tail=False
            ).split('</content>')[0].split('">')[1]

            entry_id = uuid.UUID(e.xpath(
                'atom:id',
                namespaces=self.namespaces
            )[0].text.split('urn:uuid:')[1])

            link = e.xpath(
                'atom:link',
                namespaces=self.namespaces
            )[0].get('href')

            updated_ts = e.xpath(
                'atom:updated',
                namespaces=self.namespaces
            )[0].text

            published_ts = e.xpath(
                'atom:published',
                namespaces=self.namespaces
            )[0].text

            # TODO(Kuwagata) Convert the entry to object
            atom_entries.append(
                atom_entry.AtomEntry(
                    title,
                    author_name,
                    author_email,
                    content,
                    entry_id,
                    link,
                    updated_ts,
                    published_ts
                )
            )

        return atom_entries

    @entries.setter
    def entries(self, value):
        raise ValueError
    
    def get_url(self):
        return parse.urlunsplit(
            (
                self.scheme,
                self.host,
                self.path,
                self.opts,
                self.fragment
            )
        )

    def refresh(self):
        """Re-gets the feed and returns the response."""

        return self._get(self.get_url())

    def get_all_entries(self):
        """Generator that yields all events in the feed."""

        self.refresh()
        while True:
            for entry in self.entries:
                yield entry

            # Navigate to next page - HTTP call
            if self.next() is None:
                break

    def post_event(self, atom_data):
        """Add an event to the RSE feed."""

        self._post(self.get_url(), atom_data)

    def next(self):
        """Loads the next page into the feed."""

        if self.link_next is None:
            return None
        return self._get(self.link_next)

    def prev(self):
        """Loads the previous page into the feed."""

        if self.link_previous is None:
            return None
        return self._get(self.link_previous)

    def last(self):
        """Loads the last page into the feed."""

        if self.link_last is None:
            return None
        return self._get(self.link_last)

    def _get(self, url):
        """Underlying get that performs error checks."""

        resp = requests.get(url, headers=self.headers)
        resp.raise_for_status()
        self._last_xml = etree.fromstring(resp.text)
        return resp.text

    def _post(self, url, data):
        """Underlying post that performs error checks."""

        resp = requests.post(url, data=data, headers=self.headers)
        resp.raise_for_status()

    def _extract_link(self, rel):
        """Grabs named links from the feed."""

        try:
            return self._last_xml.xpath(
                "//atom:link[@rel='" + rel + "']/@href",
                namespaces=self.namespaces
            )[0]
        except IndexError:
            return None
