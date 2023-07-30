# utils 

from itertools import permutations
import numpy as np

# name of the image files 

np.random.seed(1024)
def get_perm(n=1):
    # images = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png']
    indices = [1,2,3,4,5,6]
    combo_length = 6

    # combinations_img = list(permutations(images))
    combinations_idx = list(permutations(indices))

    if n == 1:
        index = np.random.randint(0, len(combinations_idx))
        return list(combinations_idx[index])

    a = []
    for _ in range(n):
        index = np.random.randint(0, len(combinations_idx))
        a.append(list(combinations_idx[index]))

    return a

def check_answers(inx1, indx2, answers):
    score = 0 
    for i, answer in enumerate(answers):
        if inx1[i] == indx2[answer-1]:
            score += 1
    return score

if __name__ == '__main__':
    indx1, indx2 = get_images_perm(2)
    print(indx1, indx2)
    test_answer = [6,2,5,3,1,4]
    score = check_answers(indx1, indx2, test_answer)
    print(score)