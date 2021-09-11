from astropy.io import fits
import csv
import argparse
import os


# fits_header_data represents a csv data row
class FitsHeaderData:
    def __init__(self):
        # dictionary (collection of key/value pairs)
        self.header = {"Object": "", "Filter": "", "Binning": "", "Focuser_pos": -1,  "Focuser_temp": 999, "Sensor_temp": 999, "RA": "", "Dec": "" }


class FitsHeaderExtractor:
    def __init__(self, inputpath, outputcsv):
        self.inputpath = inputpath
        self.outputcsv = outputcsv
        self.csv_columns = ["Object", "Filter", "FileName", "Binning", "Focuser_pos", "Focuser_temp", "Sensor_temp",
                            "RA", "Dec"]
    # end def

    def load(self):
        csv_row_list = []

        for file_name in os.listdir(self.inputpath):
            file_location = os.path.join(self.inputpath, file_name)

            if not os.path.isdir(file_location) :
                if file_location.endswith('FIT'):
                    print("file : " + file_name)
                    fits_file = FitsImage(file_location, file_name)

                    print("        filter: " + fits_file.get_filter())
                    print("       binning: " + str(fits_file.get_binning()))
                    print("    focus temp: " + str(fits_file.get_focus_temp()))
                    print("     focus pos: " + str(fits_file.get_focus_position()))
                    print("     object RA: " + str(fits_file.get_ra()))
                    print("    object DEC: " + str(fits_file.get_dec()))

                    header_data = self.populate_header_data_from_fits(fits_file)
                    csv_row_list.append(header_data)

                # end if
            else:
                self.load(file_location)
            # end if
        # end for loop

        return csv_row_list
    # end load

    # Assign values from the Fits header to a csv_row.
    # The csv_row is a dictionary of name/values.
    @staticmethod
    def populate_header_data_from_fits(fits_file):
        csv_row = FitsHeaderData().header
        csv_row["FileName"] = str(fits_file.file_name)
        csv_row["Object"] = str(fits_file.get_object())
        csv_row["Binning"] = str(fits_file.get_binning())
        csv_row["Filter"] = str(fits_file.get_filter())
        csv_row["Focuser_pos"] = fits_file.get_focus_position()
        csv_row["Focuser_temp"] = fits_file.get_focus_temp()
        csv_row["Sensor_temp"] = fits_file.get_sensor_temp()
        csv_row["RA"] = str(fits_file.get_ra())
        csv_row["Dec"] = str(fits_file.get_dec())

        return csv_row
    # end def

    def write(self, row_list):
        file_path = self.outputcsv
        f = open(file_path, 'w',  newline='')
        writer = csv.DictWriter(f, fieldnames=self.csv_columns)
        writer.writeheader()
        for row in row_list:
            writer.writerow(row)

        f.close()
    # end def
# end class


class FitsImage:
    def __init__(self, file_path, file_name):
        self.file_path = file_path
        self.file_name = file_name
        self.fits_file = fits.open(self.file_path)

    def get_object(self):
        return self.fits_file[0].header['OBJECT']

    def get_filter(self):
        return self.fits_file[0].header['FILTER']

    def get_sensor_temp(self):
        return self.fits_file[0].header['CCD-TEMP']

    def get_focus_temp(self):
        return self.fits_file[0].header['FOCTEMP']

    def get_focus_position(self):
        return self.fits_file[0].header['FOCPOS']

    def get_ra(self):
        return self.fits_file[0].header['OBJCTRA']

    def get_dec(self):
        return self.fits_file[0].header['OBJCTDEC']

    def get_binning(self):
        return self.fits_file[0].header['XBINNING']


def main(args):

    extractor = FitsHeaderExtractor(args.inputfolder, args.outputcsvfile)
    list = extractor.load()
    extractor.write(list)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Log watch-dog to lookout for text and call a .bat file if it appears')
    parser.add_argument('inputfolder', type=str, help='The folder containing FITS files')
    parser.add_argument('outputcsvfile', type=str, help='The output location of the CSV file')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')

    args = parser.parse_args()
    main(args)
