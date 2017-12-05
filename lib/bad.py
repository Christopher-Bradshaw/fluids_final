import numpy as np
import matplotlib.pyplot as plt

def cell_mean(arr):
    return np.array([ (arr[i] + arr[i+1])/2 for i in range(len(arr)-1)])

def norm(arr):
    return arr / np.mean(arr)

def get_positions():
    # np.linspace(0, self.width, num=self.nParticles+1) # defined on t
    return np.concatenate((
        np.arange(0, 40, 2),
        np.arange(40, 60, 1/3),
        np.arange(60, 101, 2),
    ))

class OneDFluid():
    gamma = 7/3

    nParticles = 100
    width = 100
    deltaT = 1
    massParticle = 1
    work = np.array([])

    def __init__(self):
        # Things that are defined on the cell boundaries
            # and defined on time boundaries
        self.positions = get_positions()

            # and defined on time + 1/2
        self.velocities = np.random.normal(0, 0.01, len(self.positions)) # defined of t+1/2
        # hard boundary
        self.velocities[0] = 0
        self.velocities[-1] = 0

        # Things that are defined in the middle of the cells
            # and defined on time boundaries
        self.cell_size = np.ediff1d(self.positions)
        self.densities = self.massParticle / self.cell_size
        self.energies = np.ones_like(self.densities) # just start with some energy (this is the temperature)
        self.pressures = self.get_pressures()

        # sanity check
        self.plot()
        self.sanity_checks()

    def get_pressures(self):
        return (self.gamma - 1) * self.densities * self.energies

    def get_time_step(self):
        # 1 = v * t / x, t = x/v
        return np.min(self.cell_size) / np.max(np.abs(self.velocities)) / 10

    def evolve(self):
        self.deltaT = self.get_time_step()

        # Move things defined at t up to t+1
            # first the basics
        self.positions += self.velocities * self.deltaT
        self.cell_size = np.ediff1d(self.positions)
        self.densities = self.massParticle / self.cell_size

            # now energies and pressures
            # diff(velocity) > 0 = expansion
        self.work = np.ediff1d(self.velocities) * self.deltaT * self.pressures
        self.energies -= self.work
        self.pressures = self.get_pressures()

        # Move things defined at t+1/2 up to t+3/2
            # something is probably slightly wrong here. A sign. Might also need a work term?
        pressureDV = np.ediff1d(self.pressures) * self.deltaT / np.ediff1d(self.densities)
        workDV = np.ediff1d(self.work) * self.deltaT / np.ediff1d(self.densities)
        self.velocities[1:-1] -= pressureDV + workDV


        # Now plot and sanity check
        self.plot()
        self.sanity_checks()

    def plot(self):
        _, ax = plt.subplots()
        ax.plot(self.densities, label="Density")
        ax.plot(self.velocities, label="Velocities")
        # ax.plot(self.pressures, label="Pressure")
        # ax.plot(self.energies, label="Energy")
        ax.legend()
        plt.show()

    def sanity_checks(self):
        try:
            # Position assertions
            assert np.all(self.densities * self.cell_size) == self.massParticle, "Mass is conserved"
            assert np.sum(self.cell_size) == 100, "Total width is conserved"
            assert np.all(np.ediff1d(self.positions) > 0), "Cells never overlap"
            assert np.all(np.ediff1d(self.positions) == self.cell_size), "We aren't messing up this calc"

            # Velocity assertions
            assert (self.velocities[0] == 0 and self.velocities[-1] == 0)

            # Time assertions
            assert self.deltaT > 0

            # Energy assertions
            if len(self.work):
                assert np.isclose(np.sum(self.work), 0), "No net work"
            assert np.isclose(np.sum(self.energies), 100), "Energy is conserved"

            print("Success!")
        except:
            print(np.sum(self.energies * self.densities))
            print(self.cell_size)
            print(np.sum(self.cell_size))
            # print(np.sum(self.work))
            # print(np.sum(self.densities))
            # print(self.positions)
            # print(self.velocities)
            # print(np.ediff1d(self.positions))
            raise
