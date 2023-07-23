from abc import abstractmethod


class UsernameGeneration:
    def __init__(self):
        pass

    def get_next_user(self):
        pass

    def get_next_users(self, number: int):
        return [self.get_next_user() for i in range(number)]
