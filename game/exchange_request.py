class ExchangeRequest:
    """Class representing an exchange request between two players."""
    def __init__(self, requestor, from_animal, to_animal):
        self.requestor = requestor  # The player making the request
        self.from_animal = from_animal  # Animal the requestor offers
        self.to_animal = to_animal  # Animal the requestor wants
        self.status = "pending"  # Request can be 'pending', 'accepted', 'rejected', or 'invalid'
