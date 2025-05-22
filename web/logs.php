<?php
session_start();

if ($_SESSION['admin'] != 1) {
    header("Location: login.php");
    exit;
}

// Connexion à la base de données
$host = 'localhost';
$db = 'Linky';
$user = 'charlie';
$password = 'root';
$dsn = "mysql:host=$host;dbname=$db;charset=utf8mb4";

try {
    $pdo = new PDO($dsn, $user, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    die("Erreur de connexion : " . $e->getMessage());
}

// Suppression des logs
if (isset($_POST['reset_logs'])) {
    $sql = "DELETE FROM Logs";
    $stmt = $pdo->prepare($sql);
    if ($stmt->execute()) {
    } else {
        echo "Une erreur est survenue lors de la suppression des logs.";
    }

    //réinitialise l'autoincrementation
    $sql = "ALTER TABLE Logs AUTO_INCREMENT = 1";
    $stmt = $pdo->prepare($sql);
    if ($stmt->execute()) {
    } else {
        echo "Une erreur est survenue lors de la suppression des logs.";
    }

    // Redirection vers la même page pour éviter la ré-exécution lors du rafraîchissement
    header('Location: logs.php');
    exit; // Assurez-vous que le script s'arrête ici après la redirection
}

// Récupérer les logs
$sql = "SELECT * FROM Logs ORDER BY id";
$stmt = $pdo->prepare($sql);
$stmt->execute();
$logs = $stmt->fetchAll(PDO::FETCH_ASSOC);
?>

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Logs</title>
    <link rel="stylesheet" href="style/styleLogs.css">
</head>
<body>
    <div class="head">
        <h1>Logs</h1>
        <div class="head">
            <form action="index.php" method="POST">
                <button type="submit">Aceuil</button>
            </form>
            <form method="POST" action="">
                <button type="submit" name="reset_logs">Reset</button>
            </form>
        </div>
    </div>

    <table>
        <tr>
            <th>id</th>
            <th>Scénario</th>
            <th>Date/Heure</th>
        </tr>
        <?php foreach ($logs as $log): ?>
        <tr>
            <td><?php echo htmlspecialchars($log['id']); ?></td>
            <td><?php echo htmlspecialchars($log['scenario']); ?></td>
            <td><?php echo htmlspecialchars($log['date_heure']); ?></td>
        </tr>
        <?php endforeach; ?>
    </table>

</body>
</html>
