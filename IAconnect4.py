from random import choice

from games.connect4.player import Connect4Player
from games.connect4.state import Connect4State
from games.state import State




class IAConnect4Player(Connect4Player):
    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: Connect4State):
        # Determinar a coluna central
        center_col = state.get_num_cols() // 2
        possible_actions = state.get_possible_actions()

        # Tentativa de bloquear o oponente se ele estiver prestes a ganhar
        critical_action = self.find_critical_block(state)
        if critical_action:
            return critical_action

        # Verificar se a coluna central está disponível
        for action in possible_actions:
            if action.get_col() == center_col:
                return action  # Retorna a ação que coloca a peça na coluna central

        # Se a coluna central não estiver disponível, escolha uma ação aleatória
        return choice(possible_actions)

    def find_critical_block(self, state):
        opponent_id = 1 if state.get_acting_player() == 0 else 0
        for action in state.get_possible_actions():
            temp_state = state.clone()
            temp_state.update(action)  # Simula a jogada do oponente
            if temp_state._Connect4State__check_winner(opponent_id):
                # ação se o oponente vencer
                # Verifica se a jogada resultaria em vitória
                return action
        return None


    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass