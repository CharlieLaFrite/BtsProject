from gpiozero import Button, LED
from datetime import datetime
import websockets
import rgbScreen
import asyncio
import dbConn
import dbExit
import time
import ip

screen = 16
leftButton = Button(23)
rightButton = Button(22)
led = LED(27)
ledFrequence = 1.0
host = "0.0.0.0"
port = 64510
tension = 230

# Fonction asynchrone pour gérer la LED
async def clignoLed():
    global ledFrequence
    while True:
        led.on()
        await asyncio.sleep(0.1)
        led.off()
        await asyncio.sleep(ledFrequence)

async def handle_client(websockets):
    global tension
    print("client connecté")
    try:
        async for message in websockets:
            tension = int(message)
    except websockets.ConnectionClosed:
        print("connexion clos")

async def startServer():
    #creer et demare le server
    async with websockets.serve(handle_client, host, port):
        print("le serveur écoute")
        await asyncio.Future() #le maintient actif

class screenManager:
    def __init__(self):
        self.l1 = "http://"
        self.l2 = ip.get_ip()
        self.l3 = ""
        self.lastl1 = 0
        self.lastl2 = 0
    
    def update(self):
        if self.l1 != self.lastl1 or self.l2 != self.lastl2:
            rgbScreen.setText(f"{self.l1}\n{self.l2}")
        self.lastl1 = self.l1
        self.lastl2 = self.l2

class LinkySimulation:
    def __init__(self):
        try:
            self.currentScenario = dbConn.get_last_log()[1]
        except:
            self.currentScenario = -1
        self.screen = screenManager()
        self.scenarioListe = {
            "0": self.default,
            "1": self.scenario1,
            "2": self.scenario2
        }
        self.tension = 230
    
    async def checkTension(self, duration):
        startTime = time.time()
        while time.time() < (startTime + duration):
            if tension < 270:  # Utilisation de self.tension
                return False
            await asyncio.sleep(0.1)
        return True

    def checkScenario(self):
        try:
            temp = dbConn.get_last_log()[1]
            if self.currentScenario != temp:
                self.currentScenario = temp
                self.loadScenario(temp)
                return True
        except:
            return False

    def loadScenario(self, scenarioId):
        scenarioFunction = self.scenarioListe.get(scenarioId)
        if scenarioFunction:
            asyncio.create_task(scenarioFunction())

    async def default(self):
        pos = 0
        oldPos = 1
        conso = 13453
        puissanceA = 4248
        puissanceM = 4690
        puissanceS = 12
        puissanceC = 1000 * puissanceS
        prm = 19468306747877
        heure = datetime.now().strftime("%H:%M:%S")
        date = datetime.now().strftime("%d/%m/%y")
        indexDistributeur = 13153
        numeroDeSerie = "021875361258"
        indexInjection = 0
        registreErreur = "0000"
        screen = [
            [f"     {str(conso)} kWh  ", "  HEURE CREUSE ", "            *"],
            ["H PLEINE/CREUSE", " NOM DU CONTRAT", ""],
            [f"      {str(puissanceA)} VA", " PUIS APP SOUTIR", ""],
            [f"     {str(puissanceM)} VA", " PUIS MAX SOUTIR", ""],
            [f"        {str(puissanceS)} kVA", "   P SOUSCRITE", ""],
            [f"     {str(puissanceC)} VA", " PUISSANCE COUP ", ""],
            [f" {str(prm)}", " NUMERO DE PRM", ""],
            [f"  {str(heure)}", " HEURE COURANTE", ""],
            [f"  {str(date)}", "  DATE COURANTE", ""],
            ["    OUVERT", "   CONTACT SEC", ""],
            ["HISTORIQUE", "    MODE TIC", ""],
            [f"     {str(indexDistributeur)} kWh", "   HC  DISTRIB", ""],
            [f"  {str(numeroDeSerie)}", "  NUMERO SERIE", ""],
            [f"         {str(indexInjection)} kWh", " INDEX INJECTION", "            *"],
            [f"      {registreErreur}", " REGISTRE ERREUR", "            *"]
        ]
        numberOfScreen = len(screen) - 1

        while 1:
            self.screen.l1 = screen[pos][0]
            self.screen.l2 = screen[pos][1]
            self.screen.update()

            if leftButton.is_pressed:
                pos -= 1
                await asyncio.sleep(0.3)

            if rightButton.is_pressed:
                pos += 1
                await asyncio.sleep(0.3)

            if pos > numberOfScreen:
                pos = 0
            elif pos < 0:
                pos = numberOfScreen

            if self.checkScenario():
                break
            heure = datetime.now().strftime("%H:%M:%S")
            date = datetime.now().strftime("%d/%m/%y")

            await asyncio.sleep(0.1)

    async def scenario1(self):
        global tension
        self.screen.l1 = "     Tension"
        
        # Lancer la surveillance de surtension dans une tâche séparée
        async def monitor_surtension():
            global tension
            while True:
                is_overvoltage = await self.checkTension(5)
                if is_overvoltage:
                    print("Surtension détectée pendant 5 secondes !")
                    tension = 0
                await asyncio.sleep(0.1)
        asyncio.create_task(monitor_surtension())

        while 1:
            self.screen.l2 = f"       {tension}V"
            self.screen.update()
            await asyncio.sleep(0.1)
            if self.checkScenario():
                rgbScreen.setRGB(20, 20, 20)
                break
            if tension == 0:
                self.screen.l1 = "Breaker ouvert"
                rgbScreen.setRGB(20, 20, 20)
            elif tension < 160:
                self.screen.l1 = "Tension Faible !"
                rgbScreen.setRGB(1, 1, 30)
            elif 160 <= tension < 207:
                self.screen.l1 = "Excursion basse"
                rgbScreen.setRGB(10, 10, 50)
            elif 207 <= tension < 253:
                self.screen.l1 = "Tension normal"
                rgbScreen.setRGB(20, 20, 20)
            elif 253 <= tension < 270:
                self.screen.l1 = "Excursion haute"
                rgbScreen.setRGB(255, 105, 0)
            else:
                self.screen.l1 = "Surtension !"
                rgbScreen.setRGB(255, 10, 10)

    async def scenario2(self):
        self.screen.l1 = "Scenario 2"
        self.screen.l2 = "En cours ..."
        self.screen.update()

    async def run(self):
        print("Simulation Linky démarrée...")
        rgbScreen.setRGB(20, 20, 20)
        asyncio.create_task(clignoLed())
        try:
            while True:
                self.checkScenario()
                self.screen.update()
                await asyncio.sleep(0.1)
        except KeyboardInterrupt:
            dbExit.close_connexion()
            print("Fin de la simulation.")
