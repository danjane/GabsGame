import sys

from game import Game


def main() -> None:
    landscape_seed = sys.argv[1] if len(sys.argv) > 1 else None
    game = Game(landscape_seed)
    game.run()


if __name__ == "__main__":
    main()
