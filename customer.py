class Customer:
    def __init__(self, username):
        self.username = username

    def place_order(self):
        return f"Customer {self.username} is placing an order."
