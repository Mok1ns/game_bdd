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
    # Faire des conditions pour verifier si le nombre est bien un integer avec des booleans 
    # Si ce n'est pas un nombre, on return False
    if not number.isnumeric():
        return False
    number = int(number)
    # Si le nombre est inferieur à la valeur minimale, on return False
    if number < min_val:
        return False
    # Si le nombre est superieur à la valeur maximale, on return False
    if number > max_val:
        return False
    # Sinon on retournera True si chaque condition n'ont pas été remplie.
    return True


def get_user_choice(text, min_val, max_val):
    print(f"------------------------------")
    # Tant que ce que l'utilisateur rentre un choix qui ne correspond pas, il va recommencer.
    while True:
        # demander a l'utilisateur de rentrer du texte
        choice = input(text)
        # Si c'est un nombre/integer, on retourne le choix mais converti en integer
        if is_int(choice, min_val, max_val):
            return int(choice)
        # Si il y'a erreur, on fait apparaitre un message d'erreur
        print(f"Erreur : Veuillez choisir un nombre entre {min_val} et {max_val}")


def display_ranking(db):
    print(f"\n꧁----------⎝ 𓆩༺✧ ༻𓆪⎠----------꧂")
    print(f"  ✧    ---LEADERBOARD---    ✧\n")
    # recuperer les scores dans la limite de 3 personnes max affiché
    scores = db.leaderboard.find().sort("score", -1).limit(3)
    rank = 1
    # Pour chaque entrée dans la db du score, on va affficher les 3 meilleurs.
    for entry in scores:
        print(f"      {rank}. {entry['username']} - {entry['score']} vague(s)")
        rank += 1
    print(f"\n------------------------------")
    time.sleep(1)



def username_check(username):
    # retourner un filtre si le username est inferieur à 0 ou supérieur à 20
    return len(username) > 0 and len(username) <= 20


def username_func():
    # Tant que l'utilisateur ne rentre pas un nom d'utilisateur correcte :
    while True:
        # on demande de rentrer un nom d'utilisateur à l'user
        username = input("Entrez votre nom d'utilisateur : ")
        # Si le username est valide 
        if username_check(username):
            # Retourne le username
            return username
        # si il ne passe pas le check, il printera un message d'erreur
        print("Erreur : le nom doit contenir entre 1 et 20 caractères.")


def is_team_full(team):
    # on retourne une verification de si la team est bien constituée de 3
    return len(team) >= 3





"""                                    ENTITÉS                                                     """



def get_available_heroes (team, list_of_heroes):
    # créer une liste vide pour les héros 
    available_heroes = []
    # Pour chaque hero dans la liste de heros
    for hero in list_of_heroes:
        # Si il n'est pas déjà dans l'équipe
        if hero not in team:
            # le rajouter si il ne l'est pas
            available_heroes.append(hero)
    # on retourne la liste
    return available_heroes


def get_characters(db):
    # faire une liste pour stocker les heros avec les caractéristiques 
    characters = []
    # Pour chaque héros dans la db, trouver les heros et les ajouter à la liste characters
    for char in db.characters.find():
        characters.append({
            "name": char["nom"],
            "HP": char["PV"],
            "ATK": char["ATK"],
            "DEF": char["DEF"]
        })
    # on retourne la liste
    return characters


def display_available_heroes(available_heroes):
    # afficher les héros disponibles avec leurs stats
    print("\nHéros disponibles:")
    # Pour chaque index et héros dans la liste disponnible des héros, on va print un par un avec son index
    for idx, hero in enumerate(available_heroes):
        print(f"{idx + 1}. {hero['name']} (HP: {hero['HP']}, ATK: {hero['ATK']}, DEF: {hero['DEF']})")


def ask_hero_choice(available_heroes):
    # demander à l'user de faire un choix en passant par une fonction qui va verifier que ca soit entre des limites
    choice = get_user_choice("Choisissez un héros (1-{}): ".format(len(available_heroes)), 1, len(available_heroes))
    # retourner avec le max un choix en moins (car le nombre décrémente avec le choix)
    return available_heroes[choice - 1]


def create_team(list_of_heroes):
    # faire une liste pour l'équipe et mettre les héros séléctionnés dedans tout en vérifiant
    team = []
    # tant que l'équipe n'est pas complète
    while not is_team_full(team):
        # on recupere les heros dispo
        available_heroes = get_available_heroes(team, list_of_heroes)
        # on affiche les heros dispo
        display_available_heroes(available_heroes)
        # demander le choix des heros
        hero = ask_hero_choice(available_heroes)
        # le rajouter à l'équipe
        team.append(hero)  
    # retourner la liste team
    return team
 

def generate_monster(db, wave):
    # prendre les monstres de la db et les convertir en liste
    monsters = list(db.monsters.find())
    # prendre un monstre aléatoire dans la liste de monstre 
    random_monster = random.choice(monsters)
    # on va attribuer les stats aux monstres qu'on à récupéré aléatoirement
    monster = {
        "name": random_monster["nom"],
        "HP": random_monster["PV"],
        "ATK": random_monster["ATK"],
        "DEF": random_monster["DEF"]
    }
    print(f"\nUn {monster['name']} apparaît !")
    print(f"HP: {monster['HP']} | ATK: {monster['ATK']} | DEF: {monster['DEF']}")
    # on retourne la liste de monstre 
    return monster


def calculate_team_damage(team, monster):
    # additionner toutes les stats d'attaque de l'équipe et la rendre en dégat
    total_atk = sum(hero["ATK"] for hero in team)
    # dégat par rapport au max défense de l'ennemi
    damage = max(1, total_atk - monster["DEF"])
    # on retourne les dégats
    return damage


def calculate_monster_damage(team, monster):
    # dégat par rapport à la moyenne de défense de l'équipe
    avg_def = sum(hero["DEF"] for hero in team) // len(team)
    # dégat par rapport à la défense moyenne de l'équipe
    damage = max(1, monster["ATK"] - avg_def)
    # on retourne les dégats
    return damage




"""                                 SYSTEME DE JEU                                                     """



def fight_rounds(team, monster, team_hp, monster_hp):
    # on return un relancement du tour en faisant appel à la fonciton de turn
    return fight_turn(team, monster, team_hp, monster_hp)


def fight_turn(team, monster, team_hp, monster_hp):
    # le tour de l'équipe et appel de la fonction pour connaitre les dégats de l'équipe
    damage_to_monster = calculate_team_damage(team, monster)
    # dégats qui seront soustrait par rapport aux dégats des monstres
    monster_hp -= damage_to_monster
    print(f"Votre équipe inflige {damage_to_monster} dégâts ! HP monstre restant : {max(monster_hp,0)}")
    time.sleep(0.25)
    # Si les hp du monstre tombent à 0
    if monster_hp <= 0:
        # on retourne les pv de l'équipe
        return team_hp, 0 
    # faire des pauses pour rendre plus animé
    time.sleep(0.5)
    # le tour des monstres et ses dégats qui seront soustrait par rapport aux dégats de l'équipe
    damage_to_team = calculate_monster_damage(team, monster)
    team_hp -= damage_to_team
    print(f"Le monstre inflige {damage_to_team} dégâts ! HP équipe restante : {max(team_hp,0)}")
    # on retourne les hp de deux camps
    return team_hp, monster_hp


def fight(team, monster, team_hp):
    # on récupere l'HP du monstre
    monster_hp = monster["HP"]
    print("\nCombat en cours ! ૮ ˙Ⱉ˙ ა rawr!")

    # Tant que les hp de l'équipe et du monstre sont supérieur à 0
    while team_hp > 0 and monster_hp > 0:
        # on va se battre
        team_hp, monster_hp = fight_rounds(team, monster, team_hp, monster_hp)

        # Si le monstre meurt 
        if monster_hp <= 0:
            print("\nVous avez vaincu le monstre ! ٩(^ᗜ^ )و ´-")
            # on retourne que les hp du monstre et continuer 
            return True, team_hp

        # Si l'équipe meurt
        if team_hp <= 0:
            print("Votre équipe a été vaincue ! (っ- ‸ - ς)")
            # on retourne False et les hp de l'équipe, fin de boucle
            return False, team_hp


def score(wave):
    # on retourne le nombre de wave - 1 pour calculer le nombre de wave finaux pour le score
    return wave - 1


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
    # Tant que la victoire est vraie on continue sinon on arrete la boucle 
    while True:
        print(f"\n\n+   VAGUE {wave}   +")
        # generer les monstres et prendre un aléatoire au début
        monster = generate_monster(db, wave)
        # commencer le fight en appelant sa fonction 
        victory, team_hp = fight(team, monster, team_hp)

        # Si victoire nous renvoie un false alors on rentre dans la condition
        if not victory:
            print(f"\nGame Over ! Vous avez survécu {wave - 1} vague(s). ദ്ദി(˵ •̀ ᴗ - ˵ ) ✧")
            # Score final qui sera le nombre de wave - 1
            score_final = score(wave)
            # on enregistre le score
            save_score(db, username,score_final)
            # on affiche le leaderboard
            display_ranking(db)
            time.sleep(1)
            # on arrete la boucle while true
            break
        
        # message de fin de wave et on incrémente le nombre de wave pour le score
        print(f"\n◝(ᵔᗜᵔ)◜ Vague {wave} terminée ! HP restants : {team_hp} ◝(ᵔᗜᵔ)◜")
        wave += 1
        time.sleep(1)

def play_game(db):
    # on demande un nom d'utilisateur
    username = username_func()
    print(f"Username : {username}")

    # récupérer les héros et créer l'équipe
    characters = get_characters(db)
    team = create_team(characters)

    # montrer l'équipe
    print("\nVotre équipe :")
    # Pour chaque héro dans l'équipe, on va print leurs noms
    for hero in team:
        print(hero["name"])

    # systeme de vague d'ennemie et tout le systeme de combat derriere
    wave(db,team,username)