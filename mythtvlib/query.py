"""
MythTVQuerySet is the general search mechanism for querying the MythTV Backend
"""
import re
from copy import copy

from mythtvlib.models import MythTVClass

class MythTVQueryException(Exception):
    pass



class MythTVQuerySet(object):
    """Provide a django like interface for filtering MythTV objects."""
    
    def __init__(self, classname):
        self.mythtv_class = MythTVClass.classname(classname)
        if self.mythtv_class is None:
            raise MythTVQueryException("Unknown class name: {0}".format(classname))
        # _filters is a list of (field_name, field_regex, compiled_regex)
        self._filters = []
        self._records = None
        return

    def filter(self, **kwargs):
        "Add the supplied filter to the list."
        new_query = self.copy()
        attributes = self.mythtv_class.keys()
        for k, v in kwargs.items():
            if k not in attributes:
                raise MythTVQueryException(("Attempt to filter on" 
                                    "non-existant attribute: {0}").format(k))
            new_query._filters.append((k, v, re.compile(v)))
        if self._records is not None and len(self._records) > 0:
            self._apply_filters()
        return new_query

    def _apply_filters(self):
        """Apply the receivers filters to the records"""
        if self._records is None:
            self._records = self.mythtv_class.all()
        # TODO: This can probably be optimised in some way
        if len(self._filters) > 0:
            filtered_records = []
            for rec in self._records:
                for f in self._filters:
                    if f[2].search(str(getattr(rec, f[0]))):
                        filtered_records.append(rec)
            self._records = filtered_records
        return

    def all(self):
        """Answer all the records in a copy of the receiver"""
        self._apply_filters()
        return self._records

    def copy(self):
        """Answer a copy of the receiver.
        If _records are not None, copy the record list"""
        new_copy = copy(self)
        if new_copy._records is not None:
            new_copy._records = copy(new_copy._records)
        return new_copy

