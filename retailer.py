from tyre import Tyre

class Retailer:
    """A class that links a retailer to a set of tyres"""
    def __init__(self, retailer: str, tyres: list[Tyre]):
        self.retailer = retailer
        self.tyres = tyres