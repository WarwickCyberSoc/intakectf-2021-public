<?php
  require_once "redis.php";
  session_start();

  if(isset($_SESSION["username"]))
  {
    header("Location: /");
    die();
  }

  $error = "";

  if(isset($_POST["username"]) && isset($_POST["password"]))
  {
    if(strlen($_POST["username"]) < 3 || strlen($_POST["username"]) > 56)
    {
      $error = "Username must be between 3 and 56 characters.";
    }

    if(strlen($_POST["password"]) < 3 || strlen($_POST["password"]) > 56)
    {
      $error = "Password must be between 3 and 56 characters.";
    }

    if(!$error)
    {
      $pwHash = $redis->get($_POST["username"]);

      if($pwHash !== false)
      {
        $error = "This user already exists.";
      }
      else
      {
        $redis->set($_POST["username"], password_hash($_POST["password"], PASSWORD_DEFAULT));
  
        $_SESSION["username"] = $_POST["username"];
      
        header("Location: /");
        die();
      }
    }
  }
?>
<html lang="en"><head>
    <meta charset="utf-8">
    <title>FanFix</title>

     <!-- Bootstrap core CSS -->
     <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">

    <style>
      .bd-placeholder-img {
        font-size: 1.125rem;
        text-anchor: middle;
        -webkit-user-select: none;
        -moz-user-select: none;
        user-select: none;
      }

      @media (min-width: 768px) {
        .bd-placeholder-img-lg {
          font-size: 3.5rem;
        }
      }
    </style>

    
    <!-- Custom styles for this template -->
    <link href="/css/signin.css" rel="stylesheet">
  </head>
  <body class="text-center">
    
    <main class="form-signin">
      <form  data-form-type="login" method="POST">
        <h1 class="h3 mb-3 fw-normal">Please register</h1>
        
        <?php 
          if($error)
          {
            ?>
              <div class="alert alert-danger"><?php echo $error; ?></div>
            <?
          }
        ?>

        <div class="form-floating">
          <input type="text" class="form-control" id="floatingInput" name="username" placeholder="Admin">
          <label for="floatingInput">Username</label>
        </div>
        <div class="form-floating">
          <input type="password" class="form-control" id="floatingPassword" name="password" placeholder="Password">
          <label for="floatingPassword">Password</label>
        </div>

        <a href="/login.php">Login</a><br><br>
        <button class="w-100 btn btn-lg btn-primary" type="submit">Register</button>
        <p class="mt-5 mb-3 text-muted">© 2021</p>
      </form>
    </main>
  </body>
</html>