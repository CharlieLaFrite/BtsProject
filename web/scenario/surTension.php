<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Surtenstion</title>
    <link rel="stylesheet" href="../style/styleSurtension.css">
    <script src="../script/scriptSurtension.js" defer></script>
</head>
<body>
    <?php include "../script/header.php"; ?>
    <main>
        <div id="tension">
                <label for="tensionSlider">Tension : <span id="tensionValue">230</span> V   </label>
            <input type="range" min="120" max="300" value="230" id="tensionSlider">
        </div>
        <div id="légende">
            <div id="Soustension">
                <div class="couleur" id="BleuFoncé"></div>
                <p class="texte">Excursion haute</p>
            </div>
            <div id="ExcursionBasse">
                <div class="couleur" id="Bleuclair"></div>
                <p class="texte">Excursion haute</p>
            </div>
            <div id="normal">
                <div class="couleur" id="bleuNormal"></div>
                <p class="texte">Excursion haute</p>
            </div>
            <div id="ExcursionHaute">
                <div class="couleur" id="jaune"></div>
                <p class="texte">Excursion haute</p>
            </div>
            <div id="Surtension">
                <div class="couleur" id="rouge"></div>
                <p class="texte">Surtension</p>
            </div>
        </div>
    </main>
</body>
</html>