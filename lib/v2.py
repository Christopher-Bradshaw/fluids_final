#!/usr/bin/env python3
import numpy as np

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
        return 1

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
    print(x)
    x.evolve()
    print(x)

if __name__ == "__main__":
    main()
