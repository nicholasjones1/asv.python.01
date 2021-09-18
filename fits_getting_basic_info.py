# astropy.io.fits
# Basic things to do with a FITS file


from astropy.io import fits

# getting familiar with your FITS data


# let's open a FITs file using astropy.io

with fits.open('resources/HATS28B_LIGHT_lum_90s_BIN2_-20C_005_20210913_194430_262_PA271.65_W.FIT', mode='readonly', ignore_missing_end=True) as hdu_list:

    # the fits.open gave us an HDUList object

    # the image contains just one HDU (Header-Data-Unit)
    # the image data is in the primary hdu.data
    print("This FITS file contains " + str(len(hdu_list)) + " HDU")

    print(hdu_list.info())

    print("Programmatically getting the dimensions... The is "
          + str(hdu_list[0].shape[0]) + " by " + str(hdu_list[0].shape[1]))

    # print the values in the header of the first (and only HDU)
    print("HEADER KEY VALUES")
    for key in hdu_list[0].header:
        print(key + ": " + str(hdu_list[0].header[key]))






