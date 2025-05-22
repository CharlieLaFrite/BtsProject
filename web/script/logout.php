<?php
session_start(); //récupère la session 
session_unset(); //supprime toutes les variables sesession
session_destroy(); //detruit la session

header('Location: ../login.php');
exit();
?>