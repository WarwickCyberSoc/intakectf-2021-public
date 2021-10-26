<?php
    session_start();

    $errorMessage = null;

    if(isset($_POST["username"]) && isset($_POST["password"]))
    {
        if (strcmp($_POST["username"], "admin") == 0 && strcmp($_POST["password"], "SuperSecurePasswordTheyWouldNeverGuess") == 0)
        {
            $_SESSION["isAdmin"] = true;
        }

        $errorMessage = "Invalid username or password";
    }

    if(isset($_SESSION["isAdmin"]) && $_SESSION["isAdmin"] === true)
    {
        header("Location: /admin.php");
        echo "Redirecting to admin page...";
        die();
    }
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Netkit Store | Login</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">

</head>
<body>
    <div class="container mt-4">
        <h1 class="mb-4 text-center">Login</h1>
        <?php
            if($errorMessage !== null)
            {
                ?>
                <div class="alert alert-danger">
                    <?= $errorMessage; ?>
                </div>
                <?php
            }
        ?>
        <form action="/login.php" method="POST">
            <div class="mb-3">
                <label class="form-label">Username</label>
                <input type="text" class="form-control" name="username">
            </div>
            <div class="mb-3">
                <label class="form-label">Password</label>
                <input type="password" class="form-control" name="password">
            </div>
            <button type="submit" class="btn btn-primary">Login</button>
        </form>
    </div>
</body>
</html>