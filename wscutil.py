import argparse
import os
import os.path
from subprocess import check_output
from time import sleep

from astropy.io import fits
import astropy.wcs as wcs

class WCSProcessor:
    def __init__(self, inputpath, outputpath, fov):
        self.inputpath = inputpath
        self.outputpath = outputpath
        self.fov = fov
    # end def

    def process_folder(self):
        for file_name in os.listdir(self.inputpath):
            input_file_path = os.path.join(self.inputpath, file_name)

            if os.path.isdir(input_file_path):
                # ignore sub-folders
                continue

            if not input_file_path.endswith('.FIT') and not input_file_path.endswith('.fit'):
                # only process FIT files
                continue

            output_file_name = self.get_wcs_file_name(file_name)
            output_file_path = os.path.join(self.outputpath, output_file_name)

            if os.path.exists(output_file_path):
                print("Output file " + output_file_path + " already exists")
                continue

            self.process_fits_file(input_file_path, output_file_path)

    # end def

    def process_fits_file(self, input_file_path, output_file_path):
        print("\n\n")
        print("output_file_path: " + output_file_path)
        wcs_file_name = output_file_path.replace("-WCS.FIT", "")
        wcs_file_name = wcs_file_name.replace("-WCS.fit", "")
        wcs_file_name = wcs_file_name.replace(".", "_")
        print("   wcs_file_name: " + wcs_file_name)

        self.generate_wcs_for_fits_file(input_file_path, wcs_file_name)

        wcs_file_name = wcs_file_name + ".wcs"
        print("looking for " + wcs_file_name)
        if os.path.exists(wcs_file_name):
            wcs_header = self.get_wcs_headers(wcs_file_name)
            #for key in wcs_header:
            #    print("WCS " + key + " " + str(wcs_header[key]))

            with fits.open(input_file_path, mode='readonly', ignore_missing_end=True) as hdu_list:
                self.map_wcs_header_to_original(wcs_header, hdu_list[0].header)
                # save
                hdu_list.writeto(output_file_path)
                hdu_list.close()
                print("generated " + output_file_path)
        else:
            print("file " + output_file_path + " not generated")

        # end if
    # end def

    def map_wcs_header_to_original(self, wcs_header, original_header):
        original_header["CRPIX1"] = wcs_header["CRPIX1"]
        original_header["CRPIX2"] = wcs_header["CRPIX2"]

        # coordinate at reference point
        original_header["CRVAL1"] = wcs_header["CRVAL1"]
        original_header["CRVAL2"] = wcs_header["CRVAL2"]

        # coordinate increment at reference point
        original_header["CDELT1"] = wcs_header["CDELT1"]
        original_header["CDELT2"] = wcs_header["CRPIX2"]

        # rotational correction
        original_header["CROTA1"] = wcs_header["CROTA1"]
        original_header["CROTA2"] = wcs_header["CROTA2"]

        original_header["CD1_1"] = wcs_header["CD1_1"]
        original_header["CD1_2"] = wcs_header["CD1_2"]
        original_header["CD2_1"] = wcs_header["CD2_1"]
        original_header["CD2_2"] = wcs_header["CD2_2"]
    # def end

    @staticmethod
    def get_wcs_headers(file_path: str):
        with fits.open(file_path, mode='readonly', ignore_missing_end=True) as hdu_list:
            return hdu_list[0].header
        return None
    # end def

    def generate_wcs_for_fits_file(self, source_fits_path: str, output_file_path):
        print("generating wcs for " + source_fits_path)
        # build cmd
        cmd = "astap_cli -f " + source_fits_path + " -wcs -fov " + self.fov + " -o " + output_file_path
        output = check_output(cmd, shell=True).decode()
        print(output)

        if 'Solution found' in output:
            return True
        return False
    # end def

    @staticmethod
    def get_wcs_file_name(source_fits_path: str):
        name = source_fits_path
        if ".FIT" in source_fits_path:
            return source_fits_path.replace(".FIT", "-WCS.FIT")
        if ".fit" in source_fits_path:
            return source_fits_path.replace(".fit", "-wcs.fit")
        return None
    # end def

# end class


def main(args):
    wcs_processor = WCSProcessor(args.inputfolder, args.outputfolder, args.fov)
    wcs_processor.process_folder()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Log watch-dog to lookout for text and call a .bat file if it appears')
    parser.add_argument('inputfolder', type=str, help='The folder containing FITS files to solve and calc WCS')
    parser.add_argument('-o', '--outputfolder', type=str, help='The output location updated FITS files')
    parser.add_argument('-f', '--fov', type=str, help='arc/sec of your imaging system in seconds per pixel for example 1.2')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')

    args = parser.parse_args()
    main(args)