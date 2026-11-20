from dataclasses import dataclass
@dataclass
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
    @property
    def strength(self):
        return int(self.prestige_multiplier() * (self.attack+self.block+self.receive+self.setting+self.serve)/5*(1+self.level*0.03))
    def to_dict(self): return self.__dict__
    def prestige_multiplier(self):

        return 1 + (
            self.prestige_level * 0.10
        )
