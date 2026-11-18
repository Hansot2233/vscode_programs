from dataclasses import dataclass
@dataclass
class Player:
    name:str; position:str; rarity:str; attack:int; block:int; receive:int; setting:int; serve:int; level:int=1
    @property
    def strength(self):
        return int((self.attack+self.block+self.receive+self.setting+self.serve)/5*(1+self.level*0.03))
    def to_dict(self): return self.__dict__
