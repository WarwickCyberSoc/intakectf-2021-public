<?php
$pdo = new PDO('mysql:dbname=webapp;host=mysql', 'tutorial', 'secret');

$queryString = "SELECT * FROM products";

$query = $pdo->query($queryString);

$rows = $query->fetchAll();
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Netkit Store</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">

</head>
<body>
    <div class="container mt-4">
    <div class="row">
        <div class="col-10">
            <h1 class="mb-4">Viewing Products</h1>
        </div>        
        <div class="col-2 text-center">
            <a href="/login.php">Login</a>
        </div>
    </div>
        <hr>
        <table class="table">
            <thead>
                <tr>
                <th scope="col">Product Name</th>
                <th scope="col">Price</th>
                <th scope="col">Stock</th>
                </tr>
            </thead>
            <tbody>
                <?php

                foreach($rows as $product) {
                    ?>
                    <tr>
                        <th scope='row'><?=$product["name"]?></th>
                        <td>£<?=$product["price"]?></td>
                        <td><?=$product["stock"]?></td>
                    </tr>
                    <?php
                }

                ?>
            </tbody>
        </table>
    </div>
</body>
</html>