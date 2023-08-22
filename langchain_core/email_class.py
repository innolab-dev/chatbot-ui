class email:
    def __init__(self):
        self.email = "not yet set"

    def set_email(self, email):
        self.email = email

    def get_email(self):
        return self.email


email_class = email()
