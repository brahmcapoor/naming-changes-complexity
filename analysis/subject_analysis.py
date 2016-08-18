import matplotlib.pyplot as plt
import seaborn as sns
from random import shuffle


def graph(transparencies_1, transparencies_2):
    
    x = [i for i in range(1,11)]
    sns.pointplot(x, transparencies_1)
    sns.pointplot(x, transparencies_2)
    plt.show()

def find_turning_points(series):

    turning_points = []
    last_point = len(series) - 1

    for i, point in enumerate(series):
        if i != 0 and i != last_point:
            if (point < series[i - 1] and point < series[i + 1]) or \
            (point > series[i - 1] and point > series[i + 1]):
                turning_points.append(point)

    return turning_points



def main():
    transparencies_1 = [20, 11, 19, 12, 18, 13, 17, 14, 16, 15]
    transparencies_2 = [n - 10 for n in transparencies_1]
    #graph(transparencies_1, transparencies_2)
    print(find_turning_points(transparencies_1))

if __name__ == '__main__':
    main()
