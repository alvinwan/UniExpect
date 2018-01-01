/*
Expect Utility
--------------

Regardless of comment type, all tests in this file will be detected. We will
demonstrate that expect can handle several edge cases, accommodate regular
doctest formats, and detect inline tests.

>>> SELECT "hello" || " " || "world";
hello world
>>> SELECT burd FROM LePoop WHERE goose > 2;
12
20
*/

CREATE TABLE LePoop AS -- > SELECT "hai" || ! => hai!
  SELECT 20 AS burd,    10 AS duck,     5 AS goose UNION
  SELECT 12,            2,              3         UNION
  SELECT 31,            34,             0;

-- >>> SELECT burd FROM LePoop WHERE goose > 2 LIMIT 1;
-- 20