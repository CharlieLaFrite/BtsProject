<?php
session_start();

if ($_SESSION['admin'] == 2) {
    echo"<p class='band'>Vous devez etre administrateur pour visionner les logs</p>";
}

//conenxion à la base de données
$host = 'localhost';
$db = 'Linky';
$user = '';
$password = '';
$dsn = "mysql:host=$host;dbname=$db;charset=utf8mb4";

try {
    $pdo = new PDO($dsn, $user, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    die("erreur de connexion :" . $e->getMessage());
}

//Vérifie si le formulaire a été soumis
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $identifiant = $_POST['identifiant'];
    $mdp = $_POST['mdp'];

    //requete pour vérifier si l'utilisateur existe et est admin
    $sql = "SELECT * FROM Users WHERE identifiant = :identifiant AND mdp = :mdp AND admin = 1";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':identifiant', $identifiant);
    $stmt->bindParam(':mdp', $mdp);
    $stmt->execute();

    //vérifie si une ligne correspondante est trouvé
    if ($stmt->rowCount() > 0) {
        $_SESSION['admin'] = 1;
        header("Location: logs.php");
        exit;
    } else {
        //requete pour vérifier si l'utilisateur existe sans être admin
        $sql = "SELECT * FROM Users WHERE identifiant = :identifiant AND mdp = :mdp";
        $stmt = $pdo->prepare($sql);
        $stmt->bindParam(':identifiant', $identifiant);
        $stmt->bindParam(':mdp', $mdp);
        $stmt->execute();
        //vérifie si une ligne correspondante est trouvé
        if ($stmt->rowCount() > 0) {
            $_SESSION['admin'] = 2;
            header("Location: index.php");
        } else {
            echo "Identifiant ou mot de passe incorrecte";
        }
    }    
}


?>

<!-- Formulaire de connexion -->
<!DOCTYPE html>
<html>
    <head>
        <meta charset='utf8'>
        <title>Connexion</title>
        <link rel="stylesheet" href="style/styleLogin.css">
    </head>
    <body>
        <div id="formulaire">
            <h1>Connectez-Vous</h1>
            <form action="login.php" method="POST">
                <label for="identifiant">Identifiant :</label>
                <input type="text" id="identifiant" name="identifiant" required></br>

                <label for="mdp">Mot de passe : </label>
                <input type="password" id="mdp" name="mdp" required></br>

                <button type="submit">Connexion</button>
            </form>
            
        </div>
    </body>
</html>
