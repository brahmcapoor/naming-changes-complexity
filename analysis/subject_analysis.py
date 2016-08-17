import matplotlib.pyplot as plt
import seaborn as sns
from random import shuffle


def graph(transparencies_1, transparencies_2):
    x = [i for i in range(1,11)]
    sns.pointplot(x, transparencies_1)
    sns.pointplot(x, transparencies_2)
    plt.show()

def find_average(transparencies_1, transparencies_2):


def main():
    transparencies_1 = [20, 11, 19, 12, 18, 13, 17, 14, 16, 15]
    transparencies_2 = [n - 10 for n in transparencies_1]
    graph(transparencies_1, transparencies_2)
    find_average(transparencies_1, transparencies_2)

if __name__ == '__main__':
    main()
