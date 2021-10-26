<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Netkit Store | Reviews</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">

</head>
<body>
    <div class="container mt-4">
        <h1 class="mb-4 text-center">Viewing Reviews</h1>
        <div class="row">
            <div class="col-4">
                <a href="/reviews.php?review=reviews/1" class="btn btn-primary w-100">Read Dave H's Review</a>
            </div>
            <div class="col-4">
                <a href="/reviews.php?review=reviews/2" class="btn btn-primary w-100">Read Steve L's Review</a>
            </div>
            <div class="col-4">
                <a href="/reviews.php?review=reviews/3" class="btn btn-primary w-100">Read Joesph D's Review</a>
            </div>
        </div>
        <hr>
        <?php
            if(isset($_GET["review"]))
            {
                include $_GET["review"] . ".php";
            }
        ?>
    </div>
</body>
</html>