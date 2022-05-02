import pytest
import lab1
import os.path


def test_create_database():
    lab1.init()
    assert os.path.exists(lab1.db_file) == True


def test_clients_fields():
    assert lab1.Clients.name == True
    assert lab1.Clients.city == True
    assert lab1.Clients.address == True


def test_orders_fields():
    assert lab1.Orders.client == True
    assert lab1.Orders.amount == True
    assert lab1.Orders.date == True
    assert lab1.Orders.description == True


def test_clients_len():
    lab1.fill()
    assert len(lab1.Clients.select()) >= 10


def test_orders_len():
    lab1.fill()
    assert len(lab1.Orders.select()) >= 10