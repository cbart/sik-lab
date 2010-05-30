import unittest
from sklab.util.functional import \
        oneshot, reset_oneshot, inject_function_before, inject_function_after
from sklab import util

class TestCaseBase(unittest.TestCase, util.ClassInitBase):
    '''A "black-magic" base class for tests.

       Provides two features:

       1. Replaces `setUp` and `tearDown` methods in derived classes, such
          that they call all methods prefixed `setUp_` and `tearDown_`,
          along with the original `setUp` and `tearDown`.

       2. Autmatically decorates all `setUp*` and `tearDown*` methods with
          `@oneshot`.

       This is intended to be used by convenient testing mixins, so that they
       can provide their own `setUp()` and `tearDown()` methods, without the
       need to explicitly call them in derived classes.

       It is guaranteed, that the `setUp` method is called after all
       `setUp_*` methods and `tearDown` before all `tearDown_*` methods.
       `setUp_*` methods are called in alphanumeric order, `tearDown_*`
       in the reverse alphanumeric order.

       It is advised to name these methods according to the pattern
       `{setUp,tearDown}_nnnn_description`, where `nnnn` represents a
       four-digit number (with leading zeroes).
    '''

    @classmethod
    def __classinit__(cls):
        super(globals().get('TestCaseBase', cls), cls).__classinit__()

        # Decorate setUp and tearDown such that they automatically call
        # setUp_* and tearDown_* methods.

        if 'setUp' in cls.__dict__:
            decorator = inject_function_before(cls.__callSetUpMethods)
            cls.setUp = decorator(cls.setUp)

        if 'tearDown' in cls.__dict__:
            decorator = inject_function_after(cls.__callTearDownMethods)
            cls.tearDown = decorator(cls.tearDown)

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        util.ClassInitBase.__init__(self)

    def __callMethodsWithPrefix(self, prefix, reverse=False):
        # Call all methods with specified prefix, in alphabetical order (or
        # reversed).

        methods = util.find_members_with_prefix(self, prefix)
        methods.sort(key=lambda m: m.__name__, reverse=reverse)
        for m in methods:
            m(self)

    @oneshot
    def __callSetUpMethods(self):
        self.__callMethodsWithPrefix('setUp_')
        reset_oneshot(self.__callTearDownMethods)

    @oneshot
    def __callTearDownMethods(self):
        self.__callMethodsWithPrefix('tearDown_', reverse=True)
        reset_oneshot(self.__callSetUpMethods)

    def setUp(self):
        # We need this empty function, so setUp_* methods are called even if
        # setUp is never overridden in subclasses.
        pass

    def tearDown(self):
        # We need this empty function, so tearDown_* methods are called even if
        # tearDown is never overridden in subclasses.
        pass


class TestCase(TestCaseBase):
    '''An SKLAB base TestCase.'''

    pass

