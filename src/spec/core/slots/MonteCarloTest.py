import unittest

from src.core.models.Slots import Slots

class MonteCarloTest(unittest.TestCase):
    def monte_carlo_simulation(self, trials=10000, bet=10, slots=Slots()):
        prize = 0
        bonus = 0
        for _ in range(trials):
            slots.visited = []
            slots.wins = []
            slots.scatter_count = 0
            
            slots.fill_table()
            slots.find_clusters_and_update()
            
            wins = [win for win in slots.wins]
            while len(slots.wins) > 0:
                for win in slots.wins:
                    wins.append(win)
                    
                slots.visited = []
                slots.wins = []
                
                slots.tumble_table()
                slots.fill_table(only_empty=True)
                slots.find_clusters_and_update()

            for win in wins:
                prize += (((win.prize() // 100) * (bet // 100)) / 100)
                
            if slots.bonus_game():
                bonus += slots.bonus_game()

        return prize, bonus

    def test_rtp(self):  
        """
            Use monte carlo simulation to assert RTP over time to 92% with a maximum of 5% of variance
        """
        total = 0
        rtp = 0
        trials = 10_000
        bet = 100
        total_bonus = 0
        total_bet = (bet // 100) * trials

        print(f"\nBet: ${bet // 100} for {trials} times (${total_bet})")
        wins, bonus_rounds = self.monte_carlo_simulation(trials=trials, bet=bet)
        total += (wins - total_bet)
        rtp += (wins - total_bet) / trials
        total_bonus += bonus_rounds
        
        while(bonus_rounds > 0):
            wins, bonus = self.monte_carlo_simulation(trials=bonus_rounds, bet=bet)
            total += wins
            rtp += wins / trials
            bonus_rounds += bonus
            total_bonus += bonus
            bonus_rounds -= bonus_rounds
        
        rtp = (rtp * 100) // 1
        bonus_rounds = ((total_bonus / (trials + total_bonus)) * 100) // 1
        total = total // 1
        
        print(f"Bonus rounds: {bonus_rounds:.2f}%")    
        print(f"Final Balance: ${total:.2f}")    
        print(f"Theoretical RTP: {rtp:.2f}%")
        
        self.assertIn(rtp, range(87, 97))
        self.assertIn(total, range(8700, 9700))
        self.assertIn(bonus_rounds, range(10, 20))
        
