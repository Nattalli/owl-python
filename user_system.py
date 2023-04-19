from owlready2 import *

onto = get_ontology("https://test.org/onto.owl")

class User(Thing):
    namespace = onto

class AgeGroup(Thing):
    namespace = onto

class UserGroup(Thing):
    namespace = onto

class name(DataProperty):
    namespace = onto
    domain = [User]
    range = [str]

class age(DataProperty, FunctionalProperty):
    namespace = onto
    domain = [User]
    range = [int]

teenagers = AgeGroup("teenagers")
adults = AgeGroup("adults")

class hasAgeGroup(ObjectProperty, FunctionalProperty):
    namespace = onto
    domain = [User]
    range = [AgeGroup]

class memberOf(ObjectProperty):
    namespace = onto
    domain = [User]
    range = [UserGroup]

first_user = User("first_user")
first_user.name = "Alina"
first_user.age = 17

second_user = User("second_user")
second_user.name = "Bohdan"
second_user.age = 16

third_user = User("third_user")
third_user.name = "Vlad"
third_user.age = 25

first_user.hasAgeGroup = teenagers
second_user.hasAgeGroup = teenagers
third_user.hasAgeGroup = adults

first_group = UserGroup("first_group")
second_group = UserGroup("second_group")

first_user.memberOf.append(first_group)
second_user.memberOf.append(first_group)
third_user.memberOf.append(second_group)

with onto:
    class CanCommunicateWith(Property):
        domain = [User]
        range = [User]

def can_communicate(user_first: User, user_second: User) -> bool:
    if user_first.hasAgeGroup == user_second.hasAgeGroup:
        return True
    return False

if can_communicate(first_user, second_user):
    first_user.CanCommunicateWith = [second_user]
    second_user.CanCommunicateWith = [first_user]

if can_communicate(first_user, third_user):
    first_user.CanCommunicateWith = [third_user]
    third_user.CanCommunicateWith = [first_user]

if can_communicate(second_user, third_user):
    second_user.CanCommunicateWith = [third_user]
    third_user.CanCommunicateWith = [second_user]

onto.save(file="onto.owl", format="rdfxml")
