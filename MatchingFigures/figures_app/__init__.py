from otree.api import *
from figures_app._utils import *
import numpy as np
import os

doc = """
Your app description
"""

class C(BaseConstants):
    NAME_IN_URL = 'figures'
    PLAYERS_PER_GROUP = 2 # people who are in the same group, None if all are in the same group
    MAIN_PLAYER_ID = 0

    NUM_ROUNDS = 2
    PAYMENT_PER_CORRECT = 1
    TIME_PER_GAME = 5 # min
    
    DIR_IMAGES = "original" # ai or original
    NUM_TOTAL = len([file for file in os.listdir(f"_static/global/{DIR_IMAGES}") if file.endswith(".png")])
    NUM_FIGURES = 6
    N_SHUFFLE = 3

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
        C.CARDS[group_id] = get_perm(
            n_players=C.PLAYERS_PER_GROUP, 
            n_cards=C.NUM_FIGURES, 
            n_shuffle=C.N_SHUFFLE, 
            n_total=C.NUM_TOTAL
        )
    # read network file


class Group(BaseGroup):
    # The correct results should be placed here
    pass


def make_result(fig_id):
    return models.IntegerField(
        label=f"My Figure {fig_id} corresponds to Figure number ... on my partner's screen", 
        min=1, 
        max=6
    )
    
class Player(BasePlayer):
    '''All variables in the Player is for the current round.'''
    # payoff and round_number are defined in the background, don't redefine it.  

    score = models.IntegerField(initial=0)
    rounds_to_play = models.IntegerField(initial=1)
    
    result0 = make_result(1)
    result1 = make_result(2)
    result2 = make_result(3)
    result3 = make_result(4)
    result4 = make_result(5)
    result5 = make_result(6)
    
    def get_figure_names(self, indx):
        return [f'global/{C.DIR_IMAGES}/{i}.png' for i in indx]
    
    def get_results(self):
        return [
                self.result0, 
                self.result1, 
                self.result2, 
                self.result3, 
                self.result4, 
                self.result5
            ]
    
    
# PAGES
class Game(Page):
    form_model = "player"

    @staticmethod
    def get_form_fields(player: Player):
        return ['result0', 'result1', 'result2', 'result3', 'result4', 'result5'] if player.id_in_group == 1 else []

    @staticmethod
    def vars_for_template(self):
        ordered_figures = self.get_figure_names(C.CARDS[self.group.id_in_subsession][self.id_in_group - 1])
        text = "Bellow you have to enter THE LABEL of the figure on " +\
        "YOUR PARTNER'S SCREEN that matches the FIGURES ON YOUR SCREEN." if self.id_in_group == 1 else ""
        
        return {
            'ordered_figures': ordered_figures,
            'text': text
        }


class ResultsWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        # Check for correct answers
        main_player = group.get_players()[C.MAIN_PLAYER_ID]
        main_player.score = check_answers(
            C.CARDS[group.id_in_subsession][0], 
            C.CARDS[group.id_in_subsession][1], 
            main_player.get_results()
        )

        for player in group.get_players():
            player.score = main_player.score
    

class Results(Page):
    @staticmethod
    def vars_for_template(self):
        return {
            'score': self.score,
            'n_figs': C.NUM_FIGURES
        }


class EndRound(Page):
    @staticmethod
    def vars_for_template(self):
        multiplier = 1

        return {
            'time': C.TIME_PER_GAME * multiplier,
            'rounds' : self.rounds_to_play
        } 


page_sequence = [Game, ResultsWaitPage, Results, EndRound]
