import mysql.connector

def get_last_log():
    # Se connecte à la base de données et récupère la dernière entrée dans Logs
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user=",
            password="",
            database="Linky"
        )
        cursor = conn.cursor()
        query = "SELECT * FROM Logs ORDER BY id DESC LIMIT 1"
        cursor.execute(query)
        last_row = cursor.fetchone()
        cursor.close()
        conn.close()
        return last_row
    except mysql.connector.Error as e:
        print(f"Erreur de connexion ou d'exécution de la requête : {e}")
        return None
