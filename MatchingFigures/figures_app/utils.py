# utils 

from itertools import permutations
import numpy as np

# name of the image files 

def get_images_perm(n=1):
    images = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png']
    indices = [1,2,3,4,5,6]
    combo_length = 6

    combinations_img = list(permutations(images))
    combinations_idx = list(permutations(indices))

    if n == 1:
        index = np.random.randint(0, len(combinations_img))
        return combinations_idx[index], combinations_img[index]

    a = []
    for _ in range(n):
        index = np.random.randint(0, len(combinations_img))
        a.append([combinations_idx[index], combinations_img[index]])

    return a

def answer(inx1, indx2):

    correct_result = [](1, 2, 3, 6, 5, 4

    return correct_result

if __name__ == '__main__':
    a = get_images_perm(2)
    print(a)



[1, 2, 3, 6, 5, 4]
[4, 5, 1, 2, 6, 3]
