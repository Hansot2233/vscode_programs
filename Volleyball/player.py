from dataclasses import dataclass
@dataclass(eq=False)
class Player:
    name:str
    position:str
    rarity:str

    attack:int
    block:int
    receive:int
    setting:int
    serve:int

    level:int=1

    attack_level:int=0
    block_level:int=0
    receive_level:int=0
    setting_level:int=0
    serve_level:int=0

    prestige_level:int=0
    coins_spent: int = 0
    @property
    def strength(self):

        return int(
            (
                self.effective_attack +
                self.effective_block +
                self.effective_receive +
                self.effective_setting +
                self.effective_serve
            ) / 5
            *
            (1 + self.level * 0.03)
        )
    def to_dict(self): return self.__dict__
    def prestige_multiplier(self):

        return 1 + (
            self.prestige_level * 0.10
        )

    def prestige_multiplier(self):

        return (
            1 +
            self.prestige_level * 0.10
        )

    @property
    def effective_attack(self):

        return int(
            self.attack *
            self.prestige_multiplier()
        )

    @property
    def effective_block(self):

        return int(
            self.block *
            self.prestige_multiplier()
        )

    @property
    def effective_receive(self):

        return int(
            self.receive *
            self.prestige_multiplier()
        )

    @property
    def effective_setting(self):

        return int(
            self.setting *
            self.prestige_multiplier()
        )

    @property
    def effective_serve(self):

        return int(
            self.serve *
            self.prestige_multiplier()
        )
