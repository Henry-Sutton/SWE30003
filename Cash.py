class Cash:
    def __init__(self, amount):
        self.amount = amount

    def pay(self):
        return f"Open till and calculate change. Amount owed is ${self.amount}"