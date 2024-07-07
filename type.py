import pygame
import copy

BD_SIZE = 5
SQ_SIZE = 80
RED = pygame.Color("#eb3734")
BLUE = pygame.Color("#343deb")
GRAY = pygame.Color("#454545")

C = [
    GRAY,
    RED, RED, RED, RED,
    BLUE, BLUE, BLUE, BLUE,
]

class Explode4:
    def __init__(self, bd_size: int=5, use_pygame: bool=False):
        self.n = 5
        self._turn = -1
        
        self.bd = [
            [0 for _ in range(self.n)]
            for _ in range(self.n)
        ]
        
        self.moves = 0
        self.use_pygame = use_pygame

        if self.use_pygame:
            pygame.init()

            pygame.display.set_caption("Explode4")
            self.background = pygame.display.set_mode((BD_SIZE * SQ_SIZE, BD_SIZE * SQ_SIZE))

            # self.background = pygame.Surface((BD_SIZE * SQ_SIZE, BD_SIZE * SQ_SIZE))
            self.background.fill(pygame.Color("#000000"))
        
    def turn(self):
        self._turn *= -1
        
        return self._turn
        
    def update(self):
        if self.use_pygame:
            for _ in pygame.event.get():
                ...
                
            self.background.fill(pygame.Color("#000000"))
            
            for i in range(1, self.n):
                pygame.draw.line(
                    self.background,
                    pygame.Color("#ffffff"),
                    (0, i * SQ_SIZE),
                    (self.n * SQ_SIZE, i * SQ_SIZE),
                    5
                )
                pygame.draw.line(
                    self.background,
                    pygame.Color("#ffffff"),
                    (i * SQ_SIZE, 0),
                    (i * SQ_SIZE, self.n * SQ_SIZE),
                    5
                )
                
            regfont = pygame.font.Font("FiraCode-Regular.ttf", 40)
            bldfont = pygame.font.Font("FiraCode-Bold.ttf", 40)
                
            for i in range(self.n):
                for j in range(self.n):
                    coord = (
                        round((j + 0.5) * SQ_SIZE),
                        round((i + 0.5) * SQ_SIZE),
                    )
                    font = bldfont if self.bd[i][j] else regfont
                    
                    text = font.render(str(abs(self.bd[i][j])), True, C[self.bd[i][j]])
                    text_rect = text.get_rect(center=coord)
                    self.background.blit(text, text_rect)
            
            pygame.display.update()
            
        else:
            print(self)
        
    def is_under_4(self):
        for i in range(self.n):
            for j in range(self.n):
                if not (-4 < self.bd[i][j] < 4):
                    return False
                
        return True
        
    def truncate(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.bd[i][j] > 4:
                    self.bd[i][j] = 4
                    
                if self.bd[i][j] < -4:
                    self.bd[i][j] = -4
                
        return True
        
    def is_game_over(self):
        if self.moves < 2:
            return False
        
        positive = 0
        negative = 0

        for i in range(self.n):
            for j in range(self.n):
                if self.bd[i][j] > 0:
                    positive = 1
                    
                if self.bd[i][j] < 0:
                    negative = 1
                    
        return positive + negative == 1
    
    def move(self, x: int, y: int, debug: bool=False):
        assert 0 <= x < self.n
        assert 0 <= y < self.n
        
        if   self.moves  == 0:
            self.bd[x][y] = self.turn() * 3
            
        elif self.moves == 1:
            assert self.bd[x][y] == 0
            self.bd[x][y] = self.turn() * 3
            
        else:
            assert self.bd[x][y] * self._turn < 0
            
            self.bd[x][y] += self.turn()
            
            if debug:
                print(str(self))
                print(self.is_under_4())
            
            while not self.is_under_4():
                self.truncate()
                tmp = copy.deepcopy(self.bd)
                
                for i in range(self.n):
                    for j in range(self.n):
                        if abs(self.bd[i][j]) == 4:
                            tmp[i][j] -= self.bd[i][j]
                            
                            for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                                ni = i + di
                                nj = j + dj

                                if 0 <= ni < self.n:
                                    if 0 <= nj < self.n:
                                        if tmp[ni][nj] * self._turn > 0:
                                            tmp[ni][nj] += self._turn

                                        else:
                                            tmp[ni][nj] *= -1
                                            tmp[ni][nj] += self._turn
                self.bd = tmp             
                self.truncate()
                                        
        self.moves += 1
        
    def legal_moves(self):
        if self.moves == 0:
            return [
                (i, j)
                for i in range(self.n)
                for j in range(self.n)
            ]
            
        elif self.moves == 1:
            return [
                (i, j)
                for i in range(self.n)
                for j in range(self.n)
                if not self.bd[i][j]
            ]
            
        else:
            return [
                (i, j)
                for i in range(self.n)
                for j in range(self.n)
                if self.bd[i][j] * self._turn < 0
            ]
        
    def __str__(self):
        ret = "-" * 10
        
        for i in self.bd:
            ret += "\n" + "".join(map(lambda x: F"{x :+02.0f} ", i))
            
        ret += "\n" + "-" * 10
        
        return ret
        
    def quit(self):
        if self.use_pygame:
            pygame.quit()
        
def evaluation(pos: Explode4) -> float:
    return sum(sum(i) for i in pos.bd)
        
if __name__ == "__main__":
    import time
    import random

    game = Explode4(use_pygame=True)
    
    is_game_over = False
    
    while not game.is_game_over():
        game.update()
        
        time.sleep(0.05)
        
        mv = random.choice(game.legal_moves())
        
        game.move(mv[0], mv[1])
        
        # print(F"Eval: {evaluation(game)}")
        # print(F"Valid moves: {game.valid_moves()}")
        # print(str(game))