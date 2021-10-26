<?php
    require_once "redis.php";
    session_start();

    function generateRandomString($length = 10) {
        $characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
        $charactersLength = strlen($characters);
        $randomString = '';
        for ($i = 0; $i < $length; $i++) {
            $randomString .= $characters[rand(0, $charactersLength - 1)];
        }
        return $randomString;
    }

    if(!isset($_SESSION["username"]))
    {
        header("Location: /login.php");
        die();
    }

    $success = false;
    
    if(isset($_POST["title"]) && isset($_POST["content"]))
    {
        $story = array(
            "title" => $_POST["title"],
            "story" => $_POST["content"],
            "author" => $_SESSION["username"]
        );

        $redis->set("draft_" . generateRandomString(32), json_encode($story));
        $success = true;
    }
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FanFix</title>
     <!-- Bootstrap core CSS -->
     <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">

</head>
<body>
<body class="py-4">
    
    <main>
      <div class="container">
    
        <a href="/"><h1 class="text-start mt-4">FanFix</h1></a>
        <h3 class="text-start mb-4">The best fan fiction website around.</h3>
        <a href="/logout.php">Logout</a>
        <hr>
        <h3>Featured FanFix:</h3>
        <div class="row">
            <div class="col-4">
                <a href="/post.php?id=featured_1">
                    <img src="/assets/fan.jpg" class="img-fluid" />
                    <h4>fan fiction innit</h4>
                </a>
            </div>
            <div class="col-4">
                <a href="/post.php?id=featured_2">
                    <img src="/assets/joe_biden.jpg" class="img-fluid" />
                    <h4>joe biden</h4>
                </a>
            </div>
            <div class="col-4">
                <a href="/post.php?id=featured_3">
                    <img src="/assets/gardener.jpg" class="img-fluid" />
                    <h4>angus the gardener VS. angus gardner</h4>
                </a>
            </div>
        </div>
        <hr>
        <h3 class="mb-4">Submit a story!</h3>
        <?php
            if($success)
            {
                ?>
                    <div class="alert alert-success">Your story draft has been saved and will be reviewed by an admin soon!</div>
                <?php
            }
        ?>

        <form method="POST" class="form">
            <div>
                <label class="form-label">Title</label>
                <input type="text" class="form-control" name="title" required placeholder="Name your story something exciting!">
            </div>
            <br>
            <div>
                <label class="form-label">Story</label>
                <textarea type="text" class="form-control" name="content" required placeholder="Your story goes here!"></textarea>
            </div>
            <br>
            <button class="btn btn-success">Upload story for admin review</button>
        </form> 
    </main>
</body>
</html>