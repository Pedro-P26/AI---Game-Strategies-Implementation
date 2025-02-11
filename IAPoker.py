from concurrent.futures import ThreadPoolExecutor

from games.hlpoker.player import HLPokerPlayer
from games.hlpoker.round import Round
from games.hlpoker.state import HLPokerState
from games.state import State

import random


class IAHLPokerPlayer(HLPokerPlayer):
    num_simulations = 1000

    def __init__(self, name):
        super().__init__(name)
        self.bluffing_chance = 0.15  # Probabilidade base de decidir blefar

    def hand_strength(self, private_cards, board_cards):
        # A função real de avaliação da mão deveria ser implementada aqui
        return random.randint(1, 100)  # Exemplo fictício

    def should_bluff(self, state, private_cards, board_cards):
        # Decisão de blefar baseada na força da mão e no tamanho do pote
        pot_size = state.get_pot()
        hand_strength = self.hand_strength(private_cards, board_cards)
        # Blefa se a mão for fraca e o pote for grande, ajustando a probabilidade de blefar
        if hand_strength < 30:
            bluff_probability = min(1.0, (
                        pot_size / 100) * self.bluffing_chance)  # Aumenta a chance de blefar se o pote for grande
            return random.random() < bluff_probability
        return False

    def simulate_game(self, state, action, private_cards, board_cards):
        if self.should_bluff(state, private_cards, board_cards):
            return random.random() < 0.5  # Assume uma chance de 50% de sucesso do blefe
        current_strength = self.hand_strength(private_cards, board_cards)
        future_strength = self.hand_strength(private_cards, board_cards + [random.randint(2, 14)])
        return future_strength > current_strength  # Simulação de melhoria da mão

    def monte_carlo_simulation(self, state, private_cards, board_cards):
        actions = state.get_possible_actions()
        with ThreadPoolExecutor() as executor:
            results = {action: executor.submit(self.perform_simulation, state, action, private_cards, board_cards) for
                       action in actions}
        best_action = max(results, key=lambda x: results[x].result())
        return best_action

    def perform_simulation(self, state, action, private_cards, board_cards):
        return sum(self.simulate_game(state, action, private_cards, board_cards) for _ in range(self.num_simulations))

    def get_action_with_cards(self, state: HLPokerState, private_cards, board_cards):
        return self.monte_carlo_simulation(state, private_cards, board_cards)

    def event_my_action(self, action, new_state):
        pass

    def event_opponent_action(self, action, new_state):
        pass

    def event_new_game(self):
        pass

    def event_end_game(self, final_state: State):
        pass

    def event_result(self, pos: int, result: int):
        pass

    def event_new_round(self, round: Round):
        pass