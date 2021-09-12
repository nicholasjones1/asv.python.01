import csv
import argparse

# we have imported some more libraries to do the maths work
import numpy as np
from sklearn.linear_model import LinearRegression

# and a plotting library
import matplotlib.pyplot as plt


class Calculator:
    def __init__(self, inputcsv):
        self.inputcsv = inputcsv

    def extract_linear_regression_data(self, filter_name: str):
        focuser_temp_list = []
        focuser_pos_list = []

        with open(self.inputcsv, newline='') as csvfile:
            # reader = csv.reader(csvfile)
            csv_dict_reader = csv.DictReader(csvfile)
            for row in csv_dict_reader:
                if row['Filter'] == filter_name:
                    focuser_pos_list.append(float(row["Focuser_pos"]))
                    focuser_temp_list.append(float(row["Focuser_temp"]))

        return focuser_temp_list, focuser_pos_list
    # end if

    @staticmethod
    def perform_temp_focus_linear_regression(focuser_temp_list, focuser_pos_list):
        dependent = np.array(focuser_pos_list)
        independent = np.array(focuser_temp_list).reshape(-1, 1)

        model = LinearRegression()
        model.fit(independent, dependent)
        intercept, coefficients = model.intercept_, model.coef_

        plt.scatter(focuser_temp_list, focuser_pos_list, color='g')
        plt.xlabel("temp")
        plt.ylabel("position")
        plt.plot(independent, model.predict(independent), color='k')
        plt.title("focuser pos = " + str(coefficients[0]) + "* temp(c) + " + str(int(intercept)))

        plt.show()

        return intercept, coefficients

    def calc(self):
        calculator = Calculator(args.inputfitscsv)
        focuser_temp_list, focuser_pos_list = calculator.extract_linear_regression_data(args.filter_name)
        intercept, coefficients = calculator.perform_temp_focus_linear_regression(focuser_temp_list, focuser_pos_list)

        print('focuser position = ' + str(coefficients[0]) + "* temp(c) + " + str(int(intercept)))

        return intercept, coefficients


def main(args):
    csv_reader = Calculator(args.inputfitscsv)
    csv_reader.calc()
# end def


# what is this strange looking thing?

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Log watch-dog to lookout for text and call a .bat file if it appears')
    parser.add_argument('inputfitscsv', type=str, help='The CSV file containing the FITS header data')
    parser.add_argument('filter_name', type=str, help='The filter to analyse')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')

    args = parser.parse_args()
    main(args)