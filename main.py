#!/usr/bin/env python3
from lib.v2 import OneDFluid
import lib.initialConditions as ic
import matplotlib.pyplot as plt

"""
Current state

Things appear to mostly work.
Except when I start with a density imbalance...
I think the issue there is setting initial viscocity
"""

def main():
    # x = OneDFluid(config=ic.getShockTubeConfig())
    x = OneDFluid(config=ic.getSedovConfig())
    i = 0

    fig, ax = plt.subplots()
    volLine, = ax.plot(1/x.gaps["volume"], label="Cell Density")
    energyLine, = ax.plot(x.gaps["energy"], label="Cell Energies")
    pressureLine, = ax.plot(x.gaps["pressure"], label="Cell Pressures")
    velLine, = ax.plot(x.grid["velocity"], label="Cell Velocities")
    plt.legend()
    plt.show(block=False)

    while True:
        if i % 1 == 0:
            print(x)
            volLine.set_ydata(1/x.gaps["volume"])
            energyLine.set_ydata(x.gaps["energy"])
            pressureLine.set_ydata(x.gaps["pressure"])
            velLine.set_ydata(x.grid["velocity"])
            ax.relim()
            ax.autoscale_view()
            fig.canvas.draw()
            input()
        x.evolve()
        i += 1

if __name__ == "__main__":
    main()
