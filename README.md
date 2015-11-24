> Not yet ready for use.

# UniExpect
UniExpect (UE) offers inline testing for *any* command-line-executable language.
In other words, if language x offers an interactive prompt, UniExpect can run
all inline tests you specify, for a file written in x.

UE effectively takes the notion of doctests in Python and enhances the
idea. Writing code in SQL could, for example, benefit greatly.
For starters, testing SQL code repeatedly by copying and pasting into the
interactive prompt is not only annoying but also painful: each `create table`
script would require you to `drop table` before trying new code. Not to mention,
each accidental table modification means you have to restart the session,
copy in the data, and *then* try your code again.

##How to Use

UE contains a variety of features. One of the most important is to
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

##Installation

At some point, UniExpect will be installable via pypi:

```pip install uniexpect```
