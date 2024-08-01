<?php
require('config.php');

if($_GET['show_source'] === '1') {
    highlight_file(__FILE__);
    exit;
}

if($_POST['name'] === 'admin') {
    if($_POST['password'] !== $password) {
        // show failed message if you input wrong password
        header('Location: ./?failed=1');
    }
}
?><!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Login As Admin 4</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="/bootstrap/css/bootstrap.min.css" media="all">
</head>
<body>
    <div class="jumbotron">
        <div class="container">
            <h1>Login as Admin 4</h1>
        </div>
    </div>

    <div class="container">
        <div class="navbar">
            <div class="container-fluid">
                <div class="navbar-header">
                    <a class="navbar-brand" href="/">Please Hack Me</a>
                </div>
                <ul class="nav navbar-nav">
                    <li>
                        <a href="/scoreboard">Scoreboard</a>
                    </li>
                    <li>
                        <a href="?show_source=1" target="_blank">Source Code</a>
                    </li>
                </ul>
            </div>
        </div>
    </div>

    <div class="container">
        <div class="col-md-6 col-md-offset-3">
<?php if($_GET['failed'] == '1'): ?>
            <div class="alert alert-danger">Login failed</div>
<?php endif; ?>

<?php if($_POST['name'] === 'admin'): /* login success! */ ?>
            <div class="alert alert-success"><code><?=$flag?></code></div>
<?php else: ?>
            <form action="." method="POST">
                <div class="form-group">
                    <label for="name">User:</label>
                    <input id="name" class="form-control" type="text" name="name" placeholder="User">
                </div>
                <div class="form-group">
                    <label for="password">Pass:</label>
                    <input id="password" class="form-control" type="text" name="password" placeholder="Password">
                </div>
                <div class="form-group">
                    <input class="form-control btn btn-primary" type="submit" value="Login">
                </div>
            </form>
<?php endif; ?>
        </div>
    </div>
</body>
</html>