import argparse
from utils import Expect

hbar = '*' * 70

header_output = hbar + """

Testing {}\n
""" + hbar

test_output = """
{command}

Expected:
{expected}
Actual:
{actual}

""" + hbar

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
    print(header_output.format(args.filename))
    length = passed = 0
    for output, data in Expect(args.filename, args.language).go():
        length += 1
        correct = output['expected'] == output['actual']
        passed += int(correct)
        if not correct or args.verbose:
            print(test_output.format(**output))
    if length == passed:
        print('\nAll passed!\n')
    else:
        print('\nPassed', passed, 'of', length, 'tests.\n')
    print('*'*70)


if __name__ == '__main__':
	args = parser.parse_args()
	main(args)
