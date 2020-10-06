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

def main():
    log.setLevel('ERROR')
    pint.observatory.topo_obs.TopoObs(
        "ata",
        aliases=["hcro"],
        itrf_xyz=[-2524263.18,   -4123529.78,     4147966.36 ]
    )
    target_time = sys.argv[1]
    freq = float(sys.argv[2])
    par_file = sys.argv[3]
    toa_list = []
    target_times = [Time(target_time,format='mjd')]
    freq = [freq]
    for t, f in zip(target_times, freq):
        toa_entry = toa.TOA(t, obs="ata", freq=f)
        toa_list.append(toa_entry)

    toas = toa.get_TOAs_list(toa_list)
    model = get_model(par_file)
    F0_apparent = model.d_phase_d_toa(toas)
    print ("%.13f" % (1.0/F0_apparent.value[0]))
    return 0

if __name__ == '__main__':
    main()

