class Payment:
    def __init__(self, order_id, payment_method):
        self.order_id = order_id
        self.payment_method = payment_method
    
    def make_payment(self):
        return self.payment_method.pay()