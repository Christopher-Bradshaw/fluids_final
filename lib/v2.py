#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

def getDefaultConfig():
    dx = 1
    width = 5
    gamma = 5/3
    # Densities
    initialRho = np.ones(width) # this will never change
    summedInitialRho = np.array([
        initialRho[i] + initialRho[i+1] for i in range(len(initialRho)-1)
        ])

    # The grid
    grid = np.zeros(width + 1, dtype=[
        ("position", "float64"),
        ("velocity", "float64"),
    ])
    grid["position"] = np.arange(0, width + 1, dx)
    grid["velocity"] = np.ones_like(grid["position"]) / 100
    grid["velocity"][0] = 0
    grid["velocity"][-1] = 0
    # Things defined in the gaps
    gaps = np.zeros(width, dtype=[
        ("volume", "float64"),
        ("vorticity", "float64"),
        ("energy", "float64"),
        ("pressure", "float64"),
    ])
    gaps["volume"] = 1/initialRho
    gaps["vorticity"] = np.zeros(width)
    gaps["energy"] = np.ones(width)
    gaps["pressure"] = getPressure(gaps["energy"], gaps["volume"], gamma)

    return {
            "grid": grid,
            "gaps": gaps,
            "initialRho": initialRho,
            "summedInitialRho": summedInitialRho,
            "dx": dx,
            "width": width,
            "gamma": gamma,
    }

def getPressure(energy, volume, gamma):
    return energy * (gamma - 1) / volume

class OneDFluid():

    def __init__(self, config=None):
        if config is None:
            config = getDefaultConfig()
        # Ideally would just __setattr__ but pylint doesn't like that
        self.grid = config["grid"]
        self.gaps = config["gaps"]
        self.initialRho = config["initialRho"]
        self.summedInitialRho = config["summedInitialRho"]
        self.dx = config["dx"]
        self.width = config["width"]
        self.gamma = config["gamma"]

    def getDeltaT(self):
        return 0.00001

    def evolve(self):
        deltaT = self.getDeltaT()
        newGrid = np.copy(self.grid)
        newGaps = np.copy(self.gaps)

        # Pull velocity from t = -1/2 to t = 1/2
        newGrid["velocity"][1:-1] = self.grid["velocity"][1:-1] - (
                (2 * deltaT / self.summedInitialRho / self.dx) *
                (np.ediff1d(self.gaps["pressure"]) - np.ediff1d(self.gaps["vorticity"]))
        )

        # Pull position from t = 0 to t = 1
        newGrid["position"] = self.grid["position"] + (
                deltaT * newGrid["velocity"]
        )

        # Pull volume from t = 0 to t = 1
        newGaps["volume"] = self.initialRho * (
                np.ediff1d(newGrid["position"]) / self.dx
        )
        # Also define this deltaVolume for each gap
        deltaVolume = newGaps["volume"] - self.gaps["volume"]

        # Get the vorticity in the middle of this timestep
        # I don't think this is pulling? But see comment for my thoughts on vorticity
        a = 1/8 # From Zack in slack.
        gapDeltaVelocity = np.ediff1d(newGrid["velocity"])
        newGaps["vorticity"] = 0.5 * a**2 * (
                np.power(gapDeltaVelocity, 2) *
                ((1 / newGaps["volume"]) + (1 / self.gaps["volume"]))
        )
        newGaps["vorticity"][gapDeltaVelocity > 0] = 0 # things that are expanding have no vorticity



        # Pull energy from t = 0 to t = 1
        newGaps["energy"] = self.gaps["energy"] - (
                (self.gaps["pressure"] - self.gaps["vorticity"]) * deltaVolume
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
