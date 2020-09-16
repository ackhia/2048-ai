# author: Jonathan Few
# description: An AI to play 2048


from game import Board, Action
import numpy as np
import copy

SIMULATIONS = 100 # Number of simulations to run for each potential move
LOOK_AHEAD = 80 # Number of moves to look ahead
ACTIONS = {Action.UP: "Up", Action.RIGHT: "Right", Action.DOWN: "Down", Action.LEFT: "Left"}

def run_sim(board, first_action):
    board_copy = copy.deepcopy(board)
    if not board_copy.move(first_action): #If we can't move in this direction, no point in running the sim
        return 0

    for i in range(LOOK_AHEAD):
        if board_copy.completed():
            break
        board_copy.move(np.random.randint(min(ACTIONS), max(ACTIONS)+1))

    return board_copy.average_score()

def run():
    score_totals = {}
    
    board = Board(4)

    while not board.completed():        
        for action in ACTIONS.keys():
            sim_scores = []
            for i in range(SIMULATIONS):
                sim_result = run_sim(board, action)
                sim_scores.append(sim_result)
            
            score_totals[action] = np.mean(sim_scores)

        move = max(score_totals, key=score_totals.get)
        board.move(move)
        board.paint()
        print(f"Last move: {ACTIONS[move]}")
        print(f"Score: {board.score()}")

    print(f"Average score: {board.average_score()}")
    print(f"Final score: {board.score()}")

    board.paint()

if __name__ == "__main__":
    run()