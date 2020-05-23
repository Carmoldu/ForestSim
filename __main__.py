import SimulationCycle


if __name__ == "__main__":

    simulation = SimulationCycle.SimulationCycle()
    simulation.initialize_forest()

    while True:
        user_in = input("What do you want to do? "
                        "\n\t- [t] Advance one tick"
                        "\n\t- [m] Advance one month"
                        "\n\t- [y] Advance one year"
                        "\n\t- [p] Plot current population history"
                        "\n\t- [q] Quit")
        if user_in == "t":
            simulation.advance_to_next_tick()
        elif user_in == "m":
            simulation.advance_to_next_month()
        elif user_in == "y":
            simulation.advance_to_next_year()
        elif user_in == "p":
            simulation.plot_population_history()
        elif user_in == "q":
            break
        else:
            print("Input not accepted")

    simulation.plot_population_history()

