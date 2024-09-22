"""Module to handle animals exchange rates."""


# game/exchange_board.py
class ExchangeBoard:
    """Class to handle animals exchange rates."""
    exchange_rates = {}

    @classmethod
    def set_exchange_rate(cls, from_animal, to_animal, offered_amount, requested_amount):
        """Set exchange rate between two animals using offered and requested amounts."""
        cls.exchange_rates[(from_animal, to_animal)] = (offered_amount, requested_amount)

    @classmethod
    def get_exchange_rate(cls, from_animal, to_animal):
        """Get exchange rate between two animals."""
        return cls.exchange_rates.get((from_animal, to_animal), (0, 0))
