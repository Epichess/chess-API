class Board:
    def __init__(self):
        self.fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
    
    def __str__(self) -> str:
        return self.fen

    def debug(self):
        print("DEBUG BOARD")