import argparse
import importlib
import re
import subprocess
import random
import string
import select

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
                    detailed reporting')

def main(args):
    """Main function for except utility. Prints output of the process function.
    """
    try:
        for output, data in process(args):
            correct = output['expected'] == output['actual']
            if not correct:
                for k, v in output.items():
                    print(k + ':')
                    print(v)
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
                    [line, lines.pop(0), test] if not test['output_prefix'] else
                    split(line, test['output_prefix']) + [test]))
        suites.append(suite)

    # assemble all inline tests
    for inline in inlines:
        inline = inline.strip()
        map_break(inline_tests,
            lambda test: inline.startswith(test['input_prefix']),
            lambda test: suites.append(split(inline, test['output_prefix']) + [test]))

    # execute all suites of code
    for suite in suites:

        # initialize process for suite
        process = subprocess.Popen([settings.command],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        poll = select.poll()
        poll.register(process.stdout.fileno(), select.POLLIN)

        # run file
        process.stdin.write(code.encode('utf-8'))
        process.stdin.flush()

        for i, data in enumerate(suite):

            # get and clean data
            cmd, out, test = data
            cmd = cmd.replace(test['input_prefix'], '').strip()
            out = out.strip()

            # issue command
            process.stdin.write((cmd + "\n").encode('utf-8'))
            process.stdin.flush()

            # add output back to data
            suite[i] = ({
                'command': cmd,
                'expected': out,
                'actual': process.stdout.readline() if poll.poll(100) else '',
            }, {
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
    return [pieces[0], divider.join(pieces[1:])]

if __name__ == '__main__':
	args = parser.parse_args()
	main(args)
