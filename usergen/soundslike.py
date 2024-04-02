from usergen.base.UsernameGeneration import UsernameGeneration


class SoundsLike(UsernameGeneration):
    def __init__(self, soundslike: str):
        self.users = []
        resp = requests.get("https://api.rhymezone.com/words?k=rza&arhy=1&max=99999&qe=sl&md=fpdlr&sl="+soundslike)
        rres = resp.json()
        users = []
    
        for x in rres:
            users.append(x["word"])

    def get_next_user(self):
        if len(self.users) > 0:
            return self.users.pop(0)
        else:
            return
