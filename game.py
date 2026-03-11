from db_init import get_db
import random
import time


"""                                    MENU                                                     """

def main_menu():
    print(f"\n꧁----------⎝ 𓆩༺✧ ༻𓆪⎠----------꧂")
    print("  ✦     ---BIENVENUE---      ✦")
    print("1 -      LANCER LE JEU       - ")
    print("2 -       LEADERBOARD        - ")
    print("3 -   QUITTER LE PROGRAMME   - ")


def is_int(number, min_val, max_val):
    # verifier si c'est est un nombre
    if not number.isnumeric():
        return False
    number = int(number)
    # faire une condition pour comparer le nombre aux valeurs max et min
    if number < min_val:
        return False
    if number > max_val:
        return False
    return True


def get_user_choice(text, min_val, max_val):
    print(f"------------------------------")
    while True:
        choice = input(text)
        # on doit verifier si c'est un nombre et ses filtres
        if is_int(choice, min_val, max_val):
            return int(choice)
        # message d'erreur
        print(f"Erreur : Veuillez choisir un nombre entre {min_val} et {max_val}")


def display_ranking(db):
    print(f"\n꧁----------⎝ 𓆩༺✧ ༻𓆪⎠----------꧂")
    print(f"  ✦    ---LEADERBOARD---    ✦\n")
    # recuperer les scores dans la limite de 3 personnes max affiché
    scores = db.leaderboard.find().sort("score", -1).limit(3)
    rank = 1
    # boucle pour afficher
    for entry in scores:
        print(f"      {rank}. {entry['username']} - {entry['score']} vague(s)")
        rank += 1
    print(f"\n------------------------------")
    time.sleep(1)



def username_check(username):
    # filtrer si le username est inferieur à 0 ou supérieur à 20
    return len(username) > 0 and len(username) <= 20


def username_func():
    # demander le nom d'utilisateur et faire une boucle pour qu'elle recommence jusqu'a qu'il soit bon
    while True:
        username = input("Entrez votre nom d'utilisateur : ")
        # voir si le username est valide 
        if username_check(username):
            # on retourne le username
            return username
        print("Erreur : le nom doit contenir entre 1 et 20 caractères.")


def is_team_full(team):
    # verifier si la team est bien constituée de 3
    return len(team) >= 3




"""                                    ENTITÉS                                                     """

def get_available_heroes (team, list_of_heroes): 
    available_heroes = []
    # rajouter chaque hero dans la liste
    for hero in list_of_heroes:
        # verifier qu'il n'est pas déjà dans l'équipe
        if hero not in team:
            # le rajouter si il ne l'est pas
            available_heroes.append(hero)

    return available_heroes


def get_characters(db):
    # faire une liste pour stocker les heros avec les caractéristiques 
    characters = []
    # trouver les heros et les ajouter à la liste characters
    for char in db.characters.find():
        characters.append({
            "name": char["nom"],
            "HP": char["PV"],
            "ATK": char["ATK"],
            "DEF": char["DEF"]
        })
    return characters


def display_available_heroes(available_heroes):
    # afficher les héros disponibles avec leurs stats
    print("\nHéros disponibles:")
    # énumerer chaque héros avec une boucle pour chacun
    for idx, hero in enumerate(available_heroes):
        print(f"{idx + 1}. {hero['name']} (HP: {hero['HP']}, ATK: {hero['ATK']}, DEF: {hero['DEF']})")


def ask_hero_choice(available_heroes):
    # créer un moyen de choisir ses heros dans les limites du nombre de héros
    choice = get_user_choice("Choisissez un héros (1-{}): ".format(len(available_heroes)), 1, len(available_heroes))
    # retourner avec le max un choix en moins
    return available_heroes[choice - 1]


def create_team(list_of_heroes):
    # faire une liste pour l'équipe et mettre les héros séléctionnés dedans tout en vérifiant
    team = []
    while not is_team_full(team):
        # recuperer les heros dispo
        available_heroes = get_available_heroes(team, list_of_heroes)
        # afficher les heros dispo
        display_available_heroes(available_heroes)
        # demander le choix des heros
        hero = ask_hero_choice(available_heroes)
        # le rajouter 
        team.append(hero)  
    # retourner l'équipe
    return team
 

def generate_monster(db, wave):
    # générer les monstres et les afficher. Il faut que ca prenne random dans la liste des monstres 
    monsters = list(db.monsters.find())
    # prendre un random monster
    momonster = random.choice(monsters)
    monster = {
        "name": momonster["nom"],
        "HP": momonster["PV"],
        "ATK": momonster["ATK"],
        "DEF": momonster["DEF"]
    }
    print(f"\nUn {monster['name']} apparaît !")
    print(f"HP: {monster['HP']} | ATK: {monster['ATK']} | DEF: {monster['DEF']}")
    return monster


def calculate_team_damage(team, monster):
    # additionner toutes les stats d'attaque de l'équipe et la rendre en dégat
    total_atk = sum(hero["ATK"] for hero in team)
    damage = max(1, total_atk - monster["DEF"])
    return damage


def calculate_monster_damage(team, monster):
    # dégat par rapport à la moyenne de défense de l'équipe
    avg_def = sum(hero["DEF"] for hero in team) // len(team)
    damage = max(1, monster["ATK"] - avg_def)
    return damage




"""                                 SYSTEME DE JEU                                                     """

def fight_rounds(team, monster, team_hp, monster_hp):
    # relancer le tour tant que la condition de la fonction précedente est
    return fight_turn(team, monster, team_hp, monster_hp)


def fight_turn(team, monster, team_hp, monster_hp):
    # le tour de l'équipe et ses dégats qui seront soustrait par rapport aux dégats des monstres
    damage_to_monster = calculate_team_damage(team, monster)
    monster_hp -= damage_to_monster
    print(f"Votre équipe inflige {damage_to_monster} dégâts ! HP monstre restant : {max(monster_hp,0)}")
    if monster_hp <= 0:
        return team_hp, 0 
    # faire des pauses pour rendre plus animé
    time.sleep(0.5)
    # le tour des monstres et ses dégats qui seront soustrait par rapport aux dégats de l'équipe
    damage_to_team = calculate_monster_damage(team, monster)
    team_hp -= damage_to_team
    print(f"Le monstre inflige {damage_to_team} dégâts ! HP équipe restante : {max(team_hp,0)}")
    return team_hp, monster_hp


def fight(team, monster, team_hp):
    # on récupere l'HP du monstre
    monster_hp = monster["HP"]
    print("\nCombat en cours !")

    # faire une boucle pour vérifier la continuation des combats par rapport aux hps
    while team_hp > 0 and monster_hp > 0:
        team_hp, monster_hp = fight_rounds(team, monster, team_hp, monster_hp)

        # condition quand on a tué un monstre
        if monster_hp <= 0:
            print("Vous avez vaincu le monstre !")
            return True, team_hp

        # condition quand on a perdu
        if team_hp <= 0:
            print("Votre équipe a été vaincue !")
            return False, team_hp


def score(wave):
    return wave -1


def save_score(db, username, score_final):
    # inserer le username et son score dans la db
    score_data = {
        "username": username,
        "score": score_final,
    }

    # Insérer dans la collection leaderboard
    db.leaderboard.insert_one(score_data)
    print(f"Score de {username} sauvegardé : {score_final} vague(s)")
    

def wave(db, team, username):
    wave = 1
    # additionner tous les hp de l'équipe pour donner l'hp de l'équipe
    team_hp = sum(hero["HP"] for hero in team)
    while True:
        print(f"\n\n+   VAGUE {wave}   +")
        # generer les monstres et prendre un aléatoire au début
        monster = generate_monster(db, wave)
        # commencer le fight
        victory, team_hp = fight(team, monster, team_hp)

        # condition si perte et donc fin de jeu avec son score
        if not victory:
            print(f"\nGame Over ! Vous avez survécu {wave - 1} vague(s).")
            score_final = score(wave)
            # on enregistre le score
            save_score(db, username,score_final)
            # on affiche le leaderboard
            display_ranking(db)
            time.sleep(1)
            break

        print(f"\nVague {wave} terminée ! HP restants : {team_hp}")
        wave += 1

def play_game(db):
    # on demande un nom d'utilisateur
    username = username_func()
    print(f"Username : {username}")

    # récupérer les héros et créer l'équipe
    characters = get_characters(db)
    team = create_team(characters)

    # montrer l'équipe
    print("\nVotre équipe :")
    for hero in team:
        print(hero["name"])

    # systeme de vague d'ennemie
    wave(db,team,username)