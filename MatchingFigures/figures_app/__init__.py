from otree.api import *
from figures_app._utils import *
import numpy as np

doc = """
Your app description
"""

class C(BaseConstants):
    NAME_IN_URL = 'figures'
    PLAYERS_PER_GROUP = 2 # people who are in the same group, None if all are in the same group
    MAIN_PLAYER_ID = 0

    NUM_ROUNDS = 1
    PAYMENT_PER_CORRECT = 1
    
    NUM_FIGURES = 6
    N_SHUFFLE = 3
    IMAGES = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png']
    CARDS = dict()
    NETWORK = np.array([[0, 1, 0, 1], 
                        [0, 0, 1, 0], 
                        [0, 0, 0, 1], 
                        [0, 0, 0, 0]])
    STARTING_PAIR = (0, 1)


class Subsession(BaseSubsession):
    pass    


def creating_session(subsession: Subsession):
    for group_id in range(1, len(subsession.get_groups()) + 1):
        C.CARDS[group_id] = get_perm(n_players=C.PLAYERS_PER_GROUP, n_cards=C.NUM_FIGURES, n_shuffle=C.N_SHUFFLE, n_total=C.NUM_FIGURES)
    # read network file


class Group(BaseGroup):
    # The correct results should be placed here
    pass
    

class Player(BasePlayer):
    '''All variables in the Player is for the current round.'''
    # payoff and round_number are defined in the background, don't redefine it.  

    payoff = 0
    
    result0 = models.IntegerField(
        label=f"My Figure 1 corresponds to Figure number ... on my partner's screen",
        min=1, max=6
        )
    result1 = models.IntegerField(
        label=f"My Figure 2 corresponds to Figure number ... on my partner's screen",
        min=1, max=6
        )
    result2 = models.IntegerField(
        label=f"My Figure 3 corresponds to Figure number ... on my partner's screen",
        min=1, max=6
        )
    result3 = models.IntegerField(
        label=f"My Figure 4 corresponds to Figure number ... on my partner's screen",
        min=1, max=6
        )
    result4 = models.IntegerField(
        label=f"My Figure 5 corresponds to Figure number ... on my partner's screen",
        min=1, max=6
        )
    result5 = models.IntegerField(
        label=f"My Figure 6 corresponds to Figure number ... on my partner's screen",
        min=1, max=6
        )
    
    def get_figure_names(self, indx):
        return [f'global/{i}.png' for i in indx]
    
    def get_results(self):
        return [self.result0, 
                self.result1, 
                self.result2, 
                self.result3, 
                self.result4, 
                self.result5]
    
    
# PAGES
class Game(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        if player.id_in_group == 1:
            # The first player's ID is 1
            return ['result0', 'result1', 'result2', 'result3', 'result4', 'result5']
        else:
            return []

    @staticmethod
    def vars_for_template(self):
        # For example, let's say you have six figures in a specific order:
        
        if self.id_in_group == 1:
            ordered_figures = self.get_figure_names(C.CARDS[self.group.id_in_subsession][0]) 
            text = "Bellow you have to enter THE LABEL of the figure on YOUR PARTNER'S SCREEN that matches the FIGURES ON YOUR SCREEN."
        else:
            ordered_figures = self.get_figure_names(C.CARDS[self.group.id_in_subsession][1])
            text = ""

        return {
            'ordered_figures': ordered_figures,
            'text': text
        }


class ResultsWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        # Check for correct answers
        main_player = group.get_players()[C.MAIN_PLAYER_ID]
        main_player.payoff = check_answers(C.INDX1, C.INDX2, main_player.get_results())

        for player in group.get_players():
            player.payoff = main_player.payoff
    

class Results(Page):
    @staticmethod
    def var_for_template(player: Player):
        pass 

# class CombinedResults(Page):
#     @staticmethod
#     def var_for_template(player: Player):
#         all_players = player.in_all_rounds()
#         combined_payoff = 0
#         for this_player in all_players:
#             combined_payoff += this_player.payoff
#         return {
#             'combined_payoff': combined_payoff
#         }

page_sequence = [Game, ResultsWaitPage, Results]#, CombinedResults]
