import matplotlib.pyplot as plt
import seaborn as sns
from random import shuffle
import csv


def graph(transparencies_1, transparencies_2):

    x = [i for i in range(1,41)]
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

def load_subject_data(subject_number):
    filename = "../subject logs/subject {}.csv".format(subject_number)

    with open(filename, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)[1:]

    transparency_log_1 = [trial[1] for trial in data]
    transparency_log_2 = [trial[3] for trial in data]
    transparency_log_3 = [trial[5] for trial in data]
    transparency_log_4 = [trial[7] for trial in data]

    transparency_log_1 = list(map(lambda x: float(x), transparency_log_1))
    transparency_log_2 = list(map(lambda x: float(x), transparency_log_2))
    transparency_log_3 = list(map(lambda x: float(x), transparency_log_3))
    transparency_log_4 = list(map(lambda x: float(x), transparency_log_4))

    return (transparency_log_1, transparency_log_2)

def main():
    subject_number = input("Subject number? ")
    transparency_log_1, transparency_log_2 = load_subject_data(subject_number)
    graph(transparency_log_1, transparency_log_2)

    find_turning_points(transparencies_1)

if __name__ == '__main__':
    main()
