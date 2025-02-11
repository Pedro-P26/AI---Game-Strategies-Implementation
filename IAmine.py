from asyncio import PriorityQueue

from random import randint, choice

from games.minesweeper.action import MinesweeperAction
from games.minesweeper.player import MinesweeperPlayer
from games.minesweeper.state import MinesweeperState
from games.state import State

from games.minesweeper.result import MinesweeperResult
from games.minesweeper.simulator import MinesweeperSimulator

class IAMinesweeperPlayer(MinesweeperPlayer):

    def __init__(self, name):
        super().__init__(name)

    def heuristic(self, state, action):
        # Heurística avalia o risco de escolher uma ação baseado nas informações das células adjacentes
        row, col = action.get_row(), action.get_col()
        grid = state.get_grid()
        if grid[row][col] != MinesweeperState.EMPTY_CELL:
            return float('inf')  # Célula já revelada, custo infinito
        mine_indicators = 0
        for drow in (-1, 0, 1):
            for dcol in (-1, 0, 1):
                if 0 <= row + drow < state.get_num_rows() and 0 <= col + dcol < state.get_num_cols():
                    if grid[row + drow][col + dcol] > 0:
                        mine_indicators += grid[row + drow][col + dcol]
        return mine_indicators

    def get_action(self, state: MinesweeperState):
        possible_actions = list(state.get_possible_actions())
        open_list = PriorityQueue()
        for action in possible_actions:
            h_cost = self.heuristic(state, action)
            open_list.put((h_cost, action))

        # Assegure-se que a lista de prioridades não está vazia antes de obter um elemento
        if not open_list.empty():
            return open_list.get()[1]  # para acessar o objeto action no tuplo
        else:
            # Caso não haja ações válidas, retorne uma ação padrão ou trate o caso adequadamente
            return choice(possible_actions) if possible_actions else None

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass
