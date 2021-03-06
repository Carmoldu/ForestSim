import GameCycle


if __name__ == "__main__":

    game = GameCycle.GameCycle()
    game.initialize_forest()

    while True:
        user_in = input("What do you want to do? "
                        "\n\t- [t] Advance one tick"
                        "\n\t- [m] Advance one month"
                        "\n\t- [y] Advance one year"
                        "\n\t- [p] Plot current population history"
                        "\n\t- [q] Quit")
        if user_in == "t":
            game.advance_to_next_tick()
        elif user_in == "m":
            game.advance_to_next_month()
        elif user_in == "y":
            game.advance_to_next_year()
        elif user_in == "p":
            game.plot_population_history()
        elif user_in == "q":
            break
        else:
            print("Input not accepted")

    game.plot_population_history()

