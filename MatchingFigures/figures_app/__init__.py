from otree.api import *
from figures_app._utils import *
import os

doc = """
Your app description
"""

class C(BaseConstants):
    NAME_IN_URL = 'figures'
    PLAYERS_PER_GROUP = 2 # people who are in the same group, None if all are in the same group
    MAIN_PLAYER_ID = 0

    NUM_ROUNDS = 1
    PAYMENT_PER_CORRECT = 1
    TIME_PER_GAME = 4 # min
    TIME_RESULTS = 15 # sec
    
    DIR_IMAGES = "original" # ai or original
    NUM_TOTAL = len([file for file in os.listdir(f"_static/global/{DIR_IMAGES}") if file.endswith(".png")])
    NUM_FIGURES = 6
    N_SHUFFLE = 3

    RESULTS = dict()
    

class Subsession(BaseSubsession):
    pass    


def creating_session(subsession: Subsession):
    for group in subsession.get_groups():
        cards = get_perm(
            n_players=C.PLAYERS_PER_GROUP, 
            n_cards=C.NUM_FIGURES, 
            n_shuffle=C.N_SHUFFLE, 
            n_total=C.NUM_TOTAL
        )
        
        for i, player in enumerate(group.get_players()):
            player.card0 = cards[i][0]
            player.card1 = cards[i][1]
            player.card2 = cards[i][2]
            player.card3 = cards[i][3]
            player.card4 = cards[i][4]
            player.card5 = cards[i][5]
   
    for player_id in range(1, len(subsession.get_players()) + 1): 
        C.RESULTS[player_id] = [] 

    # read network file


class Group(BaseGroup):
    # The correct results should be placed here
    pass


def make_result(fig_id):
    return models.IntegerField(
        label=f"My Figure {fig_id} corresponds to Figure number ... on my partner's screen  " +\
        f"//  Min figur {fig_id} tilsvarer figur nummer ... på partnerens skjerm.", 
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
    
    card0 = models.IntegerField()
    card1 = models.IntegerField()
    card2 = models.IntegerField()
    card3 = models.IntegerField()
    card4 = models.IntegerField()
    card5 = models.IntegerField()
    
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
    
    def get_cards(self):
        return [
                self.card0, 
                self.card1, 
                self.card2, 
                self.card3, 
                self.card4, 
                self.card5
            ]
    

# PAGES
class Game(Page):
    form_model = "player"
    timeout_seconds = 60 * C.TIME_PER_GAME

    @staticmethod
    def get_form_fields(player: Player):
        return ['result0', 'result1', 'result2', 'result3', 'result4', 'result5'] if player.id_in_group == 1 else []

    @staticmethod
    def vars_for_template(self):
        return {
            'ordered_figures': self.get_figure_names(self.get_cards()),
            'text': "Bellow you have to enter THE LABEL of the figure on " +\
                    "YOUR PARTNER'S SCREEN that matches the FIGURES ON YOUR SCREEN. Note that your answer should be between 1 and 6." +\
                    "  //  Nedenfor må du skrive inn MERKET på figuren på " +\
                    "PARTNERENS SKJERM som samsvarer med FIGURENE PÅ DIN SKJERM. Vær oppmerksom på at svaret ditt skal ligge mellom 1 og 6." if self.id_in_group == 1 else "" +\
                    "Converse with your partner so he/she can input the correct labels of YOUR FIGURES on HIS/HERS ANSWER FORM." +\
                    "  //  Snakk med partneren din, slik at han/hun kan skrive inn de riktige merkelappene for DINE FIGURER på HANS/HANS SVARSKJEMA.",
            'time': C.TIME_PER_GAME
        }


class ResultsWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        # Check for correct answers
        players = group.get_players()
        score = check_answers(
            players[0].get_cards(), 
            players[1].get_cards(), 
            group.get_players()[C.MAIN_PLAYER_ID].get_results()
        )

        for player in players:
            player.score = score
            C.RESULTS[player.id_in_subsession].append(score)
    

class Results(Page):
    timeout_seconds = C.TIME_RESULTS

    @staticmethod
    def vars_for_template(self):
        return {
            'score': self.score,
            'n_figs': C.NUM_FIGURES
        }


class WaitForGame(Page):
    @staticmethod
    def is_displayed(player: Player):
        return False #C.NUM_ROUNDS != 1
    
    @staticmethod
    def vars_for_template(self):
        multiplier = 1

        return {
            'time': C.TIME_PER_GAME * multiplier,
            'rounds' : self.rounds_to_play
        } 


class EndGame(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.group.round_number == C.NUM_ROUNDS
    
    @staticmethod
    def vars_for_template(self):
        return {
            'sum_score': sum(C.RESULTS[self.id_in_subsession]),
            'rounds_played': len(C.RESULTS[self.id_in_subsession]),
            'label': ["Round", "Score"],
            'rounds': list(range(1, len(C.RESULTS[self.id_in_subsession]) + 1)),
            'scores': C.RESULTS[self.id_in_subsession]
        }


class WaitForStartGame(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        pass


page_sequence = [WaitForStartGame, Game, ResultsWaitPage, Results, WaitForGame, EndGame]
