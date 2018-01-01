import argparse
from .expect import Expect

hbar = '*' * 70

header_output = hbar + """

Testing {filename} on {language}

""" + hbar

test_output = """
>>> {command}

Expected:
{expected}

Actual:
{actual}

""" + hbar

parser = argparse.ArgumentParser(description="""
This small utility allows you to use inline, 'expect' tests for any language.
It's primarily built for languages that don't already support inline tests, but
any language (even Python!) may be added using a configuration file.
""")

parser.add_argument('filename', type=str, help='the file to parse for tests')
parser.add_argument('-l', '--language', type=str, help='the language to parse',
                    default=None)
parser.add_argument('-v', '--verbose', help='turn on verbose mode for more \
                    detailed reporting', action='store_true')


def main():
    """Main function for except utility. Prints output of the process function.
    """
    args = parser.parse_args()
    expect = Expect(args.filename, args.language)
    print(header_output.format(
        filename=args.filename,
        language=expect.settings.language))
    length = passed = 0
    for output, data in expect.go():
        length += 1
        correct = output['expected'] == output['actual']
        passed += int(correct)
        if not correct or args.verbose:
            print(test_output.format(**output))
    if length == passed:
        print('\nAll passed!\n')
    else:
        print('\nPassed', passed, 'of', length, 'tests.\n')
    print(hbar)


if __name__ == '__main__':
    main()

