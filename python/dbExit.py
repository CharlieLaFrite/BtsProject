import mysql.connector

def close_connexion():
    # Se connecte à la base de données et récupère la dernière entrée dans Logs
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="",
            password="",
            database="Linky"
        )
        cursor = conn.cursor()
        query = "INSERT INTO Logs (scenario) VALUES (-1)"
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as e:
        print(f"Erreur de connexion ou d'exécution de la requête : {e}")
        return None


