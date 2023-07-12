from abc import abstractmethod


class UsernameGeneration:
    def __init__(self):
        pass

    @abstractmethod
    def get_next_user(self):
        pass