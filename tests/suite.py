import unittest
import os
from optparse import OptionParser
import logging

"""
to run tests:

    All tests
        $ tox

    All tests in all files matching glob
        $ tox --  -p *node*

    All tests in class in module:
        $ tox -- test_node.NodeCreateTests

    Single test:
        $ tox -- test_node.NodeCreateTests.test_create_named_node
"""

parser = OptionParser('usage: %prog [options] -- [testsuite options]')

parser.add_option('-v', '--verbose',
                  action='count', dest='verbose', default=2,
                  help='increase verbosity')

parser.add_option('-p', '--pattern',
                  dest='pattern',
                  default='test*.py',
                  help='pattern for tests')

parser.add_option('-d', '--dbtype',
                  default='auto',
                  choices=['auto', 'mongo', 'ming'],

                  help='Backend DB')

(options, args) = parser.parse_args()

loader = unittest.TestLoader()
suite = unittest.TestSuite()
os.environ["LUNA_TEST_DBTYPE"] = options.dbtype

# prepend log messages with tab
log_format = "\t%(levelname)s:%(name)s:%(message)s"
logging.basicConfig(format=log_format)
if options.verbose < 3:
    logging.disable(logging.CRITICAL)

if args:
    for elem in args:
        suite.addTests(
            loader.loadTestsFromName(elem),
        )
else:
    tests_dir = os.path.dirname(os.path.realpath(__file__))
    suite.addTests(
        loader.discover(tests_dir, options.pattern),
    )

if __name__ == '__main__':
    runner = unittest.TextTestRunner(
        verbosity=options.verbose,
    )
    runner.run(suite)
