<?php
session_start();
if (!isset($_SESSION['admin'])) {
    header('Location: login.php');
}

if (isset($_POST['submit'])) {
    // Connexion à la base de données
    $host = 'localhost';
    $db = 'Linky';
    $user = 'charlie';
    $password = 'root';
    $dsn = "mysql:host=$host;dbname=$db";

    try {
        $dbco = new PDO($dsn, $user, $password);
        $dbco->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    } 
    catch(PDOException $e) {
        echo "Erreur : " . $e->getMessage();
    }

    $sth = $dbco->prepare("INSERT INTO Logs (scenario) VALUES (:scenario)");
    $sth->bindParam(':scenario', $_POST['submit']);
    $sth->execute();

    // Redirection vers la même page pour éviter la ré-exécution lors du rafraîchissement
    switch ($_POST['submit']){
        case "0":
            header('Location: scenario/defaut.php');
            break;
        case "1":
            header('Location: scenario/surTension.php');
            break;
        default:
            header('Location: index.php');
    }
    
    exit; // Assure que le script s'arrête ici après la redirection
}

?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Simulation Linky</title>
    <link rel="stylesheet" href="style/style.css">
    <script src="script/script.js"></script>
</head>
<body>
    <?php include 'script/header.php'; ?>
    
    <form action="index.php" method="POST">
        <button class="men" type="submit" name="submit" value="0">Défaut</button>
        <button class="men" type="submit" name="submit" value="1">Surtension</button>
        <button class="men" type="submit" name="submit" value="2">Scenario 2</button>
    </form>
</body>
</html>
