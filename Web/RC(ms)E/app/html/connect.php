<?php


$servername = "mysql";
$username = "examiner";
$password = 'SecurePassword1234560123456';
$dbname = "webapp";


$conn = mysqli_connect($servername, $username, $password, $dbname);

if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}



?> 