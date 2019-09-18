class DBinterface():
    def __init__(self, engine):
        self.engine = engine
        conn = engine.connect()

    def register_user(self, name, fullname):
        self.name = name
        self.fullname = fullname
        ins = users.insert().values(name, fullname)
        conn.execute(ins)
    def remove_user(self):

    def join_channel(self):

    def leave_channe(self):
        
    