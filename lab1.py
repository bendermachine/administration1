import sys
import peewee as pw
from random import randint, choice
from faker import Faker

db_file = 'orders.db'
db = pw.SqliteDatabase(db_file)

fake = Faker('ru_RU')
Faker.seed(randint(1, 99))

class Clients(pw.Model):
    client_id = pw.PrimaryKeyField()
    name = pw.CharField()
    city = pw.CharField()
    address = pw.CharField()

    class Meta:
        database = db


class Orders(pw.Model):
    order_id = pw.PrimaryKeyField()
    client = pw.ForeignKeyField(Clients)
    date = pw.DateField()
    amount = pw.IntegerField()
    description = pw.CharField()

    class Meta:
        database = db


def create_tables():
    with db:
        db.create_tables([Clients, Orders])


def help():
    print("Допустимые параметры:\n\tinit -- 2.\n\tfill -- 3.\n\tshow [table_name] -- 4.\n")


def init():
    with db:
        if db.get_tables():
            db.drop_tables([Clients, Orders])
        create_tables()


def fill():
    for _ in range(20):
        client = Clients.create(name=fake.name(), city=fake.city(), address=fake.address())
    db.commit()
    for _ in range(20):
        order = Orders.create(client=Clients.get_by_id(randint(1,10)), date=fake.date(), amount=randint(1,20), description=fake.paragraph(nb_sentences=randint(2, 5)))
    db.commit()


def show(table_name=''):
    table = db.get_tables()
    if table_name.lower() in ['clients', 'orders']:
        print(table_name.lower())
        if table_name == 'clients':
            print("client_id\t\tname\t\tcity\t\taddress")
            clients = Clients.select()
            for client in clients:
                print(f"{client.client_id}\t{client.name}\t{client.city}\t{client.address}")
        else:
            print("order_id client_id date\t   amount\tdescription")
            orders = Orders.select()
            for order in orders:
                print(f"{order.order_id}\t{order.client}\t{order.date}\t{order.amount}\t{order.description}")
    else:
        print("Такой таблицы не существует")
        help()

print("+++++++")
if __name__ == "__main__":
    if len(sys.argv) == 1:
        help()
    elif sys.argv[1] == '2':
        init()
    elif sys.argv[1] == '3':
        fill()
    elif sys.argv[1] == '4':
        if len(sys.argv) == 3:
            show(sys.argv[2])
        else:
            show()
