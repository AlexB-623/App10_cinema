import sqlite3, random
import string


class User:
    def __init__(self, name):
        self.name = name

    def buy(self, seat, card):
        if seat.is_free():
            if card.validate(price=seat.get_price()):
                seat.occupy()
                ticket = Ticket(user=self, price=seat.get_price(), seat_number=seat_id)
                ticket.to_pdf()
                return "Purchase Successful"
            else:
                return "Invalid Card, please try again"
        else:
            return "Seat taken, sorry"


class Seat:
    database = "cinema.db"
    def __init__(self, seat_id):
        self.seat_id = seat_id

    def get_price(self):
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        cursor.execute("""
        SELECT "price" from "Seat" WHERE "seat_id" = ?
        """, [self.seat_id])
        price = cursor.fetchall()[0][0]
        return price

    def is_free(self):
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        cursor.execute("""
        SELECT "taken" FROM "Seat" WHERE "seat_id" = ?
        """, [self.seat_id])
        result = cursor.fetchall()[0][0]
        #check if the seat is free and return value to occupied
        if result == 0:
            return True
        else:
            return False

    def occupy(self):
        connection = sqlite3.connect(self.database)
        connection.execute("""
            UPDATE "Seat" SET "taken" = "1" WHERE "seat_id" = ?
            """, [self.seat_id])
        connection.commit()
        connection.close()

# a1 = Seat("A1").is_free()
# print(a1)


class Card:
    database = "banking.db"
    def __init__(self, type, number, cvc, holder):
        self.type = type
        self.number = number
        self.cvc = cvc
        self.holder = holder

    def validate(self, price):
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        cursor.execute("""
        SELECT "balance" from "Card" WHERE "number" = ? and "cvc" = ?
        """, [self.number, self.cvc])
        result = cursor.fetchall()

        if result:
            balance = result[0][0]
            if balance >= price:
                connection.execute("""
                UPDATE "Card" SET "balance" = ? WHERE "number" = ? and "cvc" = ?
                """, [balance - price, self.number, self.cvc])
                connection.commit()
                connection.close()
                return True

class Ticket:
    def __init__(self, user, price, seat_number):
        self.id = "".join([random.choice(string.ascii_letters) for n in range(8)])
        self.user = user
        self.price = price
        self.seat = seat_number

    def to_pdf(self):
        pass

if __name__ == "__main__":
    name = input("Please enter your name: ")
    seat_id = input("Please enter your desired seat number: ")
    card_type = input("Please enter your card type: ")
    card_number = input("Please enter your card number: ")
    card_cvc = input("Please enter your card CVC: ")
    card_holder = input("Please enter the name of the card holder: ")

    user = User(name=name)
    seat = Seat(seat_id=seat_id)
    card = Card(type=card_type, number=card_number, cvc=card_cvc, holder=card_holder)

    print(user.buy(seat=seat, card=card))
