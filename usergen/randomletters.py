from usergen.base.UsernameGeneration import UsernameGeneration


class RandomLetters(UsernameGeneration):
    def __init__(self, start_length=4):
        self.letters = "abcdefghijklmnopqrstuvwxyz"
        self.length = start_length

        self.current_letters = [0 for i in range(self.length)]

    def get_next_user(self):
        current_position = 0
        for letter in range(len(self.current_letters)):
            if self.current_letters[current_position] >= len(self.letters)-1:
                self.current_letters[current_position] = 0
                current_position += 1
            else:
                self.current_letters[current_position] += 1
                break
            if letter == len(self.current_letters) - 1:
                self.length += 1

                self.current_letters = [0 for i in range(self.length)]

        return "".join([self.letters[i] for i in reversed(self.current_letters)])
