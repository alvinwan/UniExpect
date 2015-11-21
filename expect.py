import argparse
import importlib
import re
import subprocess
import random
import string
import select
from pexpect.replwrap import REPLWrapper

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
parser.add_argument('-v', '--verbose', help='turn on verbose mode for more \
                    detailed reporting', action='store_true')

def main(args):
    """Main function for except utility. Prints output of the process function.
    """
    try:
        print('*'*70)
        print("""
        Testing {}\n'.format(args.filename)
        """)
        print('*'*70)
        length = passed = 0
        for output, data in process(args):
            length += 1
            correct = output['expected'] == output['actual']
            passed += int(correct)
            if not correct or args.verbose:
                print("""
                >>> {command}

                Expected:
                {expected}
                Actual:
                {actual}
                """)
                print('*'*70)
        if length == passed:
            print('\nAll passed!\n')
        else:
            print('\nPassed', passed, 'of', length, 'tests.\n')
        print('*'*70)
    except subprocess.CalledProcessError as e:
        pass


def process(args):
    """Main parser and tester for the except utility.

    @return: a list of tests, and their expected outputs
    """
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
    block_tests = list(filter(lambda s: s['block_comments'], settings.tests))
    inline_tests = list(filter(lambda s: s['inline_comments'], settings.tests))

    # test suites
    suites = []

    # assemble all block tests
    for block in blocks:
        lines, suite = list(block.split('\n')), []
        while lines:
            line = lines.pop(0).strip()
            map_break(block_tests,
                lambda test: line.startswith(test['input_prefix']),
                lambda test: suite.append(
                    [line, lines.pop(0), test]
                    if not test.get('one-liner', False) else
                    split(line, test['output_prefix']) + [test]))
        suites.append(suite)

    # assemble all inline tests
    for inline in inlines:
        inline = inline.strip()
        map_break(inline_tests,
            lambda test: inline.startswith(test['input_prefix']),
            lambda test: suites.append([split(inline, test['output_prefix']) + [test]]))

    # execute all suites of code
    for suite in suites:

        wrapper = REPLWrapper(*settings.wrapper)

        for i, data in enumerate(suite):

            # get and clean data
            command, expected, test = data
            command = command.replace(test['input_prefix'], '').strip()
            expected = expected.replace(test['output_prefix'], '').strip()

            # issue command, getting rid of line break at end
            actual = wrapper.run_command(command)[:-2]

            # add output back to data
            suite[i] =(dict(command=command, expected=expected, actual=actual),{
                'type': test
            })

            yield suite[i]


def map_break(items, condition, f):
    """Calls function f on the item where a condition is satisfied"""
    for item in items:
        if condition(item):
            f(item)
            break

def split(string, divider):
    """Splits a string according at the first instance of a divider."""
    pieces = string.split(divider)
    return [pieces[0].strip(), divider.join(pieces[1:])]

if __name__ == '__main__':
	args = parser.parse_args()
	main(args)
