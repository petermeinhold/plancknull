import numpy as np
import logging as log
import healpy as hp
from glob import glob
import os
from differences import halfrings, surveydiff, chdiff 
import sys

try:
    INPUT_PATH = os.environ["DX9_LFI"]
except KeyError:
    sys.stderr.write("You must set the environment variable DX9_LFI to the\n"
                     "path containing the data release files.\n")
    sys.exit(1)

try:
    READER = os.environ["NULLTESTS_ENV"]
except KeyError:
    sys.stderr.write("You must set the environment variable NULLTESTS_ENV\n"
                     "either to 'NERSC' or 'LFIDPC', according to the\n"
                     "system under which you are running the script\n")
    sys.exit(1)

if READER not in ('NERSC', 'LFIDPC'):
    sys.stderr.write("Invalid value for $NULLTESTS_ENV (\"{0}\")\n"
                     .format(READER))
    sys.exit(1)

if READER == "NERSC":
    from reader import SingleFolderDXReader as MapReader
else:
    from reader import DPCDX9Reader as MapReader


def read_dpc_masks(freq):
    if freq > 70:
        nside = 2048
    else:
        nside = 1024
    ps_mask = np.logical_not(np.floor(hp.ud_grade( 
    hp.read_map(
        glob(os.path.join(INPUT_PATH, "MASKs",'mask_ps_%dGHz_*.fits' % freq))[0]), nside))
    ).astype(np.bool)
    gal_filename = glob(os.path.join(
        os.environ["DX9_LFI"], "MASKs",
        'destripingmask_%d.fits' % freq))[0]
    gal_mask = np.logical_not(hp.read_map(gal_filename)).astype(np.bool)
    return ps_mask, gal_mask

HORNS = {30:[27,28], 44:[24,25,26], 70:list(range(18,23+1))}

def chlist(freq):
    horns = HORNS[freq]
    chs = []
    for horn in horns:
        chs += ["LFI%dM" % horn, "LFI%dS" % horn]
    return chs

NSIDE = 1024

log.root.level = log.DEBUG
mapreader = MapReader(INPUT_PATH)

#print "HALFRINGS"
#survs = ["nominal", "full"]
#freqs = [30,44,70]
#for freq in freqs:
#    smooth_combine_config = dict(fwhm=np.radians(1.), degraded_nside=128)
#    chtags = [""]
#    if freq == 70:
#        chtags += ["18_23", "19_22", "20_21"]
#    for chtag in chtags:
#        for surv in survs:
#            halfrings(freq, chtag, surv, pol='IQU', smooth_combine_config=smooth_combine_config, mapreader=mapreader, output_folder="dx9/halfrings/",read_masks=read_dpc_masks, log_to_file=False)

#print "SURVDIFF"
#survs = [1,2,3,4,5]
#freqs = [30, 44, 70]
#for freq in freqs:
#    smooth_combine_config = dict(fwhm=np.radians(1.), degraded_nside=128)
#    chtags = [""]
#    if freq == 70:
#        chtags += ["18_23", "19_22", "20_21"]
#    for chtag in chtags:
#         surveydiff(freq, chtag, survs, pol='IQU', smooth_combine_config=smooth_combine_config, mapreader=mapreader, output_folder="dx9/surveydifft/", read_masks=read_dpc_masks, log_to_file=True)

#print "SURVDIFF, CH"
#survs = [1,2,3,4,5]
#freqs = [70]
#for freq in freqs:
#    ps_mask, gal_mask = read_dpc_masks(freq, NSIDE)
#    smooth_combine_config = dict(fwhm=np.radians(1.), degraded_nside=128,smooth_mask=ps_mask, spectra_mask=gal_mask)
#    chtags = chlist(freq)
#    for chtag in chtags:
#         surveydiff(freq, chtag, survs, pol='I', smooth_combine_config=smooth_combine_config, mapreader=mapreader, output_folder="dx9/surveydiff/")

print "CHDIFF"
survs = [1]
freqs = [30, 44, 70]
freqs = [30]
    
for freq in freqs:
    smooth_combine_config = dict(fwhm=np.radians(1.), 
    degraded_nside=128)
    for surv in survs:
        chdiff(freq, ["LFI%d" % h for h in HORNS[freq]], surv, pol='I', smooth_combine_config=smooth_combine_config, mapreader=mapreader, output_folder="dx9/chdiff/", read_masks=read_dpc_masks)
