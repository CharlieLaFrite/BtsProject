import subprocess

def get_ip():
    try:
        # Exécuter la commande pour obtenir l'adresse IP de l'interface wlan0
        result = subprocess.run(['hostname', '-I'], stdout=subprocess.PIPE)
        ipAddress = result.stdout.decode('utf-8').strip()
        return ipAddress
    except Exception as e:
        print(f"Erreur lors de la récupération de l'IP : {e}")
        return None
