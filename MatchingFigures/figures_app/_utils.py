# utils 

import random
import csv
from otree.api import *

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
        if answer == 0: # not answered in time, then continue
            continue
        score += 1 if inx1[i] == indx2[answer-1] else 0
    return score

def write_to_file(subsession: BaseSubsession, cards, results, filename):
    with open(filename, "w") as file:
        fieldnames = [
                        "id_in_subsession", 
                        "group_id", 
                        "id_in_group", 
                        "c1", "c2", "c3", "c4", "c5", "c6", 
                        "a1", "a2", "a3", "a4", "a5", "a6", 
                        "score"
                    ]
        writer = csv.writer(file, delimiter=',')
        
        writer.writerow(fieldnames)
        for player in subsession.get_players():
            tmp = player.get_results()
            write = list()

            write.append(player.id_in_subsession)
            write.append(player.group.id_in_subsession)
            write.append(player.id_in_group)
            write.append(cards[player.group.id_in_subsession][player.id_in_group - 1][0])
            write.append(cards[player.group.id_in_subsession][player.id_in_group - 1][1])
            write.append(cards[player.group.id_in_subsession][player.id_in_group - 1][2])
            write.append(cards[player.group.id_in_subsession][player.id_in_group - 1][3])
            write.append(cards[player.group.id_in_subsession][player.id_in_group - 1][4])
            write.append(cards[player.group.id_in_subsession][player.id_in_group - 1][5])
            write.append(tmp[0])
            write.append(tmp[1])
            write.append(tmp[2])
            write.append(tmp[3])
            write.append(tmp[4])
            write.append(tmp[5])
            write.append(results[player.id_in_subsession][player.round_number - 1])
            
            writer.writerow(write)


def process_txt(file_name):
    all_participants = []
    all_pairs = []

    with open(file_name, 'r') as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("Round"):
            # Skip the time info
            i += 2

            # Extract participant IDs and save them to a set
            participants = set(map(int, lines[i][18:-1].split(", ")))
            all_participants.append(participants)

            i += 1
            # Extract pairs and save them to a matrix
            pairs_line = lines[i].strip()
            pairs = [(int(pairs_line[j]), int(pairs_line[j+2])) for j in range(0, len(pairs_line), 5)]
            all_pairs.append(pairs)

        i += 1

    return all_participants, all_pairs

if __name__ == '__main__':
    indx1, indx2 = get_perm(2)
    print(indx1, indx2)
    test_answer = [6,2,5,3,1,4]
    score = check_answers(indx1, indx2, test_answer)
    print(score)
        