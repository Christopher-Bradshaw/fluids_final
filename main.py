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
    x = OneDFluid(config=ic.getPressureConfig())
    i = 0

    fig, ax = plt.subplots()
    volLine, = ax.plot(x.gaps["volume"], label="Cell Volumes")
    energyLine, = ax.plot(x.gaps["energy"], label="Cell Energies")
    pressureLine, = ax.plot(x.gaps["pressure"], label="Cell Pressures")
    plt.legend()
    plt.show(block=False)

    while True:
        if i % 1000 == 0:
            print(x)
            volLine.set_ydata(x.gaps["volume"])
            energyLine.set_ydata(x.gaps["energy"])
            pressureLine.set_ydata(x.gaps["pressure"])
            fig.canvas.draw()
        x.evolve()
        i += 1

if __name__ == "__main__":
    main()
