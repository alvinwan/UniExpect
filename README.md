> Not yet ready for use.

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

Usage is simple. To run `expect`:

> If the language `expect` uses is not correct, see below for how to manually
select a language.

```
# format
expect path/to/file

# sample
expect path/to/file samples/scheme_sample.scm
```

UE contains a variety of settings. One of the most important is to
specify a language. To do so, use the `language` flag.

> If the language is not specified, UE will (1) assume the file extension is
the language name and otherwise will (2) search all preference files with the
same first letter as the extension.

```
# format
expect path/to/file --language=the_language

# manually specify language
expect samples/sql_sample.sql --language=sql

# auto-detect language
expect samples/sql_sample.sql
```

Just as Python doctests do, UniExpect only reports incorrect outputs by
default. To view all outputs, pass the `verbose` flag. For the abbreviated flag,
add `v`s to increase verbosity.

```
# show correct outputs as well
expect samples/python_sample.py --verbose

# whine as much as possible
expect samples/python_sample.py -vvv
```

##Support

UniExpect can be used for nearly any programming language. Here are a few that
I've already setup configurations for:

- python2.7
- python3
- sqlite3
- scheme
- bash (3.2)

Custom:

- berkeleyscheme
