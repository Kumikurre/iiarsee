class DBinterface():
    def __init__(self, engine):
        self.engine = engine
        conn = engine.connect()

<<<<<<< HEAD
    def register_user(self, name, fullname):
        self.name = name
        self.fullname = fullname
        ins = users.insert().values(name, fullname)
        conn.execute(ins)
=======
    def register_user(self):
        pass

>>>>>>> 745a3bc55c4e1a94cc438a637922686bf3e23283
    def remove_user(self):
        pass

    def join_channel(self):
        pass

    def leave_channe(self):
        pass
    