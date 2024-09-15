"""Module to handle animals exchange rates."""


class ExchangeBoard:
    """class to handle animals exchange rates."""
    exchange_rates = {}

    @classmethod
    def set_exchange_rate(cls, from_animal, to_animal, ratio):
        """Set exchange rate between two animals."""
        cls.exchange_rates[(from_animal, to_animal)] = ratio

    @classmethod
    def get_exchange_rate(cls, from_animal, to_animal):
        """Get exchange rate between two animals."""
        return cls.exchange_rates.get((from_animal, to_animal), 0)
