from .utils import map_break
from .utils import split
from .configs import languages
import re
from pexpect.replwrap import REPLWrapper


class Expect:
    """
    Main Expect utility for parsing and running tests on file
    """

    def __init__(self, filename, language):

        # load settings from configuration file
        extension = filename.split('.')[-1]
        for module in languages:
            if module.language == language or module.extension == extension:
                self.settings = module

        # grab contents of file
        self.filename = filename
        self.code = open(filename).read()

    @staticmethod
    def extract_comments(code, settings):
        """Extracts all block and inline comments"""

        # decommented code
        decommented_code = code

        # extract all block comments
        blocks = []
        for start, end in settings.block_comments:
            block = re.compile('{}[\S\s]+?{}'.format(start, end))
            blocks.extend(block.findall(code))
            decommented_code = block.sub('', decommented_code)

        # extract all inline comments
        inlines = []
        for start in settings.inline_comments:
            inline = re.compile('{}[^\n]+'.format(start))
            inlines.extend(inline.findall(code))
            decommented_code = inline.sub('', decommented_code)

        return blocks, inlines, decommented_code

    @staticmethod
    def identify_tests(code, settings):
        """Identifies all block and inline test formats"""

        # identify all possible test types
        block_tests = list(filter(lambda s: s['block_comments'], settings.tests))
        inline_tests = list(filter(lambda s: s['inline_comments'], settings.tests))

        return block_tests, inline_tests

    @staticmethod
    def extract_tests(*args):
        """Extracts all tests and packages them into suites

        @return: suites, decommented_code
        """
        block_comments, inline_comments, code = Expect.extract_comments(*args)
        block_tests, inline_tests = Expect.identify_tests(*args)

        # test suites
        suites = []

        # assemble all block tests
        for block in block_comments:
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
        for inline in inline_comments:
            inline = inline.strip()
            map_break(inline_tests,
                lambda test: inline.startswith(test['input_prefix']),
                lambda test: suites.append([split(inline, test['output_prefix']) + [test]]))

        return suites, code

    @staticmethod
    def new_session(settings, command=None):
        """Returns a new REPLWrapper"""
        return REPLWrapper(
            command or settings.shell['command'],
            settings.shell['prompt'],
            None,
            continuation_prompt=settings.shell['continuation'])

    @staticmethod
    def run_command(command, session, settings, timeout=1):
        """Runs a command in the REPLWrapper"""
        return session.run_command(command)[:-2]

    @staticmethod
    def run_file(command, session, settings, timeout=1):
        """Runs a python file in the provided session by feeding the interpreter
        one line at a time. At each iteration, run_file checks for a
        continuation or regular prompt and finally closes the expect properly,
        so that the REPLWrapper works properly the next run.
        """

        # get prompts
        init, cont = settings.shell['prompt'], settings.shell['continuation']

        # setup
        results, commands, a, b = [], command.splitlines(), init, cont

        # send command
        session.sendline(commands[0])

        for line in commands:

            # test both continuation and initial prompts
            try:
                session.expect(a, timeout=timeout)
            except:
                # swap if other prompt is found
                session.expect(b, timeout=timeout)
                b, a = a, b

            # send new command
            session.sendline(line)

            # grab output
            if a == init:
                output = session.before.splitlines()[1:]
                results.extend(output)

        # if last command resulted in continuation, terminate and grab output
        if a == cont:
            session.sendline('')
            session.expect(init)
            results.append(session.before)

        return '\n'.join(results)

    def go(self):
        """Provides a generator that gives test results one at a time."""

        code = self.code
        settings = self.settings

        suites, decommented_code = Expect.extract_tests(code, settings)

        # execute all suites of code
        for suite in suites:

            # start new session for each suite and load current file
            if 'command_with_file' in settings.shell:
                session = Expect.new_session(settings,
                    command=settings.shell['command_with_file'].format(
                        filename=self.filename))
            else:
                session = Expect.new_session(settings)
                if '_load_file' in settings.shell:
                    output = Expect.run_command(
                        settings.shell['_load_file'].format(
                            filename=self.filename), session, settings)
                else:
                    output = Expect.run_file(
                        decommented_code, session.child, settings)

            for i, data in enumerate(suite):

                # get and clean data
                command, expected, test = data
                command = command.replace(test['input_prefix'], '').strip()
                expected = expected.replace(test['output_prefix'], '').strip()

                # issue command
                actual = Expect.run_command(command, session, settings)

                # add output back to data
                yield ({
                    'command': command,
                    'expected': expected,
                    'actual': actual
                },{
                    'type': test
                })
