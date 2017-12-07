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
    volLine, = ax.plot(1/x.gaps["volume"][1:], label="Cell Density")
    energyLine, = ax.plot(x.gaps["energy"][1:], label="Cell Energies")
    pressureLine, = ax.plot(x.gaps["pressure"][1:], label="Cell Pressures")
    velLine, = ax.plot(x.grid["velocity"][1:], label="Cell Velocities")
    plt.legend()
    plt.show(block=False)

    while True:
        if i % 1 == 0:
            print(x)
            volLine.set_ydata(1/x.gaps["volume"][1:])
            energyLine.set_ydata(x.gaps["energy"][1:])
            pressureLine.set_ydata(x.gaps["pressure"][1:])
            velLine.set_ydata(x.grid["velocity"][1:])
            ax.relim()
            ax.autoscale_view()
            fig.canvas.draw()
        x.evolve()
        i += 1

if __name__ == "__main__":
    main()
