"""
    Integration of the Trappist-1 system as in Tamayo et al. 2017
    https://ui.adsabs.harvard.edu/abs/2017ApJ...840L..19T/abstract
    But without turbulence
"""

import rebound, reboundx
import numpy as np
import os
import argparse


#  Useful constants
pi = np.pi
rad = pi/180.
deg = 180./pi

yr = 2*pi
au = 1.
msun = 1.
rsun = 0.00465047
mj = 0.000954588
me = 3.003e-6
rj = 0.10045*rsun
re = rj/11.209
rs = rsun
day2year = 2*pi/365.25
#np.random.seed(1)

def migration_time(rand):
    """ Compute the migration and e-damping timescales """
    ta = 3.e4*yr
    K = np.power(10,rand)
    te = ta/K
    return ta, te


def run_sim(n, verbose=False):
    """ Main Function which creates the simulation and run the integration """

    # If file already exists, delete it
    run_name = 'run'+str(n)
    if os.path.exists(run_name + '.bin'):
        os.remove(run_name + '.bin')

    # Trappist-1 data from Agol et al 2021
    NP = 7
    e_seed = 1.e-4
    i_seed = 0.
    # Star parameters
    ms = 0.0898
    rs = 0.1234*rsun
    # Planet parameters
    mass   = np.array([1.374, 1.308, 0.388, 0.692, 1.039, 1.321, 0.326])*me
    radius = np.array([1.116,1.097,0.788,0.920,1.045,1.129,0.755])*re
    P      = np.array([1.510826, 2.421937, 4.049219, 6.101013, 9.207540, 12.352446, 18.772866])*day2year
    sma    = np.power(P*P*ms/(4*pi*pi), 1./3 )
    ecosw  = np.array([-0.00215, 0.00055, -0.00496, 0.00433, -0.00840, 0.00380, -0.00365])
    esinw  = np.array([0.00217, 0.00001, 0.00267, -0.00461, -0.00051, 0.00128, -0.00002])
    eobs   = np.sqrt(ecosw*ecosw + esinw*esinw)

    # Create initial conditions
    ecc = e_seed*np.ones(NP)
    inc = i_seed*np.ones(NP)
    Omega     = np.array([np.random.uniform(0,2*pi) for i in range(NP)])
    pomega    = np.array([np.random.uniform(0,2*pi) for i in range(NP)])
    longitude = np.array([np.random.uniform(0,2*pi) for i in range(NP)])

    spacing = 1.02 # 2% wide of observed spacing
    dist = 1.2     # How far from observed periods do we start the simulation
    Pinit = np.zeros(NP)
    for ip in range(NP):
        Pinit[ip] = np.power(spacing,ip)*dist*P[ip]

    # Create the simulation
    sim = rebound.Simulation()
    sim.integrator = "WHFast"

    # Add particles
    sim.add(m=ms, r=rs)
    for k in range(NP):
        sim.add(m=mass[k], P=Pinit[k], e=ecc[k], inc=inc[k], Omega=Omega[k], pomega=pomega[k], l=longitude[k])

    sim.move_to_com()
    ps = sim.particles
    sim.dt = 0.05*ps[1].P
    rebx = reboundx.Extras(sim)
    tf = 5.e5*yr
    n_out = 5001
    times = np.linspace(0, tf, n_out)

    # Add extra forces if needed
    flag_gr  = True
    flag_mig = True

    if flag_gr == True:
        gr = rebx.load_force("gr_potential")
        rebx.add_force(gr)
        from reboundx import constants
        gr.params["c"] = constants.C

    if flag_mig == True:
        mig = rebx.load_force("modify_orbits_forces")
        rebx.add_force(mig)
        ta, te = migration_time(np.random.uniform(2.,3.5))
        ps[7].params["tau_a"] = -ta
        for k in range(NP):
            ps[k+1].params["tau_e"] = -te


    # Star the integration loop
    for i,time in enumerate(times):

        ps = sim.particles
        sim.integrate(time)
        orb = sim.calculate_orbits()
        sim.simulationarchive_snapshot(run_name+'.bin')

        # Compare AMD with observed one (assuming inclinations=0)
        amd    = 0.
        amdobs = 0.
        for k in range(NP):
            amd    += ps[k+1].m*np.sqrt(ps[k+1].a) * (1-np.sqrt(1-ps[k+1].e*ps[k+1].e))
            amdobs += ps[k+1].m*np.sqrt(sma[k]) * (1-np.sqrt(1-eobs[k]*eobs[k]))

        # Print stuff if needed
        if verbose:
            print(("{:d} {:.2f} -- " +
            " {:.4f} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f} -- " +
            " {:.4f} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f} -- " +
            " {:.4f} ").format(i, time/yr,
                                orb[0].a,
                                orb[1].a,
                                orb[2].a,
                                orb[3].a,
                                orb[4].a,
                                orb[5].a,
                                orb[6].a,
                                np.power(orb[1].a/orb[0].a, 1.5),
                                np.power(orb[2].a/orb[1].a, 1.5),
                                np.power(orb[3].a/orb[2].a, 1.5),
                                np.power(orb[4].a/orb[3].a, 1.5),
                                np.power(orb[5].a/orb[4].a, 1.5),
                                np.power(orb[6].a/orb[5].a, 1.5),
                                amd/amdobs))



        # Exit simulation if needed
        if (orb[0].a > 1. or orb[0].e > 0.5):
            print("System went instable")
            break
        if orb[0].a < sma[0]:
            print("Inner planet reached its current location")
            break


if __name__ == '__main__':

    description = 'Rebound integration'

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-n,', '--njob', dest='job_number', type=int, default=1,
                        help='Job number', required=False)
    parser.add_argument('-v,', '--verbose', dest='verbose',
                        help='Verbose mode', action='store_true')

    args = parser.parse_args()

    run_sim(args.job_number, verbose=args.verbose)
