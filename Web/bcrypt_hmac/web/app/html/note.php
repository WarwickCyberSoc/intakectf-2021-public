<?php
require_once "cookie.php";
require_once "random.php";

$pdo = new PDO('mysql:dbname=webapp;host=mysql', 'anon', 'P8e9spXP356&g5PK');

$notes = loadNotesFromCookie();

if(!isset($_GET["id"]))
{
    header("Location: /");
    die();
}

if(!in_array($_GET["id"], $notes, true))
{
    header("Location: /");
    die();
}

$query = $pdo->query("SELECT note FROM notes WHERE id = '" . $_GET["id"] ."'");

$row = $query->fetch();

if(!isset($row["note"]))
{
    header("Location: /");
    die();
}

$note = $row["note"];
?>

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>AnonNotes</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Permanent+Marker&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="/static/style.css" />
  </head>
  <body>
    <div id="container">
      <h1 class="title"><?php echo $_GET["id"]; ?></h1>
      <div>
        <p>
          <?php 
            echo htmlspecialchars($note, ENT_QUOTES, 'UTF-8'); 
          ?>
        </p>
      </div>
    </div>
  </body>
</html>
