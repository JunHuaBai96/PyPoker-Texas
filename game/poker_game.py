from treys import Card, Deck, Evaluator
from typing import List, Dict, Optional
import random

class Player:
    def __init__(self, name: str, chips: int):
        self.name = name
        self.chips = chips
        self.cards = []
        self.is_folded = False
        self.current_bet = 0
        self.is_all_in = False

    def reset_hand(self):
        self.cards = []
        self.is_folded = False
        self.current_bet = 0
        self.is_all_in = False

class PokerGame:
    def __init__(self, num_players: int, small_blind: int):
        self.num_players = num_players
        self.small_blind = small_blind
        self.big_blind = small_blind * 2
        self.players: List[Player] = []
        self.deck = Deck()
        self.community_cards = []
        self.pot = 0
        self.current_player_idx = 0
        self.dealer_idx = 0
        self.evaluator = Evaluator()
        self.current_bet = 0
        self.round_state = 'preflop'  # preflop, flop, turn, river
        
    def initialize_game(self, player_names: List[str], initial_chips: int):
        self.players = [Player(name, initial_chips) for name in player_names]
        self.dealer_idx = random.randint(0, self.num_players - 1)
        
    def start_new_hand(self):
        # Reset game state
        self.deck = Deck()
        self.community_cards = []
        self.pot = 0
        self.current_bet = 0
        self.round_state = 'preflop'
        
        # Reset player hands
        for player in self.players:
            player.reset_hand()
            
        # Deal cards to players
        for _ in range(2):
            for player in self.players:
                if not player.is_folded:
                    player.cards.append(self.deck.draw(1)[0])
                    
        # Post blinds
        sb_pos = (self.dealer_idx + 1) % self.num_players
        bb_pos = (self.dealer_idx + 2) % self.num_players
        
        self.players[sb_pos].chips -= self.small_blind
        self.players[sb_pos].current_bet = self.small_blind
        self.players[bb_pos].chips -= self.big_blind
        self.players[bb_pos].current_bet = self.big_blind
        
        self.pot = self.small_blind + self.big_blind
        self.current_bet = self.big_blind
        self.current_player_idx = (bb_pos + 1) % self.num_players

    def deal_next_street(self):
        if self.round_state == 'preflop':
            # Deal flop
            self.community_cards.extend(self.deck.draw(3))
            self.round_state = 'flop'
        elif self.round_state == 'flop':
            # Deal turn
            self.community_cards.extend(self.deck.draw(1))
            self.round_state = 'turn'
        elif self.round_state == 'turn':
            # Deal river
            self.community_cards.extend(self.deck.draw(1))
            self.round_state = 'river'
            
    def get_valid_actions(self, player: Player) -> Dict[str, bool]:
        if player.is_folded or player.is_all_in:
            return {'check': False, 'call': False, 'raise': False, 'fold': False}
            
        can_check = player.current_bet == self.current_bet
        can_call = player.chips > 0 and player.current_bet < self.current_bet
        can_raise = player.chips > self.current_bet
        can_fold = not can_check
        
        return {
            'check': can_check,
            'call': can_call,
            'raise': can_raise,
            'fold': can_fold
        }
        
    def evaluate_hands(self) -> List[tuple]:
        results = []
        for player in self.players:
            if not player.is_folded:
                # 将玩家的手牌和公共牌组合在一起
                all_cards = player.cards + self.community_cards
                score = self.evaluator.evaluate(all_cards[:5], [])  # 只取前5张牌评估
                results.append((player, score))
        return sorted(results, key=lambda x: x[1])
        
    def process_action(self, action: str, amount: Optional[int] = None) -> bool:
        player = self.players[self.current_player_idx]
        valid_actions = self.get_valid_actions(player)
        
        if not valid_actions.get(action, False):
            return False
            
        if action == 'fold':
            player.is_folded = True
        elif action == 'call':
            call_amount = self.current_bet - player.current_bet
            player.chips -= call_amount
            player.current_bet = self.current_bet
            self.pot += call_amount
        elif action == 'raise':
            if amount is None or amount <= self.current_bet:
                return False
            player.chips -= (amount - player.current_bet)
            self.pot += (amount - player.current_bet)
            player.current_bet = amount
            self.current_bet = amount
        
        # Move to next player
        self.current_player_idx = (self.current_player_idx + 1) % self.num_players
        return True
        
    def is_round_complete(self) -> bool:
        active_players = [p for p in self.players if not p.is_folded]
        if len(active_players) == 1:
            return True
            
        return all(p.current_bet == self.current_bet or p.is_folded or p.is_all_in 
                  for p in self.players) 