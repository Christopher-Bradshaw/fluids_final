#!/usr/bin/env python3
import numpy as np
import lib.initialConditions as ic

class OneDFluid():

    def __init__(self, config=None):
        if config is None:
            config = ic.getFlatConfig()
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
                (np.ediff1d(self.gaps["pressure"]) - np.ediff1d(self.gaps["viscocity"]))
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

        # Get the viscocity in the middle of this timestep
        # I don't think this is pulling? But see comment for my thoughts on viscocity
        a = 1/8 # From Zack in slack.
        gapDeltaVelocity = np.ediff1d(newGrid["velocity"])
        newGaps["viscocity"] = 0.5 * a**2 * (
                np.power(gapDeltaVelocity, 2) *
                ((1 / newGaps["volume"]) + (1 / self.gaps["volume"]))
        )
        newGaps["viscocity"][gapDeltaVelocity > 0] = 0 # things that are expanding have no viscocity



        # Pull energy from t = 0 to t = 1
        newGaps["energy"] = self.gaps["energy"] - (
                (self.gaps["pressure"] - self.gaps["viscocity"]) * deltaVolume
        )

        # Pull pressure from t = 0 to t = 1
        newGaps["pressure"] = ic.getPressure(newGaps["energy"], newGaps["volume"], self.gamma)

        self.grid = newGrid
        self.gaps = newGaps


    def __str__(self):
        for i in ["position", "velocity"]:
            print("{}: {}".format(i, self.grid[i]))
        for i in ["volume", "pressure", "energy", "viscocity"]:
            print("{}: {}".format(i, self.gaps[i]))
        for i in ["initialRho", "summedInitialRho"]:
            print("{}: {}".format(i, self.__getattribute__(i)))
        return("")


