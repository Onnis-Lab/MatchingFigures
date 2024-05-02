from otree.api import *
from figures_app._utils import *
import os
# from figures_app.network_utils import process_txt

doc = """
Your app description
"""

class C(BaseConstants):
    NAME_IN_URL = 'figures'
    PLAYERS_PER_GROUP = 2 # people who are in the same group, None if all are in the same group
    MAIN_PLAYER_ID = 1

    ALL_PARTICIPANTS, ALL_PAIRS = process_txt('figures_app/inputs.txt')
 
    NUM_ROUNDS = len(ALL_PARTICIPANTS)
    PAYMENT_PER_CORRECT = 1
    TIME_RULES = 0.5 # min
    TIME_PER_GAME = 0.5 # min
    TIME_RESULTS = 1 # sec
    
    DIR_IMAGES = "original" # ai or original
    NUM_TOTAL = len([file for file in os.listdir(f"_static/global/{DIR_IMAGES}") if file.endswith(".png")])
    NUM_FIGURES = 5
    N_SHUFFLE = 3

    RESULTS = dict()

    

class Subsession(BaseSubsession):

    def _create_group_matrix(self):
        pairs = C.ALL_PAIRS[self.round_number-1]
        matrix = []
        players = self.get_players()
        for pair in pairs:
            group = [players[player_id] for player_id in pair]
            matrix.append(group)
        return matrix


    def group_by_round(self):
        
        # New groupings
        matrix = self._create_group_matrix()
        self.set_group_matrix(matrix)

    def assign_cards(self):
        for group in self.get_groups():
            cards = get_perm(
                n_players=C.PLAYERS_PER_GROUP, 
                n_cards=C.NUM_FIGURES, 
                n_shuffle=C.N_SHUFFLE, 
                n_total=C.NUM_TOTAL
            )
            # print('cards:', cards)
            
            for i, player in enumerate(group.get_players()):
                # print(player.id_in_subsession)
                # print('i:', i)
                player.card0 = cards[i][0]
                player.card1 = cards[i][1]
                player.card2 = cards[i][2]
                player.card3 = cards[i][3]
                player.card4 = cards[i][4]
                # player.card5 = cards[i][5]



def creating_session(subsession: Subsession):
   
    for player_id in range(1, len(subsession.get_players()) + 1): 
        C.RESULTS[player_id] = [] 

    # read network file
    subsession.group_by_round()
    subsession.assign_cards()


class Group(BaseGroup):
    # The correct results should be placed here
    pass


def make_result(fig_id):
    return models.IntegerField(
        label=f"<b>My Figure {fig_id}</b> corresponds to Figure number ... on my partner's screen  ", 
        min=1,
        max=6
    )

def make_keyword(fig_id):
    return models.StringField(
        label=f"<b>My Figure {fig_id}</b> looks like ...",
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
    # result5 = make_result(6)
    
    keyword0 = make_keyword(1)
    keyword1 = make_keyword(2)
    keyword2 = make_keyword(3)
    keyword3 = make_keyword(4)
    keyword4 = make_keyword(5)
    
    card0 = models.IntegerField()
    card1 = models.IntegerField()
    card2 = models.IntegerField()
    card3 = models.IntegerField()
    card4 = models.IntegerField()
    # card5 = models.IntegerField()
    
    def get_figure_names(self, indx):
        return [f'global/{C.DIR_IMAGES}/{i}.png' for i in indx]
    
    def get_results(self):
        return [
                self.result0, 
                self.result1, 
                self.result2, 
                self.result3, 
                self.result4
                # self.result5
            ]

    def get_cards(self):
        return [
                self.card0,
                self.card1,
                self.card2,
                self.card3,
                self.card4
                # self.card5
            ]
    

# PAGES
class Game(Page):
    form_model = "player"
    timeout_seconds = 60 * C.TIME_PER_GAME

    @staticmethod
    def get_form_fields(player: Player):
        return ['result0', 'keyword0', 'result1', 'keyword1', 'result2', 'keyword2', 'result3', 'keyword3', 'result4', 'keyword4'] if player.id_in_group == C.MAIN_PLAYER_ID else []

    @staticmethod
    def vars_for_template(self):
        return {
            'ordered_figures': self.get_figure_names(self.get_cards()),
            'text': "<b>Scroll down to use chat. Find out which figure in " +\
                    "YOUR SET corresponds to which figure in your partner's set. Your answer should be between 1 and 5. Write down your answers in the boxes. </b>" if self.id_in_group == C.MAIN_PLAYER_ID else "" +\
                    "<b>Scroll down to use chat. Help your partner so they can solve which figure in their set corresponds to which figure on YOUR SET.</b>",
            'time': C.TIME_PER_GAME
        }

    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            if player.id_in_group == C.MAIN_PLAYER_ID:
                players = player.group.get_players()
                score = check_answers(
                    players[0].get_cards(), 
                    players[1].get_cards(), 
                    player.group.get_players()[C.MAIN_PLAYER_ID - 1].get_results()
                )

                for player_ in players:
                    player_.score = score
                    C.RESULTS[player_.id_in_subsession].append(score)

    @staticmethod
    def is_displayed(player: Player):
        # print(C.ALL_PARTICIPANTS[player.subsession.round_number-1])
        return player.id_in_subsession-1 in C.ALL_PARTICIPANTS[player.subsession.round_number-1]

class Results(Page):
    timeout_seconds = C.TIME_RESULTS

    @staticmethod
    def vars_for_template(self):
        return {
            'score': self.score,
            'n_figs': C.NUM_FIGURES
        }

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_subsession-1 in C.ALL_PARTICIPANTS[player.subsession.round_number-1]


class WaitForGame(WaitPage):
    wait_for_all_groups = True
    
    @staticmethod
    def is_displayed(player: Player):
        return C.NUM_ROUNDS != 1 and player.group.round_number == 1


class WaitForRound(WaitPage):
    wait_for_all_groups = True
    template_name = "figures_app/WaitForRound.html"
    
    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_subsession-1 not in C.ALL_PARTICIPANTS[player.round_number-1]
     
    @staticmethod
    def vars_for_template(self):
        multiplier = 1

        for round in range(self.round_number, C.NUM_ROUNDS): # next round rmb counter starts at 1
            if self.id_in_subsession-1 in C.ALL_PARTICIPANTS[round]:
                break
            multiplier += 1

        return {
            'time': C.TIME_PER_GAME * multiplier
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

class ShuffleWaitPage(WaitPage):

    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession):
        subsession.group_by_round()
        subsession.assign_cards()
        
        

class Rules(Page):
    timeout_seconds = C.TIME_RULES * 60
    
    @staticmethod
    def is_displayed(player: Player):
        return player.group.round_number == 1

    @staticmethod
    def vars_for_template(self):
        return {
        } 


page_sequence = [WaitForGame, Rules, WaitForStartGame, Game, Results, WaitForRound, ShuffleWaitPage, EndGame] # EndGame
