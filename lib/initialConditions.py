import numpy as np

def getPressure(energy, volume, gamma):
    return energy * (gamma - 1) / volume

def getFlatConfig():
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
    grid["velocity"] = np.zeros_like(grid["position"])
    grid["velocity"][0] = 0
    grid["velocity"][-1] = 0
    # Things defined in the gaps
    gaps = np.zeros(width, dtype=[
        ("volume", "float64"),
        ("viscocity", "float64"),
        ("energy", "float64"),
        ("pressure", "float64"),
    ])
    gaps["volume"] = 1/initialRho
    gaps["viscocity"] = np.zeros(width)
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

def getVelocityConfig():
    config = getFlatConfig()
    config["grid"]["velocity"][1:-1] += 0.01
    return config

def getShockTubeConfig():
    dx = 1
    width = 100
    gamma = 5/3
    # Densities
    initialRho = np.ones(width) # this will never change
    # initialRho[3] = 1.1
    initialRho[:50] = 1.1
    summedInitialRho = np.array([
        initialRho[i] + initialRho[i+1] for i in range(len(initialRho)-1)
        ])

    # The grid
    grid = np.zeros(width + 1, dtype=[
        ("position", "float64"),
        ("velocity", "float64"),
    ])
    grid["position"] = np.arange(0, width + 1, dx)
    grid["velocity"] = np.zeros_like(grid["position"])
    grid["velocity"][0] = 0
    grid["velocity"][-1] = 0

    # Things defined in the gaps
    gaps = np.zeros(width, dtype=[
        ("volume", "float64"),
        ("viscocity", "float64"),
        ("energy", "float64"),
        ("pressure", "float64"),
    ])
    gaps["volume"] = 1/initialRho
    gaps["viscocity"] = np.zeros(width) # should we / can we give initial viscocity?
    gaps["energy"] = 1 * initialRho
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

def getExpansionConfig():
    dx = 1
    width = 100
    gamma = 5/3
    # Densities
    initialRho = np.ones(width) # this will never change
    # initialRho[3] = 1.1
    initialRho[50:] = 0.1
    summedInitialRho = np.array([
        initialRho[i] + initialRho[i+1] for i in range(len(initialRho)-1)
        ])

    # The grid
    grid = np.zeros(width + 1, dtype=[
        ("position", "float64"),
        ("velocity", "float64"),
    ])
    grid["position"] = np.arange(0, width + 1, dx)
    grid["velocity"] = np.zeros_like(grid["position"])
    grid["velocity"][0] = 0
    grid["velocity"][-1] = 0

    # Things defined in the gaps
    gaps = np.zeros(width, dtype=[
        ("volume", "float64"),
        ("viscocity", "float64"),
        ("energy", "float64"),
        ("pressure", "float64"),
    ])
    gaps["volume"] = 1/initialRho
    gaps["viscocity"] = np.zeros(width) # should we / can we give initial viscocity?
    gaps["energy"] = 1 * initialRho
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

def getSedovConfig():
    dx = 1
    width = 100
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
    grid["velocity"] = np.zeros_like(grid["position"])
    grid["velocity"][0] = 0
    grid["velocity"][-1] = 0

    # Things defined in the gaps
    gaps = np.zeros(width, dtype=[
        ("volume", "float64"),
        ("viscocity", "float64"),
        ("energy", "float64"),
        ("pressure", "float64"),
    ])
    gaps["volume"] = 1/initialRho
    gaps["viscocity"] = np.zeros(width) # should we / can we give initial viscocity?
    gaps["energy"] = 1 * initialRho
    gaps["energy"][0] *= 2
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
