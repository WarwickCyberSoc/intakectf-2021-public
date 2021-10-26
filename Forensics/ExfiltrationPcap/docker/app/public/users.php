<?php
error_reporting(5);
ini_set("display_errors", "on");
$pdo = new PDO('mysql:dbname=webapp;host=mysql', 'tutorial', 'secret');

$username = $_GET["username"];

// echo "SELECT * FROM users WHERE username='" . $username . "';  \n";

$query = $pdo->query("SELECT * FROM users WHERE username='" . $username . "';");

// echo "\n\n";
// print_r($pdo->errorInfo());

if(!$query)
    die("Something went wrong");
    
$row = $query->fetch();

// print_r($row);

if($row)
{
    die("User exists");
}
else
{
    die("User does not exist");
}


?>