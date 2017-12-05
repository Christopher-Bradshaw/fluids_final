#!/usr/bin/env python3
from lib.bad import OneDFluid


# Doesn't stagger things but pretty good: http://jila.colorado.edu/~ajsh/astr5540_12/prob11.pdf
# No code, but useful math http://www2.mpia-hd.mpg.de/~dullemon/lectures/fluiddynamics08/chap_1_hydroeq.pdf


def main():
    x = OneDFluid()
    while True:
        x.evolve()

if __name__ == "__main__":
    main()
