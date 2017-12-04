#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

# Doesn't stagger things but pretty good: http://jila.colorado.edu/~ajsh/astr5540_12/prob11.pdf
# No code, but useful math http://www2.mpia-hd.mpg.de/~dullemon/lectures/fluiddynamics08/chap_1_hydroeq.pdf

def cell_mean(arr):
    return np.array([ (arr[i] + arr[i+1])/2 for i in range(len(arr)-1)])

def norm(arr):
    return arr / np.mean(arr)

class OneDFluid():
    gamma = 5/3

    nParticles = 100
    width = 100
    deltaT = 1
    massParticle = 1

    def __init__(self):
        # Things that are defined on the cell boundaries
            # and defined on time boundaries
        self.positions = np.linspace(0, self.width, num=self.nParticles+1) # defined on t
            # and defined on time + 1/2
        self.velocities = np.random.normal(0, 0.01, len(self.positions)) # defined of t+1/2
        # hard boundary
        self.velocities[0] = 0
        self.velocities[-1] = 0

        # Things that are defined in the middle of the cells
            # and defined on time boundaries
        self.cell_size = np.ediff1d(self.positions)
        self.densities = self.massParticle / self.cell_size
        self.energies = 0.5 * self.densities * np.power(cell_mean(self.velocities), 2)
        self.pressures = self.get_pressures()

        # sanity check
        self.sanity_checks()

    def get_pressures(self):
        return (self.gamma - 1) * self.densities * self.energies

    def get_time_step(self):
        # 1 = v * t / x, t = x/v
        return np.min(self.cell_size) / np.max(np.abs(self.velocities)) / 10

    def evolve(self):
        self.deltaT = self.get_time_step()

        # Move things defined at t up to t+1
        self.positions += self.velocities * self.deltaT
        self.cell_size = np.ediff1d(self.positions)
        self.densities = self.massParticle / self.cell_size
        self.pressures = self.get_pressures()

        # Move things defined at t+1/2 up to t+3/2
            # something is probably slightly wrong here. A sign. Might also need an energy term?
        self.velocities[1:-1] -= self.deltaT * np.ediff1d(self.pressures) / np.ediff1d(self.densities)


        # Now plot and sanity check
        self.sanity_checks()
        self.plot()

    def plot(self):
        _, ax = plt.subplots()
        ax.plot(norm(self.densities), label="Density")
        ax.plot(norm(self.pressures), label="Pressure")
        ax.plot(norm(self.energies), label="Energy")
        ax.legend()
        plt.show()

    def sanity_checks(self):
        try:
            assert np.all(np.ediff1d(self.positions) == self.cell_size)
            assert np.all(np.ediff1d(self.positions) > 0)
            assert (self.velocities[0] == 0 and self.velocities[-1] == 0)
            assert self.deltaT > 0
            print(np.sum(self.energies))
        except:
            print(self.positions)
            print(self.velocities)
            print(np.ediff1d(self.positions))
            raise


def main():
    x = OneDFluid()
    while True:
        x.evolve()

if __name__ == "__main__":
    main()
