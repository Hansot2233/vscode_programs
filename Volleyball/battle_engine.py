import random
def simulate(team_rating,level):
    enemy=80+level*12+random.randint(-20,20)
    return team_rating+random.randint(0,50)>enemy,enemy
