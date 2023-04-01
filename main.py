from owlready2 import *

namespace = "http://test.org/onto.owl"

onto = get_ontology(namespace)


class User(Thing):
    ontology = onto

    def __init__(self, name=None, age=None, email=None) -> None:
        super().__init__()
        self.name = name
        self.age = age
        self.email = email

    def __repr__(self):
        return f"User(name='{self.name}', age='{self.age}', email='{self.email}')"


class FriendOf(ObjectProperty):
    ontology = onto
    domain = [User]
    range = [User]


onto.load()

user1 = User(name="Alice", age=25, email="alice@example.com")
user2 = User(name="Bob", age=30, email="bob@example.com")

onto.User1(user1)
onto.User2(user2)

onto.sync_reasoner()

onto.save(file="ontology.owl")
