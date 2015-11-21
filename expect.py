import argparse
import importlib
import re

parser = argparse.ArgumentParser(description="""
=============== EXPECT TESTING =================
This small utility allows you to use inline,
'expect' tests for any language. It's primarily
built for languages that don't already support
inline tests, but any language (even Python!) may
be added using a configuration file.
""")

parser.add_argument('filename', type=str, help='the file to parse for tests')
parser.add_argument('-l', '--language', type=str, help='the language to parse',
                    default='python3')

def main(args):

    # load settings from configuration file
    settings = importlib.import_module('configs.{}'.format(args.language))

    # grab contents of file
    code = open(args.filename).read()

    # extract all block comments
    blocks = []
    for start, end in settings.block_comments:
        block = re.compile('{}[\S\s]+?{}'.format(start, end))
        blocks.extend(block.findall(code))

    # extract all inline comments
    inlines = []
    for start in settings.inline_comments:
        inline = re.compile('{}[^\n]+'.format(start))
        inlines.extend(inline.findall(code))

    # identify all possible test types
    block_tests = filter(lambda s: s['block_comments'], settings.tests)
    inline_tests = filter(lambda s: s['inline_comments'], settings.tests)

    # test suites
    suites = []

    # assemble all block tests
    for block in blocks:
        lines, suite = list(block.split('\n')), []
        while lines:
            line = lines.pop(0)
            map_break(block_tests,
                lambda test: line.startswith(test['input_prefix']),
                lambda test: suite.append(
                    (line, lines.pop(0)) if not test['output_prefix'] else
                    parse_inline(line, test)))
        suites.append(suite)

    # assemble all inline tests
    for inline in inlines:
        map_break(inline_tests,
            lambda test: line.startswith(test['input_prefix']),
            lambda test: suites.append(parse_inline(line, test)))

    # execute all suites of code
    for suite in suites:
        pass

def map_break(items, condition, f):
    """Calls function f on the item where a condition is satisfied"""
    for item in items:
        if condition(item):
            f(item)
            break

def parse_inline(line, test):
    """Parses an inline test and returns a tuple containing the test and
    its expected output.
    """
    gap_start = line.indexof(test['output_prefix'])
    gap_end = end + len(test['output_prefix'])
    return (line[:gap_start], lin[gap_end:])

if __name__ == '__main__':
	args = parser.parse_args()
	main(args)
