class Game:
    def __init__(self, name):
        self._name = name
        self._score = {"Player1": 0, "Player2": 0}
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def _notify(self):
        for observer in self._observers:
            observer.update(self._name, self._score)

    def update_score(self, player, points):
        if player in self._score:
            self._score[player] += points
            print(f"Game '{self._name}': {player} scored {points} points. Current score: {self._score}")
            self._notify()
        else:
            print(f"Game '{self._name}': Invalid player '{player}'.")

class ScoreboardDisplay:
    def __init__(self, display_name):
        self._display_name = display_name

    def update(self, game_name, score):
        print(f"Scoreboard '{self._display_name}': {game_name} - P1: {score['Player1']}, P2: {score['Player2']}")

class HighScoreTracker:
    def __init__(self):
        self._high_score = 0
        self._high_scorer = None

    def update(self, game_name, score):
        current_max = max(score.values())
        if current_max > self._high_score:
            self._high_score = current_max
            for player, s in score.items():
                if s == current_max:
                    self._high_scorer = player
                    break
            print(f"High Score Tracker: New high score in {game_name} - {self._high_scorer} with {self._high_score} points!")

if __name__ == "__main__":
    football_game = Game("Championship Match")

    main_scoreboard = ScoreboardDisplay("Main Arena")
    tv_scoreboard = ScoreboardDisplay("TV Broadcast")
    high_score_tracker = HighScoreTracker()

    football_game.attach(main_scoreboard)
    football_game.attach(tv_scoreboard)
    football_game.attach(high_score_tracker)

    football_game.update_score("Player1", 3)
    football_game.update_score("Player2", 2)
    football_game.update_score("Player1", 7)
    football_game.update_score("Player2", 5)

    football_game.detach(tv_scoreboard)
    football_game.update_score("Player1", 1)