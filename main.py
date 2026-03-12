from db_init import get_db
from game import main_menu, get_user_choice, play_game, display_ranking


"""                                    MAIN                                                     """

def main():
    while True:
        db = get_db()
        # menu principal
        main_menu()
        # choix de l'utilisateur
        choice = get_user_choice("Choisissez une option: ", 1, 3)
        print("------------------------------")
        # Si choix 1 : on lance le jeu
        if choice == 1:
            play_game(db)
        # Si choix 2 : on montre le leaderboard
        elif choice == 2:
            display_ranking(db)
        # Si choix 3 : on quitte le programme
        elif choice == 3:
            exit()

if __name__ == "__main__":
    main()