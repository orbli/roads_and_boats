
class Phase:

    def waiting_user_input(self):
        raise NotImplementedError()

    def process(self, game_state):
        raise NotImplementedError()

    def process_command(self, game_state, command):
        raise NotImplementedError()

    def export_state(self):
        raise NotImplementedError()