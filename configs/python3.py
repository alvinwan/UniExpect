shell = {
    'command': 'python3',
    'prompt': '>>> ',
    'continuation': '\.\.\. '
}

language = 'python3'
extension = 'py'
block_comments = [('"""', '"""')]
inline_comments = ['#']

tests = [  # test formats higher up get precedence
    {
        'input_prefix': '>>>',  # prefix for test input
        'output_prefix': '',  # prefix for test output
        'block_comments': True,  # like doctests, runs tests in block as a suite
        'inline_comments': False  # no output_prefix = no inline_comments
    },
    {
        'input_prefix': '>',
        'output_prefix': '=>',
        'one-liner': True,
        'block_comments': True,
        'inline_comments': True
    }
]
