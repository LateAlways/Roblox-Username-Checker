from usergen.base.UsernameGeneration import UsernameGeneration


class FromFile(UsernameGeneration):
    def __init__(self, file):
        self.users = []
        with open(file, "r") as f:
            for line in f.readlines():
                self.users.append(line.strip())

    def get_next_user(self):
        if len(self.users) > 0:
            return self.users.pop(0)
        else:
            return
