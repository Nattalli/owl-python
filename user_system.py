from owlready2 import *

onto = get_ontology("https://test.org/onto.owl")


class User(Thing):
    namespace = onto

    def display_info(self) -> None:
        print(f"User: {self.name}, Age: {self.age}, Age Group: {self.hasAgeGroup.name}, User Groups: {[group.name for group in self.memberOf]}")


class AgeGroup(Thing):
    namespace = onto

    def display_users(self) -> None:
        users = [user for user in User.instances() if user.hasAgeGroup == self]
        print(f"Users in {self.name} age group:")
        for user in users:
            print(user.name)


class UserGroup(Thing):
    namespace = onto

    def display_members(self) -> None:
        print(f"Members of {self.name}:")
        for relation in memberOf.get_relations():
            if relation[1] == self:
                print(relation[0].name)



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


def create_user(user_id: str, user_name: str, user_age: int, user_age_group: AgeGroup) -> User:
    new_user = User(user_id)
    new_user.name = user_name
    new_user.age = user_age
    new_user.hasAgeGroup = user_age_group
    return new_user


first_user = create_user("first_user", "Alina", 17, teenagers)
second_user = create_user("second_user", "Bohdan", 16, teenagers)
third_user = create_user("third_user", "Vlad", 25, adults)

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

first_user.display_info()
second_user.display_info()
third_user.display_info()

teenagers.display_users()
adults.display_users()

first_group.display_members()
second_group.display_members()
