let range = document.getElementById("tensionSlider");
let tension = document.getElementById("tensionValue");
const socket = new WebSocket('ws://10.42.0.1:64510');

range.focus()

// Ouvrir la connexion
socket.addEventListener('open', (e) => {
    console.log('connected to the server');
});

range.addEventListener('input', () => {
    tension.textContent = range.value;
    socket.send(range.value);
});

// Ecouter les messages
socket.addEventListener('message', (e) => {
    console.log('message du serveur : ', e.data);
});

// gESTION ERREUR DE CONNEXION
socket.addEventListener('error', (e) => {
    console.log('error :', e);
});

// Gestion de la fermeture de session
socket.addEventListener('close', (e) => {
    console.log('connexion fermé : ', e);
    
})