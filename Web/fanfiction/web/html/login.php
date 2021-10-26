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
    $pwHash = $redis->get($_POST["username"]);

    if($pwHash === false)
    {
      $error = "Invalid username or password.";
    }
    else
    {
      if(password_verify($_POST["password"], $pwHash))
      {
        $_SESSION["username"] = $_POST["username"];
        
        header("Location: /");
        die();
      }
      else
      {
        $error = "Invalid username or password.";
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
        <h1 class="h3 mb-3 fw-normal">Please sign in</h1>
        
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

        <div class="checkbox mb-3">
          <label>
            <input type="checkbox" value="remember-me" > Remember me
          </label>
        </div>
        <a href="/register.php">Register</a><br><br>
        <button class="w-100 btn btn-lg btn-primary" type="submit">Sign in</button>
        <p class="mt-5 mb-3 text-muted">© 2021</p>
      </form>
    </main>
  </body>
</html>