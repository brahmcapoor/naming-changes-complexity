from random import shuffle
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import csv
import argparse
import os
import shutil

"""
The script required for the data analysis. Requires several python libraries
to function but otherwise isn't too complicated.
"""


def generate_all_graphs():
    number_of_subjects = len(os.listdir("../subject logs")) - 1

    for i in range(1, number_of_subjects + 1):
        try:
            os.mkdir("Subject {}".format(i))
        except FileExistsError:
            shutil.rmtree("Subject {}".format(i))
            os.mkdir("Subject {}".format(i))

        transparency_log_1, transparency_log_2, transparency_log_3, \
            transparency_log_4 = load_subject_data(i)

        individual_graph(transparency_log_1, transparency_log_2, "Easy", i,
                         False)
        individual_graph(transparency_log_3, transparency_log_4, "Hard", i,
                         False)

        print("Generated graphs for subject {}".format(i))


def individual_graph(transparencies_1, transparencies_2, condition,
                     subject_number, display_graph=True):

    x = [i for i in range(1, 81)]
    sns.pointplot(x, transparencies_1, color='red')
    plot = sns.pointplot(x, transparencies_2)
    plot.set(xlabel="Trial", ylabel="Contrast",
             title="{} Condition".format(condition))
    if display_graph:
        plt.show()
    plot = plot.get_figure()
    plot.savefig("Subject {}/{}.png".format(subject_number, condition))
    plt.cla()


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

    turning_points_1 = find_turning_points(log_1)

    if turning_points_1:
        average_1 = sum(turning_points_1)/len(turning_points_1)
    else:
        average_1 = 0

    turning_points_2 = find_turning_points(log_2)

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


def check_subject_validity(subject_number):
    with open('../subject logs/catch trials.csv', 'r') as f:
        reader = csv.reader(f)
        data = list(reader)

    subject_info = data[subject_number]

    catch_trials_valid = int(subject_info[1]) > 29 and int(subject_info[2]) < 5

    with open('../memory_results_after.csv', 'r') as f:
        reader = csv.reader(f)
        data = list(reader)

    subject_info = data[subject_number]

    remembered_names_correctly = subject_info[2] == subject_info[3] and \
        subject_info[4] == subject_info[5] and \
        subject_info[6] == '' and \
        subject_info[7] == ''

    return catch_trials_valid and remembered_names_correctly


def graph_subject(subject_number):
        try:
            os.mkdir("Subject {}".format(subject_number))
        except FileExistsError:
            shutil.rmtree("Subject {}".format(subject_number))
            os.mkdir("Subject {}".format(subject_number))
        transparency_log_1, transparency_log_2, transparency_log_3, \
            transparency_log_4 = load_subject_data(subject_number)

        individual_graph(transparency_log_1, transparency_log_2, "Easy",
                         subject_number)

        average_easy = find_threshold(transparency_log_1,
                                      transparency_log_2)

        print("Subject average for easy condition is {}".format(average_easy))

        individual_graph(transparency_log_3, transparency_log_4, "Hard",
                         subject_number)

        average_hard = find_threshold(transparency_log_3,
                                      transparency_log_4)

        print("Subject average for hard condition is {}".format(average_hard))

        valid = check_subject_validity(int(subject_number))

        if valid:
            print("Subject is valid")
        else:
            print("Subject is invalid")


def show_summary_graph():

    number_of_subjects = len(os.listdir("../subject logs")) - 1

    subject_data = []
    for i in range(1, number_of_subjects + 1):
        transparency_log_1, transparency_log_2, transparency_log_3, \
            transparency_log_4 = load_subject_data(i)

        easy_threshold = find_threshold(transparency_log_1, transparency_log_2)
        hard_threshold = find_threshold(transparency_log_3, transparency_log_4)

        subject_data.append((i, easy_threshold, "Easy",
                             check_subject_validity(i)))
        subject_data.append((i, hard_threshold, "Hard",
                             check_subject_validity(i)))

    df = pd.DataFrame(subject_data, columns=["Subject", "Threshold",
                                             "Condition", "Valid"])

    print(df)

    plot = sns.factorplot(data=df,
                          x="Subject",
                          y="Threshold",
                          hue="Condition",
                          linestyles=[" ", " "],
                          legend=False,
                          size=8,
                          aspect=2)
    plt.legend(loc='upper left')

    plot.set(xlabel="Subject Number",
             ylabel="Contrast",
             title="Summary of all subjects")

    plt.show()

    plot.savefig("Summary.png")


def generate_results_file():

    number_of_subjects = len(os.listdir("../subject logs")) - 1

    table = []
    for i in range(1, number_of_subjects + 1):
        transparency_log_1, transparency_log_2, transparency_log_3, \
            transparency_log_4 = load_subject_data(i)

        easy_threshold = find_threshold(transparency_log_1, transparency_log_2)
        hard_threshold = find_threshold(transparency_log_3, transparency_log_4)

        valid = check_subject_validity(i)

        with open('../memory_results_after.csv', 'r') as f:
            reader = csv.reader(f)
            data = list(reader)

        subject_info = data[i]

        round_number = subject_info[1]

        table.append([i, round_number, easy_threshold, hard_threshold, valid])

    table = pd.DataFrame(table, columns=["Subject", "Round number",
                                         "Easy Threshold", "Hard Threshold",
                                         "Valid"])

    table.to_csv("Summary.csv")

    print("Results file can be found in Summary.csv")


def main():

    plt.rcParams['figure.figsize'] = (18, 8)

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-i", "--individual",
                       help="Analyze a particular subject",
                       action="store", metavar='')
    group.add_argument("-s", "--summary", help="See a summary graph",
                       action="store_true")
    group.add_argument("-r", "--result", help="Create a results file",
                       action="store_true")
    args = parser.parse_args()

    if args.individual:
        if args.individual == 'a':
            generate_all_graphs()
        else:
            graph_subject(args.individual)
    if args.summary:
        show_summary_graph()
    if args.result:
        generate_results_file()


if __name__ == '__main__':
    main()
