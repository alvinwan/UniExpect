# Uexpect
Uexpect offers inline testing for *any* command-line-executable language. In
other words, if language x offers an interactive prompt, Uexpect can run all
inline tests you specify, for a file written in x.

Uexpect effectively takes the notion of doctests in Python and enhances the
idea. Writing code in SQL could, for example, benefit greatly.
For starters, testing SQL code repeatedly by copying and pasting into the
interactive prompt is not only annoying but also painful: each `create table`
script would require you to `drop table` before trying new code.

##How to Use

Uexpect binary and extra configuration options coming soon.
```expect test.sql --language=sql```
```expect --set_[setting]=[value]```
```expect --set_default-language=sql```
```expect test.sql```

##Support
Uexpect can be used for nearly any programming language. Here are a few that
I've already setup configurations for:

- python3
- sqlite3
- scheme

##Installation

At some point, Uexpect will be installable via pypi:

```pip install Uexpect```
