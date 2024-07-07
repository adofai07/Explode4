from type import Explode4
import copy

POS_WIN =  1_000_000
NEG_WIN = -1_000_000

def _p_s(g: Explode4) -> float:
    return sum(sum(i) for i in g.bd)

def _ev_1(g: Explode4) -> float:
    return _p_s(g)

def ev(g: Explode4) -> float:
    if g.is_game_over():
        if sum(sum(i) for i in g.bd) > 0:
            return POS_WIN
        
        else:
            return NEG_WIN
        
    return _ev_1(g)

def ev2(g: Explode4) -> float:
    if g.is_game_over():
        if sum(sum(i) for i in g.bd) > 0:
            return POS_WIN
        
        else:
            return NEG_WIN
        
    weights = [
        [2, 3, 4, 3, 2],
        [3, 5, 6, 5, 3],
        [4, 6, 9, 6, 4],
        [3, 5, 6, 5, 3],
        [2, 3, 4, 3, 2],
    ]
    
    s = 0
    
    for i in range(5):
        for j in range(5):
            s += g.bd[i][j] * weights[i][j]
            
    return s

def _adj_vals(x: int, y: int) -> float:
    d = {
        (1, 1): 2,
        (1, 2): 3,
        (1, 3): 4,
        (2, 2): 5,
        (2, 3): 6,
        (3, 3): 9,
        (1, -1): 0,
        (1, -2): 0,
        (1, -3): -3,
        (2, -2): 0,
        (2, -3): -11,
        (3, -3): 0,
    }
    
    if x == 0:
        return 0
    if y == 0:
        return 0
    
    if x > 0:
        if y > 0:
            return d[(min(x, y), max(x, y))]
        
        else:
            if abs(x) > abs(y):
                return d[(-y, -x)] * -1
        
            else:
                return d[(x, y)]
            
    else:
        if y > 0:
            if abs(x) < abs(y):
                return d[(-x, -y)] * -1
            
            else:
                return d[(y, x)]
            
        else:
            return d[(min(-x, -y), max(-x, -y))] * -1

def _ev3(g: Explode4) -> float:
    s = 0
    
    for i in range(4):
        for j in range(5):
            s += _adj_vals(g.bd[i][j], g.bd[i + 1][j])
            s += _adj_vals(g.bd[j][i], g.bd[j][i + 1])
            
    return s

def find_best_move(g: Explode4, evf: callable, depth: int, turn: int, all_moves: int=2) -> tuple[int, int]:
    if g.is_game_over():
        return None, evf(g)
    
    mv_ev_list = []
    depth_mv_ev_list = []
    
    g = copy.copy(g)
    
    if hasattr(g, "background"):
        setattr(g, "background", None)
    
    # print(depth, turn)
    
    if turn == 1:
        f = min
        
    if turn == -1:
        f = max
    
    if depth == 1:
        bmv = None
        bmv_eval = None

        for m in g.legal_moves():
            _g = copy.deepcopy(g)
            
            _g.move(*m)
            e = evf(_g)
            
            mv_ev_list.append((e, m))
            
            if bmv is None:
                bmv = m
                bmv_eval = e
                
            else:
                if f(e, bmv_eval) == e:
                    bmv = m
                    bmv_eval = e
                    
            # if bmv_eval == POS_WIN or bmv_eval == NEG_WIN:
            #     break
            
        mv_ev_list.sort(reverse=turn == -1)
        
        # print(mv_ev_list, turn)
        
        assert mv_ev_list[0][0] == bmv_eval
                    
        return bmv, bmv_eval
    
    else:
        bmv = None
        bmv_eval = None

        for m in g.legal_moves():
            _g = copy.deepcopy(g)
            
            _g.move(*m)
            # _, e = find_best_move(_g, evf, depth - 1, turn * -1)
            e = evf(_g)
            
            mv_ev_list.append((e, m))
            
            if bmv is None:
                bmv = m
                bmv_eval = e
                
            else:
                if bmv_eval is None:
                    print(g, depth)
                    
                if f(e, bmv_eval) == e:
                    bmv = m
                    bmv_eval = e
                    
            # if bmv_eval == POS_WIN or bmv_eval == NEG_WIN:
            #     break
        
        mv_ev_list.sort(reverse=turn == -1)
        
        for i in range(len(mv_ev_list) if all_moves > 0 else min(3, len(mv_ev_list))):
            _g = copy.deepcopy(g)
            
            _g.move(*mv_ev_list[i][1])
            _, e = find_best_move(_g, evf, depth - 1, turn * -1, all_moves - 1)
            
            depth_mv_ev_list.append((e, mv_ev_list[i][1]))
            
        depth_mv_ev_list.sort(reverse=turn == -1)
                    
        return depth_mv_ev_list[0][1], depth_mv_ev_list[0][0]
                
if __name__ == "__main__":
    # g = Explode4()
    # g.move(3, 3)
    # g.move(4, 4)
    
    # print(find_best_move(g, ev, 20))
    
    game = Explode4(use_pygame=True)
        
    while not game.is_game_over():
        game.update()
        
        mv, ev_n = find_best_move(game, ev2, 6, game._turn)
        
        print(F"Move: {mv}, Eval: {ev_n :+}")
        
        game.move(mv[0], mv[1])