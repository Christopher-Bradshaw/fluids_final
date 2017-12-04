#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

# Doesn't stagger things but pretty good: http://jila.colorado.edu/~ajsh/astr5540_12/prob11.pdf
# No code, but useful math http://www2.mpia-hd.mpg.de/~dullemon/lectures/fluiddynamics08/chap_1_hydroeq.pdf

class OneDFluid():
    # gamma = 5/3

    nParticles = 100
    width = 100
    deltaT = 1
    massParticle = 1

    def __init__(self):
        # Things that are defined on the cell boundaries
        self.positions = np.linspace(0, self.width, num=self.nParticles+1) # defined on t
        self.velocities = np.random.normal(0, 0.01, len(self.positions)) # defined of t+1/2
        # hard boundary
        self.velocities[0] = 0
        self.velocities[-1] = 0

        # Things that are defined in the middle of the cells
        self.density = self.massParticle / np.ediff1d(self.positions)

    def evolve(self):
        # Move things defined at t up to t+1
        self.positions += self.velocities * self.deltaT
        self.density = self.massParticle / np.ediff1d(self.positions)

        # Move things defined at t+1/2 up to t+3/2

    def plot(self):
        _, ax = plt.subplots()
        ax.plot(self.density, label="Density")
        ax.legend()
        plt.show()

def main():
    x = OneDFluid()
    x.plot()
    x.evolve()
    x.plot()

if __name__ == "__main__":
    main()
