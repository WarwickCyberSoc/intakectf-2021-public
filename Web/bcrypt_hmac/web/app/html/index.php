<?php
require_once "cookie.php";
require_once "random.php";

$pdo = new PDO('mysql:dbname=webapp;host=mysql', 'anon', 'P8e9spXP356&g5PK');

$notes = loadNotesFromCookie();

if(isset($_POST["note"]) && $_POST["note"] !== "")
{
  $id = random_str(10);

  try{
    $stmt = $pdo->prepare("INSERT INTO notes (id, note) VALUES (:id, :note);");
    $stmt->bindParam(":id", $id);
    $stmt->bindParam(":note", $_POST["note"]);

    $stmt->execute();
  } catch (PDOException $e) {
    echo "Something went wrong...";
    die();
  }

  array_unshift($notes, $id);
  saveNotesToCookie($notes);
  header("Location: /");
  die();
}

// $queryString = "SELECT * FROM products";

// $query = $pdo->query($queryString);

// $rows = $query->fetchAll();
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
      <h1 class="title">Anonymous Notes</h1>
      <h3 class="title">Your notes:</h3>
      <div>      
        <?php
          foreach($notes as $note)
          {
            echo "<a href='/note.php?id=" . $note . "'>" . $note . "</a> "; 
          }
        ?>
      </div>
      <br>
      <form action="/" method="POST" style="text-align: center">
        <textarea name="note" placeholder="Write here..." style="width: 100%; height: 500px"></textarea>
        <button type="submit" class="submit-button">Submit</button>
      </form>
    </div>
  </body>
</html>
