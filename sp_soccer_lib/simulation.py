import numpy as np


def cash_flow_meta(cash_flow: list):
    cumulative = np.cumsum(cash_flow)
    print(cumulative)
    min_cum = np.min(cumulative)
    max_cum = np.max(cumulative)
    print(min_cum, max_cum)
    return min_cum, max_cum


class Simulation:
    def __init__(self):
        pass


if __name__ == "__main__":
    cash_flow_meta([-2, -4, -6, 28.5, -2, -4, -6, 21.0, -2, -4, -6, 20.4, -2, 6.4])
