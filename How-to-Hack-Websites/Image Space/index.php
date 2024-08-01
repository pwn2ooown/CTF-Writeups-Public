<?php
if (isset($_GET['source'])) {
    highlight_file(__FILE__);
    exit;
}
?>
<h1>Image Uploader</h1>
<p>Only supports: jpg, jpeg, png</p>
<form action="index.php" method="POST" enctype="multipart/form-data">
    <input type="file" name="image_file">
    <input type="submit" value="Upload">
</form>
<p>
    <a href="/?source">View Source</a>
</p>
<?php
if (!isset($_FILES['image_file'])) {
    die('Give me a file!');
}

$filename = basename($_FILES['image_file']['name']);
$extension = strtolower(explode(".", $filename)[1]);

if (!in_array($extension, ['png', 'jpeg', 'jpg']) !== false) {
    die("Invalid file extension: $extension.");
}

// if (in_array($_FILES['image_file']['type'], ["image/png", "image/jpeg", "image/jpg"]) === false) {
//     die("Invalid file type: " . $_SERVER["CONTENT_TYPE"]);
// }

list($_, $_, $type) = getimagesize($_FILES['image_file']['tmp_name']);

var_dump(getimagesize($_FILES['image_file']['tmp_name']));

if ($type !== IMAGETYPE_JPEG && $type !== IMAGETYPE_PNG) {
    die("Invalid image type.");
}

$prefix = bin2hex(random_bytes(8));
move_uploaded_file($_FILES['image_file']['tmp_name'], "images/${prefix}_${filename}");
echo "<img src=\"/images/${prefix}_${filename}\">";
?>