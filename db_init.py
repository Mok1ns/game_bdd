from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://root:example@localhost:27018/")
DB_NAME = "game_db"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def get_db():
    return db

def insert_character():
    # Vérifier si les personnages existent déjà
    if db.characters.count_documents({}) > 0:
        print("Les personnages existent déjà dans la base de données.")
        return
    
    character = [
        {"nom": "Guerrier", "ATK": 15, "DEF": 10, "PV": 100},
        {"nom": "Mage", "ATK": 20, "DEF": 5, "PV": 80},
        {"nom": "Archer", "ATK": 18, "DEF": 7, "PV": 90},
    ]
    db.characters.insert_many(character)
    print("Personnages insérés avec succès!")

def insert_monster():
    # Vérifier si les monstres existent déjà
    if db.monsters.count_documents({}) > 0:
        print("Les monstres existent déjà dans la base de données.")
        return
    
    monster = [
        {"nom": "Gobelin", "ATK": 10, "DEF": 5, "PV": 50},
        {"nom": "Orc", "ATK": 20, "DEF": 8, "PV": 120},
        {"nom": "Dragon", "ATK": 35, "DEF": 20, "PV": 300},
    ]
    db.monsters.insert_many(monster)
    print("Monstres insérés avec succès!")

if __name__ == "__main__":
    try:
        insert_character()
        insert_monster()
        print("Base de données initialisée avec succès!")
    except Exception as e:
        print(f"Erreur lors de l'initialisation: {e}")