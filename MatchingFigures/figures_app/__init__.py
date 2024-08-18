from otree.api import *
from figures_app._utils import *
import os

doc = """
Your app description
"""

class C(BaseConstants):
    NAME_IN_URL = 'figures'
    PLAYERS_PER_GROUP = 2 # people who are in the same group, None if all are in the same group
    MAIN_PLAYER_ID = 1

    ALL_PARTICIPANTS, ALL_PAIRS = process_txt('figures_app/random4242.txt')
 
    NUM_ROUNDS = len(ALL_PARTICIPANTS)
    GAMES_PER_ROUND = [len(participants) // 2 for participants in ALL_PARTICIPANTS]
    GAMES_PLAYED = 0
    
    PAYMENT_PER_CORRECT = 1
    TIME_RULES = 0.1 # min
    TIME_PER_GAME = 0.2 # min
    TIME_RESULTS = 5 # sec
    
    DIR_IMAGES = "original" # ai or original
    NUM_TOTAL = len([file for file in os.listdir(f"_static/global/{DIR_IMAGES}") if file.endswith(".png")])
    NUM_FIGURES = 4
    N_SHUFFLE = 2


class Subsession(BaseSubsession):
    games_played = models.IntegerField(initial=0)
    
    def _create_group_matrix(self):
        pairs = C.ALL_PAIRS[self.round_number-1]
        matrix = list()
        players = self.get_players()

        for pair in pairs:
            group = list()

            for player_id in pair: 
                group.append(players[player_id])
                players[player_id].playing = 1 if player_id in C.ALL_PARTICIPANTS[players[player_id].subsession.round_number - 1] else 0

            matrix.append(group)

        return matrix

    def _group_by_round(self):
        # New groupings
        matrix = self._create_group_matrix()
        self.set_group_matrix(matrix)

    def _assign_cards(self):
        for group in self.get_groups():
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
                # player.card4 = cards[i][4]
                # player.card5 = cards[i][5]
                
    def reset(self):
        self._group_by_round()
        self._assign_cards()
        self.games_played = 0


def creating_session(subsession: Subsession):
    subsession.reset()

class Group(BaseGroup):
    # The correct results should be placed here
    pass


def make_result(fig_id: int):
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
    playing = models.IntegerField(initial=0)
    
    result0 = make_result(1)
    result1 = make_result(2)
    result2 = make_result(3)
    result3 = make_result(4)
    # result4 = make_result(5)
    # result5 = make_result(6)
    
    card0 = models.IntegerField()
    card1 = models.IntegerField()
    card2 = models.IntegerField()
    card3 = models.IntegerField()
    # card4 = models.IntegerField()
    # card5 = models.IntegerField()
    
    def get_figure_names(self, indx: int):
        return [f'global/{C.DIR_IMAGES}/{i}.png' for i in indx]
    
    def get_results(self):
        return [
                self.result0, 
                self.result1, 
                self.result2, 
                self.result3#, 
                # self.result4, 
                # self.result5
            ]
    
    def get_cards(self):
        return [
                self.card0, 
                self.card1, 
                self.card2, 
                self.card3#, 
                # self.card4, 
                # self.card5
            ]
    

# PAGES
class Game(Page):
    form_model = "player"
    timeout_seconds = 60 * C.TIME_PER_GAME

    @staticmethod
    def get_form_fields(player: Player):
        # return ['result0', 'result1', 'result2', 'result3', 'result4', 'result5'] if player.id_in_group == C.MAIN_PLAYER_ID else []
        return ['result0', 'result1', 'result2', 'result3'] if player.id_in_group == C.MAIN_PLAYER_ID else []

    @staticmethod
    def vars_for_template(self):
        return {
            'ordered_figures': self.get_figure_names(self.get_cards()),
            'text': "Bellow you have to enter THE LABEL of the figure on " +\
                    "YOUR PARTNER'S SCREEN that matches the FIGURES ON YOUR SCREEN. Note that your answer should be between 1 and 4." +\
                    "  //  Nedenfor må du skrive inn MERKET på figuren på " +\
                    "PARTNERENS SKJERM som samsvarer med FIGURENE PÅ DIN SKJERM. Vær oppmerksom på at svaret ditt skal ligge mellom 1 og 4." if self.id_in_group == C.MAIN_PLAYER_ID else "" +\
                    "Converse with your partner so he/she can input the correct labels of YOUR FIGURES on HIS/HERS ANSWER FORM." +\
                    "  //  Snakk med partneren din, slik at han/hun kan skrive inn de riktige merkelappene for DINE FIGURER på HANS/HENNES SVARSKJEMA.",
            'time': C.TIME_PER_GAME
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened: bool):
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

                player.subsession.games_played += 1 
                    
    @staticmethod
    def is_displayed(player: Player):
        return player.playing


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
        return player.playing


# class WaitForGame(WaitPage):
#     wait_for_all_groups = True
    
#     @staticmethod
#     def is_displayed(player: Player):
#         return C.NUM_ROUNDS != 1 and player.group.round_number == 1


class WaitForRound(WaitPage):
    # wait_for_all_groups = True
    template_name = "figures_app/WaitForRound.html"
    
    @staticmethod
    def is_displayed(player: Player):
        return not player.playing
     
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
    

# class EndGame(Page):
#     @staticmethod
#     def is_displayed(player: Player):
#         return player.group.round_number == C.NUM_ROUNDS
    
#     @staticmethod
#     def vars_for_template(self):
#         return {
#             'sum_score': sum(C.RESULTS[self.id_in_subsession]),
#             'rounds_played': len(C.RESULTS[self.id_in_subsession]),
#             'label': ["Round", "Score"],
#             'rounds': list(range(1, len(C.RESULTS[self.id_in_subsession]) + 1)),
#             'scores': C.RESULTS[self.id_in_subsession]
#         }


class WaitForStartGame(WaitPage):
    @staticmethod
    def is_displayed(player: Player):
        return player.playing


class ShuffleWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        if C.GAMES_PLAYED == C.GAMES_PER_ROUND:
            group.subsession.reset()


class Rules(Page):
    timeout_seconds = C.TIME_RULES * 60
    
    @staticmethod
    def is_displayed(player: Player):
        return player.group.round_number == 1


page_sequence = [Rules, WaitForStartGame, Game, Results, WaitForRound, ShuffleWaitPage] 
