"""Programming utilities."""

import functional


__maintainer__ = 'Cezary Bartoszuk <cbart@students.mimuw.edu.pl>'
__credits__ = ['Cezary Bartoszuk']


def find_members_with_prefix(cls_or_instance, prefix):
    '''Find all members, which names have the given prefix.
    '''

    if hasattr(cls_or_instance, '__mro__'):
        cls = cls_or_instance
    else:
        cls = type(cls_or_instance)

    methods = {}
    for c in cls.__mro__:
        for k, v in c.__dict__.iteritems():
            if k.startswith(prefix) and k not in methods:
                methods[k] = v
    return methods.values()


class ClassInitMeta(type):
    '''Meta class triggering __classinit__ on class intialization.'''

    def __init__(cls, class_name, bases, new_attrs):
        type.__init__(cls, class_name, bases, new_attrs)
        cls.__classinit__()


class ClassInitBase(object):
    '''Abstract base class injecting ClassInitMeta meta class.'''

    __metaclass__ = ClassInitMeta

    @classmethod
    def __classinit__(cls):
        '''
            Empty __classinit__ implementation.

            This must be a no-op as subclasses can't reliably call base class's
            __classinit__ from their __classinit__s.

            Subclasses of __classinit__ should look like:

            .. python::

                class MyClass(ClassInitBase):

                    @classmethod
                    def __classinit__(cls):
                        # Need globals().get as MyClass may be still undefined.
                        super(globals().get('MyClass', cls),
                                cls).__classinit__()
                        ...

                class Derived(MyClass):

                    @classmethod
                    def __classinit__(cls):
                        super(globals().get('Derived', cls),
                                cls).__classinit__()
                        ...
        '''
        pass

