

class User():
    def __init__(self, name):
        self.name = name

    def buy(self):
        pass

class Seat:
    database = ""
    def __init__(self, seat_id, price):
        self.seat_id = seat_id
        self.price = price

    def is_free(self):
        pass

    def occupy(self):
        pass


class Card:
    database = ""
    def __init__(self, type, number, cvc, holder):
        self.type = type
        self.number = number
        self.cvc = cvc
        self.holder = holder

    def validate(self, price):
        pass

class Ticket:
    def __init__(self, id, user, price, seat):
        self.id = id
        self.user = user
        self.price = price
        self.seat = seat

    def to_pdf(self, path):
        pass