import doctest
from . import test_doctests
from .test_models import *
from .test_views import *
from .test_forms import *
from .test_selenium import *


DOCTEST_MODULES = (
    test_doctests,
)


def load_tests(loader, tests, ignore):
    for m in DOCTEST_MODULES:
        tests.addTests(doctest.DocTestSuite(m))
    return tests
