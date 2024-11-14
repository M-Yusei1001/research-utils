class Bayes:
    """
    Generates Bayes class

    Constructors
    ------------
    **all_probability** : float
    """

    def __init__(self, all_probability: float) -> None:
        self.all_probability = all_probability

    def posterior_probability(
        self, likelihood: float, prior_probability: float
    ) -> float:
        return (likelihood * prior_probability) / self.all_probability
