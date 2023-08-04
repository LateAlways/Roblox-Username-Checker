from abc import abstractmethod


class UsernameGeneration:
    def __init__(self):
        pass

    def get_next_user(self):
        pass

    def get_next_users(self, number: int):
        l = []
        for i in range(number):
            x = self.get_next_user()
            if x is not None:
                l.append(x)
            else:
                break
        return l
