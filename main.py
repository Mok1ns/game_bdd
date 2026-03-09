from db_init import get_db

def main_menu():
    print("+       ---BIENVENUE---   +")
    print("1 -      LANCER LE JEU")
    print("2 -      LEADERBOARD")
    print("3 -      QUITTER LE PROGRAMME")


def is_int(number, min_val, max_val):
    if not number.isnumeric():
        return False
    
    number = int(number)

    if number < min_val:
        return False
    
    if number > max_val:
        return False

    return True


def get_user_choice(text, min_val, max_val):
    while True:
        choice = input(text)
        if is_int(choice, min_val, max_val):
            return int(choice)
        print(f"Erreur : Veuillez choisir un nombre entre {min_val} et {max_val}")

def display_ranking():
    pass

def username_check(username):
    return len(username) > 0 and len(username) <= 20

def username_func():
    while True:
        username = input("Entrez votre nom d'utilisateur : ")
        if username_check(username):
            return username
        print("Erreur : le nom doit contenir entre 1 et 20 caractères.")

def is_team_full(team):
    return len(team) >= 3

def get_available_heroes (team, list_of_heroes): 
    available_heroes = []
    for hero in list_of_heroes:
        if hero not in team:
            available_heroes.append(hero)

    return available_heroes

def get_characters(db):
    characters = []
    for char in db.characters.find():
        characters.append({
            "name": char["nom"],
            "HP": char["PV"],
            "ATK": char["ATK"],
            "DEF": char["DEF"]
        })
    return characters

def display_available_heroes(available_heroes):
    print("\nHéros disponibles:")
    for idx, hero in enumerate(available_heroes):
        print(f"{idx + 1}. {hero['name']} (HP: {hero['HP']}, ATK: {hero['ATK']}, DEF: {hero['DEF']})")

def ask_hero_choice(available_heroes):
    choice = get_user_choice("Choisissez un héros (1-{}): ".format(len(available_heroes)), 1, len(available_heroes))
    return available_heroes[choice - 1]

def create_team(list_of_heroes):
    team = []
    while not is_team_full(team):
        available_heroes = get_available_heroes(team, list_of_heroes)
        display_available_heroes(available_heroes)
        hero = ask_hero_choice(available_heroes)
        team.append(hero)
    return team
 
def play_game(db):
    username = username_func()
    print(f"Username : {username}")

    characters = get_characters(db)

    team = create_team(characters)

    print("\nVotre équipe :")
    for hero in team:
        print(hero["name"])
   # score = combat(team)
   # display_score(score)
   # save_score(username, score)

def main():
    db = get_db()

    main_menu()
    choice = get_user_choice("Choisissez une option: ", 1, 3)

    if choice == 1:
        play_game(db)

    elif choice == 2:
        display_ranking()

    elif choice == 3:
        exit()


main()