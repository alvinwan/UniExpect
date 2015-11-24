> Not yet ready for use.

# UniExpect
UniExpect offers inline testing for *any* command-line-executable language. In
other words, if language x offers an interactive prompt, UniExpect can run all
inline tests you specify, for a file written in x.

UniExpect effectively takes the notion of doctests in Python and enhances the
idea. Writing code in SQL could, for example, benefit greatly.
For starters, testing SQL code repeatedly by copying and pasting into the
interactive prompt is not only annoying but also painful: each `create table`
script would require you to `drop table` before trying new code. Not to mention,
each accidental table modification means you have to restart the session,
copy in the data, and *then* try your code again.

##How to Use

UniExpect binary and extra configuration options coming soon.

```
expect test.sql --language=sql
```

```
expect --set_[setting]=[value]
```

```
expect --set_default-language=sql
```

```
expect test.sql
```

##Support
UniExpect can be used for nearly any programming language. Here are a few that
I've already setup configurations for:

- python2.7
- python3
- sqlite3
- scheme
- bash (3.2)

##Installation

At some point, UniExpect will be installable via pypi:

```pip install uniexpect```
