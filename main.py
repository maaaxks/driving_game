from direct.showbase.ShowBase import loadPrcFile
loadPrcFile("config.prc")
from src.game import DrivingGame

def main():
    game = DrivingGame()
    game.run()

if __name__ == "__main__":
    main()