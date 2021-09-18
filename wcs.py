from astropy.io import fits
import astropy.wcs as wcs


def get_wcs_headers(fits_file_path: str):
    with fits.open(fits_file_path, mode='readonly', ignore_missing_end=True) as hdu_list:
        return hdu_list[0].header
    return None
# end def


with fits.open('resources/HATS28B_LIGHT_lum_90s_BIN2_-20C_005_20210913_194430_262_PA271.65_W.FIT', mode='readonly', ignore_missing_end=True) as hdu_list:

    wcs_header = get_wcs_headers("resources/HATS28B_LIGHT_lum_90s_BIN2_-20C_005_20210913_194430_262_PA271.65_W.wcs")

    #
    hdu_list[0].header["CRPIX1"] = wcs_header["CRPIX1"]
    hdu_list[0].header["CRPIX2"] = wcs_header["CRPIX2"]

    # coordinate at reference point
    hdu_list[0].header["CRVAL1"] = wcs_header["CRVAL1"]
    hdu_list[0].header["CRVAL2"] = wcs_header["CRVAL2"]

    # coordinate increment at reference point
    hdu_list[0].header["CDELT1"] = wcs_header["CDELT1"]
    hdu_list[0].header["CDELT2"] = wcs_header["CRPIX2"]

    # rotational correction
    hdu_list[0].header["CROTA1"] = wcs_header["CROTA1"]
    hdu_list[0].header["CROTA2"] = wcs_header["CROTA2"]

    hdu_list[0].header["CD1_1"] = wcs_header["CD1_1"]
    hdu_list[0].header["CD1_2"] = wcs_header["CD1_2"]
    hdu_list[0].header["CD2_1"] = wcs_header["CD2_1"]
    hdu_list[0].header["CD2_2"] = wcs_header["CD2_2"]

    w = wcs.WCS(hdu_list[0].header, hdu_list)
    ra, dec = w.all_pix2world([1116], [900], 1)
    print(ra)
    print(dec)

    # punch in the coorindates of an object that believe is in your image
    ra, dec = w.wcs_world2pix(284.39967, -49.13847, 1)
    #ra, dec = w.wcs_world2pix(ra, dec, 1)
    print(ra)
    print(dec)

    hdu_list.close()



