from random import sample, shuffle, randint, choice

"""
Generates 8 random pairs of names, one simple and one complex.

It's a pretty simple script, so it's not commented.
"""


VOWELS = ['a', 'e', 'i', 'o', 'u']
CONSONANTS = ['s', 'z', 'f', 'v', 'k', 'g', 'p', 'b', 't', 'd']


def generate_random_word(complex=False):
    """
    Generates one random word
    """

    if complex:
        letters = 3

    else:
        letters = 1

    vowels = sample(VOWELS, letters)
    consonants = sample(CONSONANTS, letters)
    shuffle(vowels)
    shuffle(consonants)

    return "".join(consonants[i] + vowels[i] for i in range(letters))


def generate_pair_name():
    """
    Generates a string of names for a pair
    """

    simple = generate_random_word()
    while True:
        hard = generate_random_word(True)
        if simple not in hard:
            break
    return simple + " " + hard


def main():
    names = [generate_pair_name() for i in range(8)]
    with open('names.txt', 'wb') as f:
        f.writelines(name + '\n' for name in names)

if __name__ == '__main__':
    main()
