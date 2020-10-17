#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  spin_predict.py
#  
#  Copyright 2020 Marcus D. Leech <mleech@localhost.localdomain>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
from pint import toa
from pint.models import get_model
from astropy.time import Time
from astropy import log
import pint.observatory.topo_obs
import pint
import sys
import argparse
import time

def main():
    log.setLevel('ERROR')
    
    
    pint.observatory.topo_obs.TopoObs(
        "ata",
        aliases=["hcro"],
        itrf_xyz=[-2524263.18,   -4123529.78,     4147966.36 ]
    )
    obsname = "ata"
    newargs = False
    for a in sys.argv:
        if ("--" in a):
            newargs = True
            break
    if (newargs == False):
        target_time = sys.argv[1]
        freq = float(sys.argv[2])
        par_file = sys.argv[3]
    
    else:
        parser = argparse.ArgumentParser(description="A predictor of pulsar spin")
        parser.add_argument ("--mjd", type=float, default=(time.time()/86400.0)+40587,
            help="The current Mean Julian Date")
        parser.add_argument ("--freq", type=float, default=408.0,
            help="Center frequency, in Hz")
        parser.add_argument ("--parfile", type=str, required=True,
            help="Name of .PAR file")
        
        parser.add_argument("--localxyz", type=str, default=None)
        
        args = parser.parse_args()
        target_time = "%-8.2f" % args.mjd
        freq = args.freq
        par_file = args.parfile
        
        if (args.localxyz != None):
            s = args.localxyz
            s = xyz.split(",")
            xyz = []
            for x in s:
                xyz.append(float(s))

            pint.observatory.topo_obs.TopoObs(
                "local",
                itrf_xyz=xyz
            )
            obsname = "local"

    toa_list = []
    target_times = [Time(target_time,format='mjd')]
    freq = [freq]
    for t, f in zip(target_times, freq):
        toa_entry = toa.TOA(t, obs=obsname, freq=f)
        toa_list.append(toa_entry)

    toas = toa.get_TOAs_list(toa_list)
    model = get_model(par_file)
    F0_apparent = model.d_phase_d_toa(toas)
    print ("%.13f" % (1.0/F0_apparent.value[0]))
    return 0

if __name__ == '__main__':
    main()

