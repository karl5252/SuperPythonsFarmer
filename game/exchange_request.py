class ExchangeRequest:
    """Class representing an exchange request between two players."""
    def __init__(self, requestor, from_animal, to_animal, amount_offered, amount_wanted, ratio):
        """Initialize the exchange request.
        :param requestor: Player making the request
        :param from_animal: Animal the requestor offers
        :param to_animal: Animal the requestor wants
        :param amount_offered: Amount of the from_animal offered
        :param amount_wanted: Amount of the to_animal wanted
        """

        self.requestor = requestor  # The player making the request
        self.from_animal = from_animal  # Animal the requestor offers
        self.to_animal = to_animal  # Animal the requestor wants
        self.amount_offered = amount_offered # used to calculate ratio
        self.amount_wanted = amount_wanted # used to calculate ratio
        self.ratio = ratio  # Calculated ratio (count1 / count2)
        self.status = "pending"  # Request can be 'pending', 'accepted', 'rejected', or 'invalid'
