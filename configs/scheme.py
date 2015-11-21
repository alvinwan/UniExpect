wrapper = ("scheme", "> ", None)

# doesn't exist in scheme, but we will use ;;; to denote multi-line tests
block_comments = [(';;;', ';;;')]

inline_comments = [';']

tests = [
    {
        'input_prefix': '; >>>',  # prefix for test input
        'output_prefix': '; ',  # prefix for test output
        'block_comments': True,  # just like standard doctests
        'inline_comments': False
    },
    {
        'input_prefix': '; > ',
        'output_prefix': '=>',
        'one-liner': True,
        'block_comments': True,
        'inline_comments': True
    }
]
