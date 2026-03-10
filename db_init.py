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
    # supprimer les anciens pour laisser place à la nouvelle liste
    db.characters.delete_many({})
    print("Anciens personnages supprimés.")
    
    character = [
        {"nom": "Guerrier", "ATK": 15, "DEF": 10, "PV": 100},
        {"nom": "Mage", "ATK": 20, "DEF": 5, "PV": 80},
        {"nom": "Archer", "ATK": 18, "DEF": 7, "PV": 90},
        {"nom": "Chevalier", "ATK": 18, "DEF": 12, "PV": 100},
        {"nom": "Roi Arthur", "ATK": 35, "DEF": 15, "PV": 140},
        {"nom": "Gilgamesh", "ATK": 25, "DEF": 9, "PV": 95},
        {"nom": "Berserker", "ATK": 15, "DEF": 25, "PV": 150},
    ]
    db.characters.insert_many(character)
    print("Personnages insérés avec succès!")

def insert_monster():
    # supprimer les anciens pour laisser place à la nouvelle liste
    db.monsters.delete_many({})
    print("Anciens monstres supprimés.")
    
    monster = [
        {"nom": "Gobelin", "ATK": 10, "DEF": 5, "PV": 50},
        {"nom": "Orc", "ATK": 20, "DEF": 8, "PV": 120},
        {"nom": "Dragon", "ATK": 35, "DEF": 20, "PV": 300},
        {"nom": "Rayan", "ATK": 45, "DEF": 25, "PV": 350},
        {"nom": "Hydra", "ATK": 40, "DEF": 22, "PV": 320},
        {"nom": "Serpent", "ATK": 9, "DEF": 7, "PV": 30},
        {"nom": "Sorcière", "ATK": 25, "DEF": 10, "PV": 100},
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