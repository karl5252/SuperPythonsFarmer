# game/exchange_board.py
class ExchangeBoard:
    """Class to handle animals exchange rates."""
    exchange_rates = {}

    @classmethod
    def set_exchange_rate(cls, from_animal, to_animal, offered_amount, requested_amount):
        """Set exchange rate between two animals using offered and requested amounts."""
        cls.exchange_rates[f"{from_animal}-{to_animal}"] = {
            "offered_amount": offered_amount,
            "requested_amount": requested_amount
        }

    @classmethod
    def get_exchange_rate(cls, from_animal, to_animal):
        """Get exchange rate between two animals."""
        return cls.exchange_rates.get(f"{from_animal}-{to_animal}", {"offered_amount": 0, "requested_amount": 0})

    @classmethod
    def get_all_exchange_rates(cls):
        """Get all exchange rates."""
        return cls.exchange_rates