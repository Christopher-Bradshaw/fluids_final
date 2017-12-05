#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

def getPressure(energy, volume, gamma):
    return energy * (gamma - 1) / volume

class OneDFluid():

    def __init__(self):
        self.dx = 1
        self.width = 5
        self.gamma = 5/3
        #
        self.initialRho = np.ones(self.width) # this will never change
        self.summedInitialRho = np.array([
            self.initialRho[i] + self.initialRho[i+1] for i in range(len(self.initialRho)-1)
            ])

        # The grid
        self.grid = np.zeros(self.width + 1, dtype=[
            ("position", "float64"),
            ("velocity", "float64"),
        ])
        self.grid["position"] = np.arange(0, self.width + 1, self.dx)
        self.grid["velocity"] = np.ones_like(self.grid["position"]) / 100
        self.grid["velocity"][0] = 0
        self.grid["velocity"][-1] = 0
        # Things defined in the gaps
        self.gaps = np.zeros(self.width, dtype=[
            ("volume", "float64"),
            ("vorticity", "float64"),
            ("energy", "float64"),
            ("pressure", "float64"),
        ])
        self.gaps["volume"] = 1/self.initialRho
        self.gaps["vorticity"] = np.zeros(self.width)
        self.gaps["energy"] = np.ones(self.width)
        self.gaps["pressure"] = getPressure(self.gaps["energy"], self.gaps["volume"], self.gamma)

    def getDeltaT(self):
        return 0.00001

    def evolve(self):
        deltaT = self.getDeltaT()
        newGrid = np.copy(self.grid)
        newGaps = np.copy(self.gaps)

        # Pull velocity from t = -1/2 to t = 1/2
        newGrid["velocity"][1:-1] = self.grid["velocity"][1:-1] - (
                (2 * deltaT / self.summedInitialRho / self.dx) *
                (np.ediff1d(self.gaps["pressure"]))
        )

        # Pull position from t = 0 to t = 1
        newGrid["position"] = self.grid["position"] + (
                deltaT * newGrid["velocity"]
        )

        # Pull volume from t = 0 to t = 1
        newGaps["volume"] = self.initialRho * (
                np.ediff1d(newGrid["position"]) / self.dx
        )
        # Also define this deltaV for each gap
        deltaV = newGaps["volume"] - self.gaps["volume"]

        # Get the vorticity in the middle of this timestep
        # I don't think this is pulling? But see comment for my thoughts on vorticity
        newGaps["vorticity"] = np.zeros(self.width) # Fuck vorticity for now

        # Pull energy from t = 0 to t = 1
        newGaps["energy"] = self.gaps["energy"] - (
                (self.gaps["pressure"] - self.gaps["vorticity"]) * deltaV
        )

        # Pull pressure from t = 0 to t = 1
        newGaps["pressure"] = getPressure(newGaps["energy"], newGaps["volume"], self.gamma)

        self.grid = newGrid
        self.gaps = newGaps


    def __str__(self):
        for i in ["position", "velocity"]:
            print("{}: {}".format(i, self.grid[i]))
        for i in ["volume", "pressure", "energy", "vorticity"]:
            print("{}: {}".format(i, self.gaps[i]))
        for i in ["initialRho", "summedInitialRho"]:
            print("{}: {}".format(i, self.__getattribute__(i)))
        return("")


def main():
    x = OneDFluid()
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
