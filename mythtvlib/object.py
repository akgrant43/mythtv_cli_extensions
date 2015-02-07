import re

from mythtvlib.backend import MythTVBackend

class MythTVObjectException(Exception):
    pass



class MythTVClass(object):
    """Abstract superclass to provide an object representation of a
    MythTV backend web service object"""

    def __init__(self, *args, **kwargs):
        # __setattr__ checks the value of _safe_mode and _definition,
        # to avoid a chicken-and-egg situation, bypass __setattr__
        self.__dict__['_safe_mode'] = False
        self.__dict__['_definition'] = None
        self._backend = MythTVBackend.default()
        all_attributes = []
        all_attributes.extend(self.__class__.keys())
        all_attributes.extend(['_backend', '_safe_mode', '_definition'])
        for k, v in kwargs.items():
            if k in all_attributes:
                setattr(self, k, v)
            else:
                raise TypeError('{0} is an invalid argument for {1}'.format(
                            k, self._class_definition['name']))
        return

    @classmethod
    def from_element(cls, element, backend=None):
        attributes = {}
        # Transfer all attributes from the element,
        # which is assumed to be a suds.sudsobject.Object
        for k, v in element:
            attributes[k] = v
        new_object = cls(**attributes)
        if backend is not None:
            new_object._backend = backend
        new_object._safe_mode = True
        return new_object

    @classmethod
    def classname(cls, name):
        "Answer the appropriate subclass"
        subclasses = cls.__subclasses__()
        subclass = None
        for cl in subclasses:
            if name == cl.__name__:
                subclass = cl
                break
        return subclass

    @classmethod
    def definition(cls):
        "Answer the receivers definition"
        raise MythTVObjectException("Subclass responsibility")

    @classmethod
    def keys(cls):
        "Answer the attribute names of the receiver"
        return cls.definition()['keys']

    def _service_api(self):
        "Answer the receivers service api"
        return self._backend.service_api(self._class_definition()['service'])

    def _class_definition(self):
        if self._definition is None:
            self.__dict__['_definition'] = self.__class__.definition()
        return self._definition

    def __setattr__(self, name, value):
        """Ensure that we don't update an attribute that is not marked user
        modifiable.
        
        TODO: Implement a non-safe mode that allows all attributes to be
        updated"""
        if self._safe_mode:
            definition = self._class_definition()
            attributes = definition['keys']
            update_attributes = definition['update_attributes']
            if (name in attributes) and (name not in update_attributes):
                raise MythTVObjectException(("Attempted to update read-only "
                                              "attribute: {0}").format(name))
        self.__dict__[name] = value
        return

    def save(self):
        """Save the receiver on the backend.
        The receiver must have all post attributes as we cannot assume
        reasonable defaults (yet)"""
        kwargs = {}
        for obj_attr, upd_attr in self._class_definition()['post_mapping'].items():
            kwargs[upd_attr] = getattr(self, obj_attr)
        getattr(self._service_api().service, self._class_definition()['post_operation'])(**kwargs)
        return

    def __repr__(self):
        definition = self.__class__.definition()
        keys = ["{0}={1}".format(k, getattr(self, k)) for k in definition['primary_key']]
        key_string = ", ".join(keys)
        return "{name}({pkey})".format(
                name=definition['name'], 
                pkey=key_string)
