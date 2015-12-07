# UniExpect
UniExpect (UE) offers inline testing for *any* command-line-executable language,
effectively making the notion of doctests universal. There are two immediate
benefits to using the UE utility:

1. With this, code in all languages can be placed directly below executable,
easily-checked tests that help to explain a function or class's basic
functionality.

2. The "unittest" approach to testing antiquates manual, sandbox testing.
Writing code in SQL could, for example, could benefit immensely. Each accidental
table modification means you have to restart the session, copy in the data, and
*then* try your code again. With UE, it's just one command.

See below for how to get started.

##Installation

At some point, UniExpect will be installable via pypi:

```
pip install uniexpect
```

##How to Use

(coming soon)

##How to Run

Usage is simple. To run `expect` on `samples/scheme_sample.scm`:

```
expect samples/scheme_sample.scm
```

##Settings

The following is an abridged list of more commonly-used settings. For a full
list, run `expect --help`.

###`--language=<language>`

If the language is not specified, UE will (1) assume the file extension is
the language name and, if no such configuration file exists, will (2) search all
preference files with the same first letter as the extension.

Example: `expect samples/sql_sample.sql --language=sql`

###`--verbose`

Just as Python doctests do, UniExpect only reports incorrect outputs by
default. To view all output, pass the `verbose` flag. Add `v`s to increase
verbosity, with `-vvv` for maximum whining.

Examples:
- `expect samples/python_sample.py --verbose`
- `expect samples/python_sample.py -vvv`

##Support

UniExpect can be used for nearly any programming language. Here are a few that
I've already setup configurations for:

- python2.7
```
expect samples/python_sample.py --language=python2
```

- python3
```
expect samples/python_sample.py --language=python3
```

- scheme
```
expect samples/scheme_sample.scm
```
version: chibi-scheme

- sqlite3
```
expect samples/sqlite_sample.sql
```

- bash
```
expect samples/bash_sample.sh --language=bash
```
version: 3.2

Custom:

- berkeleyscheme
```
expect samples/berkeleyscheme_sample.scm --language=berkeleyscheme
```

##How to Add Language

(coming soon)
