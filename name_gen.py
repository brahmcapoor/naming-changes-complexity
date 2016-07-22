from random import sample, shuffle, randint

"""
Generates 16 random pairs of names, one simple and one complex
"""


VOWELS = ['a', 'e', 'i', 'o', 'u']
CONSONANTS = ['s', 'z', 'f', 'v', 'k', 'g', 'p', 'b', 't', 'd']

def generate_random_word(complex = True):
    """
    Generates one random word
    """

    if complex:
        letters = 4

    else:
        letters = 2

    vowels = sample(VOWELS, letters)
    consonants = sample(CONSONANTS, letters)
    shuffle(vowels)
    shuffle(consonants)

    if complex:
        return "".join(consonants[i] + vowels[i] for i in range(4))
    else:
        unit_1 = consonants[0] + vowels[0]
        unit_2 = consonants[1] + vowels[1]
        n_1 = randint(1,3)
        n_2 = 4 - n_1
        syllables = []
        for i in range(n_1):
            syllables.append(unit_1)
        for i in range(n_2):
            syllables.append(unit_2)
        shuffle(syllables)
        return "".join(syllable for syllable in syllables)


def generate_pair_name():
    """
    Generates a string of names for a pair
    """
    
    simple = generate_random_word(False)
    hard = generate_random_word(True)
    return simple + " " + hard


def main():
    names = [generate_pair_name() for i in range(16)]
    with open('names.txt', 'wb') as f:
        f.writelines(name + '\n' for name in names)

if __name__ == '__main__':
    main()
