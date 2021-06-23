from pygame import gfxdraw
from enum import Enum

class FieldType(Enum):
    FOOD = 1
    FOOD_PHEROMONE = 2
    HOME_PHEROMONE = 4

class Field:
    def __init__(self, evaporation_speed=5):
        self.field_content = {
            "food" : 0,
            "food_pheromone" : 0,
            "home_pheromone" : 0,
        }
        self.evaporation_speed = evaporation_speed

    def draw(self, surface, x, y):
        gfxdraw.pixel(surface, x, y, (int(self.field_content["food_pheromone"]), self.field_content["food"], int(self.field_content["home_pheromone"])))

    def update(self):
        if self.field_content["food_pheromone"] > 0:
            self.field_content["food_pheromone"] -= self.evaporation_speed
        if self.field_content["food_pheromone"] < 0:
            self.field_content["food_pheromone"] = 0

        if self.field_content["home_pheromone"] > 0:
            self.field_content["home_pheromone"] -= self.evaporation_speed
        if self.field_content["home_pheromone"] < 0:
            self.field_content["home_pheromone"] = 0

    def getValues(self):
        return (self.field_content["food_pheromone"], self.field_content["home_pheromone"], self.field_content["food"])

    def addPheromone(self, type):
        if type == FieldType.FOOD_PHEROMONE:
            self.field_content["food_pheromone"] = 255
        elif type == FieldType.HOME_PHEROMONE:
            self.field_content["home_pheromone"] = 255
            
    def takeFood(self, amount):
        taken_amount = min(self.field_content["food"], amount)
        self.field_content["food"] -= taken_amount
        return taken_amount

    def addFood(self, amount):
        max_amount = min(255 - self.field_content["food"], amount)
        self.field_content["food"] += max_amount

