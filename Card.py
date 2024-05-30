class Card:
    def __init__(self, amount):
        self.amount = amount
    
    def pay(self):
        return f"Turn on EFTPOS machine. Amount Owed is ${self.amount}"