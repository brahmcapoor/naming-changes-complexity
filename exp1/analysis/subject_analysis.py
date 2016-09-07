from random import shuffle
import matplotlib.pyplot as plt
import seaborn as sns
import pandas
import csv
import argparse
import os

"""
The script required for the data analysis. Requires several python libraries
to function but otherwise isn't too complicated.
"""


def individual_graph(transparencies_1, transparencies_2):

    x = [i for i in range(1, 81)]
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


def find_threshold(log_1, log_2):

    average_1 = 0
    average_2 = 0

    turning_points_1 = find_turning_points(log_1[40:])

    if turning_points_1:
        average_1 = sum(turning_points_1)/len(turning_points_1)
    else:
        average_1 = 0

    turning_points_2 = find_turning_points(log_2[40:])

    if turning_points_2:
        average_2 = sum(turning_points_2)/len(turning_points_2)
    else:
        average_2 = 0

    return (average_1 + average_2)/2


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

    return (transparency_log_1, transparency_log_2, transparency_log_3,
            transparency_log_4)


def graph_subject(subject_number):
        transparency_log_1, transparency_log_2, transparency_log_3, \
            transparency_log_4 = load_subject_data(subject_number)

        individual_graph(transparency_log_1, transparency_log_2)

        average_easy = find_threshold(transparency_log_1,
                                      transparency_log_2)

        print("Subject average for easy condition is {}".format(average_easy))

        individual_graph(transparency_log_3, transparency_log_4)

        average_hard = find_threshold(transparency_log_3,
                                      transparency_log_4)

        print("Subject average for hard condition is {}".format(average_hard))


def show_summary_graph():

    number_of_subjects = len(os.listdir("../subject logs")) - 1

    subject_data = []
    for i in range(1, number_of_subjects + 1):
        transparency_log_1, transparency_log_2, transparency_log_3, \
            transparency_log_4 = load_subject_data(i)

        easy_threshold = find_threshold(transparency_log_1, transparency_log_2)
        hard_threshold = find_threshold(transparency_log_3, transparency_log_4)

        subject_data.append((i, easy_threshold, "Easy"))
        subject_data.append((i, hard_threshold, "Hard"))

    df = pandas.DataFrame(subject_data, columns=["Subject", "Threshold",
                                                 "Condition"])

    print(df)

    sns.factorplot(data=df,
                   x="Subject",
                   y="Threshold",
                   hue="Condition",
                   linestyles=[" ", " "],
                   legend=False)
    plt.legend(loc='upper left')

    plt.show()


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-i", "--individual",
                       help="Analyze a particular subject",
                       action="store", metavar='')
    group.add_argument("-s", "--summary", help="See a summary graph",
                       action="store_true")
    args = parser.parse_args()

    if args.individual:
        graph_subject(args.individual)
    if args.summary:
        show_summary_graph()

if __name__ == '__main__':
    main()
