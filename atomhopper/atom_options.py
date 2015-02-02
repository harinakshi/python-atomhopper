import urllib


class AtomOptions(object):
    """Container for all options that can be sent to AtomHopper."""

    def __init__(
        self,
        marker=None,
        direction=None,
        limit=None,
        search=None
    ):

        self.marker = marker
        self.direction = direction
        self.limit = limit
        self.search = search

    @property
    def marker(self):
        return self._marker

    @marker.setter
    def marker(self, value):
        if value is None:
            self._marker = value
            return
        self._marker = str(value)

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        if value is None:
            self._direction = value
            return
        if str(value).lower() in ['forward', 'backward']:
            self._direction = str(value).lower()
        else:
            raise ValueError('Valid values are "forward" or "backward".')

    @property
    def limit(self):
        return self._limit

    @limit.setter
    def limit(self, value):
        if value is None:
            self._limit = value
            return
        if (0 < int(value) < 1001):
            self._limit = value
        else:
            raise ValueError('Limit must be between 1 and 1000')

    @property
    def search(self):
        return self._search

    @search.setter
    def search(self, value):
        if value is None:
            self._search = value
            return
        self._search = str(value)

    def __str__(self):
        """Output all options as an options string for the AtomHopper url.

        :returns: string -- Returns options to inject in the AtomHopper url.
        """
        options = {}

        if self.marker:
            options['marker'] = self.marker

        if self.direction:
            options['direction'] = self.direction

        if self.limit:
            options['limit'] = self.limit

        if self.search:
            options['search'] = self.search

        return urllib.urlencode(options)
