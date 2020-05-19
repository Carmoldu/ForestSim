import GameCicle

if __name__ == "__main__":
    height = 20
    width = 20
    init_default_options = {"initial_percentage_lumberjacks": 0.01,
                            "initial_percentage_trees": 0.2,
                            "initial_percentage_bears": 0.0025}
    GameCicle.game_loop(height, width, init_default_options)
