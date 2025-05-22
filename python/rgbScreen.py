import time
import sys
import smbus
import RPi.GPIO as GPIO

# Initialisation du bus I2C
try:
    bus = smbus.SMBus(1)  # Utilisez le bus 1 pour Raspberry Pi moderne
except FileNotFoundError:
    print("Erreur : Impossible d'accéder au bus I2C 1. Vérifiez les paramètres I2C.")
    sys.exit(1)

# Adresses I2C détectées
DISPLAY_RGB_ADDR = 0x62  # Rétroéclairage RGB
DISPLAY_TEXT_ADDR = 0x3e  # Affichage texte

# Définir le rétroéclairage (R,G,B) avec des valeurs entre 0 et 255
def setRGB(r, g, b):
    try:
        bus.write_byte_data(DISPLAY_RGB_ADDR, 0, 0)
        bus.write_byte_data(DISPLAY_RGB_ADDR, 1, 0)
        bus.write_byte_data(DISPLAY_RGB_ADDR, 0x08, 0xaa)
        bus.write_byte_data(DISPLAY_RGB_ADDR, 4, r)
        bus.write_byte_data(DISPLAY_RGB_ADDR, 3, g)
        bus.write_byte_data(DISPLAY_RGB_ADDR, 2, b)
    except IOError:
        print("Erreur : Impossible de configurer le rétroéclairage RGB.")

# Envoyer une commande au module texte
def textCommand(cmd):
    try:
        bus.write_byte_data(DISPLAY_TEXT_ADDR, 0x80, cmd)
    except IOError:
        print("Erreur : Impossible d'envoyer une commande texte à l'écran.")

# Afficher du texte sur l'écran LCD
def setText(text):
    textCommand(0x01)  # Effacer l'affichage
    time.sleep(0.05)
    textCommand(0x08 | 0x04)  # Afficher sans curseur
    textCommand(0x28)  # Mode 2 lignes
    time.sleep(0.05)

    count = 0
    row = 0
    for c in text:
        if c == '\n' or count == 16:
            count = 0
            row += 1
            if row == 2:
                break
            textCommand(0xc0)  # Se déplacer à la 2e ligne
            if c == '\n':
                continue
        count += 1
        try:
            bus.write_byte_data(DISPLAY_TEXT_ADDR, 0x40, ord(c))
        except IOError:
            print("Erreur : Impossible d'écrire sur l'écran LCD.")

# Mettre à jour le texte sans effacer l'écran
def setText_norefresh(text):
    textCommand(0x02)  # Retourner à la position d'origine
    time.sleep(0.05)
    textCommand(0x08 | 0x04)
    textCommand(0x28)
    time.sleep(0.05)

    count = 0
    row = 0
    text = text.ljust(32)  # Remplir avec des espaces jusqu'à 32 caractères
    for c in text:
        if c == '\n' or count == 16:
            count = 0
            row += 1
            if row == 2:
                break
            textCommand(0xc0)
            if c == '\n':
                continue
        count += 1
        try:
            bus.write_byte_data(DISPLAY_TEXT_ADDR, 0x40, ord(c))
        except IOError:
            print("Erreur : Impossible d'écrire sur l'écran LCD.")
