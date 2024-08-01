```bash
$ npm audit            
# npm audit report

got  <11.8.5
Severity: moderate
Got allows a redirect to a UNIX socket - https://github.com/advisories/GHSA-pfrx-2q88-qq97
No fix available
node_modules/got
  @hackmd/pandoc.js  *
  Depends on vulnerable versions of got
  node_modules/@hackmd/pandoc.js

2 moderate severity vulnerabilities

Some issues need review, and may require choosing
a different dependency.
```