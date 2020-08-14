import doctest
from . import test_doctests
from .tests import *
from .test_models import *
from .test_fixtures import *


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(test_doctests))
    return tests
