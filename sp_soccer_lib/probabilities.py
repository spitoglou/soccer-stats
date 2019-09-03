import math


def convert_dec_to_prob(dec: float):
    return round(1 / dec, 4)


def convert_prob_to_dec(prob: float):
    return round(1 / prob, 4)


def convert_frac_to_prob(nom: int, denom: int):
    return round(1 - (nom / (nom + denom)), 4)


def convert_frac_to_dec(nom: int, denom: int):
    return round(1 / (1 - (nom / (nom + denom))), 4)


def exact_binomial_probability(number_of_trials: int, number_of_successes: int, success_probability: float):
    n_choose_k = math.factorial(number_of_trials) / (math.factorial(
        number_of_successes) * math.factorial(number_of_trials - number_of_successes))
    exact = n_choose_k * (success_probability**number_of_successes) * \
        ((1 - success_probability)**(number_of_trials - number_of_successes))
    return exact


def cumulative_binomial_probabilities(number_of_trials: int, number_of_successes: int, success_probability: float):
    X_lt_x = 0
    X_lt_eq_x = 0
    X_gt_x = 0
    X_gt_eq_x = 0
    for i in range(number_of_trials + 1):
        exact = exact_binomial_probability(
            number_of_trials, i, success_probability)
        if i < number_of_successes:
            X_lt_x += exact
            X_lt_eq_x += exact
        elif i == number_of_successes:
            X_lt_eq_x += exact
            X_gt_eq_x += exact
        elif i > number_of_successes:
            X_gt_x += exact
            X_gt_eq_x += exact

    return X_lt_x, X_lt_eq_x, X_gt_x, X_gt_eq_x


if __name__ == '__main__':
    print(exact_binomial_probability(10, 1, 0.1))
    print(cumulative_binomial_probabilities(10, 1, 0.1))
