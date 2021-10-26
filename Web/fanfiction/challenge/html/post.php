<?php
    require_once "redis.php";
    session_start();

    if(!isset($_SESSION["username"]) && $_SERVER["REMOTE_ADDR"] !== "127.0.0.1")
    {
        header("Location: /login.php");
        die();
    }

    if(!isset($_GET["id"]))
    {
        header("Location: /");
        die();
    }

    $id = $_GET["id"];

    $story = $redis->get($id);
    if($story === false)
    {
        header("Location: /");
        die();
    }
    
    $story = json_decode($story, false);
?>

<html lang="en"><head>
    <meta charset="utf-8">
    <title>FanFix</title>

     <!-- Bootstrap core CSS -->
     <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">

    </head>
    <main>
      <div class="container">
    
        <a href="/"><h1 class="text-start mt-4">FanFix</h1></a>
        <h3 class="text-start mb-4">The best fan fiction website around.</h3>
        <hr>
        <h3><?php echo strip_tags($story->title); ?></h3>
        <h4>Written by <?php echo $story->author; ?></h4>
        <p style="white-space: pre-wrap;"><?php echo strip_tags($story->story); ?></p>
    </main>
</body>
</html>