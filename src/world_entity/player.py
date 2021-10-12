from ursina.prefabs.first_person_controller import FirstPersonController


class Player(FirstPersonController):
    def __init__(self, position, init_health):
        super(Player, self).__init__()
        self.position = position
        self.health = init_health
        self.last_max_jump_pos = 0
