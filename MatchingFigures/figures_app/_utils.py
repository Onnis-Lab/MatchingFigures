# utils 

from itertools import permutations
import random

# name of the image files 

# np.random.seed(1024)
def get_perm(n_players=1, n_shuffle=3, n_cards=6, n_total=6):
    """
        Arguments:
           - n_players: number of players
           - n_shuffle: number of cards to shuffle
           - n_cards: number of cards to select
           - n_total: total number of cards
    """ 
    # select n_cards random cards from the n_total
    indices = random.sample(range(1, n_total+1), k=n_cards)
    # select the n_shuffle indices from the indices array to shuffle
    shuffle_idx = random.sample(range(n_cards), k=n_shuffle)
    
    cards = list()
    for p_id in range(n_players):
        player_cards = indices.copy()
        new_idx = shuffle_idx.copy()
        random.shuffle(new_idx)
        
        for i in range(n_shuffle):
            player_cards[new_idx[i]] = indices[shuffle_idx[i]]
        
        cards.append(player_cards)

    return cards

def check_answers(inx1, indx2, answers):
    score = 0
    for i, answer in enumerate(answers):
        score += 1 if inx1[i] == indx2[answer-1] else 0
    return score

if __name__ == '__main__':
    indx1, indx2 = get_perm(2)
    print(indx1, indx2)
    test_answer = [6,2,5,3,1,4]
    score = check_answers(indx1, indx2, test_answer)
    print(score)