import numpy as np
from pygame import gfxdraw
from math import sin, cos
import random
from Field import FieldType

class Ant:
    def __init__(self, position_x, position_y, direction_x, direction_y):
        self.position = np.array([position_x, position_y])
        self.direction = self.normalizeVector(np.array([direction_x, direction_y]))
        self.has_food = False
        self.rotation_speed = 90
        self.speed = 1
        self.food_amount = 0
        self.sense_distance = 3

    def correctVector(self, vector, width, height):
        if vector[0] >= width:
            vector[0] = 0
        elif vector[0] < 0:
            vector[0] = width - 1
        if vector[1] >= height:
            vector[1] = 0
        elif vector[1] < 0:
            vector[1] = height - 1

        return vector

    def senseEnvironment(self, fields, width, height):
        right_vector = self.normalizeVector(np.array([-self.direction[1], self.direction[0]])) * self.sense_distance

        

        front_sensor_pos = self.normalizeVector(self.position + self.direction) * self.sense_distance
        left_sensor_pos = self.normalizeVector(front_sensor_pos - right_vector) * self.sense_distance
        right_sensor_pos = self.normalizeVector(front_sensor_pos + right_vector) * self.sense_distance

        front_sensor_pos[0] = int(round(front_sensor_pos[0]))
        front_sensor_pos[1] = int(round(front_sensor_pos[1]))
        left_sensor_pos[0] = int(round(left_sensor_pos[0]))
        left_sensor_pos[1] = int(round(left_sensor_pos[1]))
        right_sensor_pos[0] = int(round(right_sensor_pos[0]))
        right_sensor_pos[1] = int(round(right_sensor_pos[1]))

        front_sensor_pos = self.correctVector(front_sensor_pos, width, height)
        left_sensor_pos = self.correctVector(left_sensor_pos, width, height)
        right_sensor_pos = self.correctVector(right_sensor_pos, width, height)

        left_sensor_index = int(left_sensor_pos[1]) * width + int(left_sensor_pos[0])
        front_sensor_index = int(front_sensor_pos[1]) * width + int(front_sensor_pos[0])
        right_sensor_index = int(right_sensor_pos[1]) * width + int(right_sensor_pos[0])

        left_sensor = fields[left_sensor_index].getValues()
        front_sensor = fields[front_sensor_index].getValues()
        right_sensor = fields[right_sensor_index].getValues()

        return left_sensor + front_sensor + right_sensor
    
    def normalizeVector(self, input_vector):
        output_vector = []
        sum_of_squares = 0
        for value in input_vector:
            sum_of_squares += value * value
        vector_length = np.sqrt(sum_of_squares)
        for value in input_vector:
            output_vector.append(value / vector_length)
        return np.array(output_vector)

    def rotate(self, angle):
        random_angle = random.uniform(-5, 5)
        radians = np.deg2rad(angle + random_angle)
        self.direction = np.array([
            self.direction[0] * cos(radians) - self.direction[1] * sin(radians),
            self.direction[0] * sin(radians) + self.direction[1] * cos(radians)
        ])
        self.direction = self.normalizeVector(self.direction)


    def update(self, fields, width, height):
        position = np.array([int(round(self.position[0])), int(round(self.position[1]))])
        position = self.correctVector(position, width, height)
        field_index = position[1] * width + position[0]

        field = fields[field_index]
        if field.field_content["food"] > 0 and not self.has_food:
            field.takeFood(5)
            self.has_food = True
            self.direction = -self.direction

        if self.has_food:
            field.addPheromone(FieldType.FOOD_PHEROMONE)
        else:
            field.addPheromone(FieldType.HOME_PHEROMONE)
            
        environment = self.senseEnvironment(fields, width, height)

        if self.has_food:
            if environment[1] > environment[4]:
                if environment[1] > environment[7]:
                    self.rotate(-self.rotation_speed)
                else:
                    self.rotate(self.rotation_speed)
            else:
                if environment[4] >= environment[7]:
                    self.rotate(0)
                else:
                    self.rotate(self.rotation_speed)
        else:
            if environment[2] > 0 or environment[5] > 0 or environment[8] > 0:
                if environment[2] > environment[5]:
                    if environment[2] > environment[8]:
                        self.rotate(-self.rotation_speed)
                    else:
                        self.rotate(self.rotation_speed)
                else:
                    if environment[5] >= environment[8]:
                        self.rotate(0)
                    else:
                        self.rotate(self.rotation_speed)
            else:
                if environment[0] > environment[3]:
                    if environment[0] > environment[6]:
                        self.rotate(-self.rotation_speed)
                    else:
                        self.rotate(self.rotation_speed)
                else:
                    if environment[3] >= environment[6]:
                        self.rotate(0)
                    else:
                        self.rotate(self.rotation_speed)
        
        self.position += self.direction * self.speed
        self.position = self.correctVector(self.position, width, height)

    def draw(self, surface):
        gfxdraw.pixel(surface, int(self.position[0]), int(self.position[1]), (255, 255, 255))

    def visitAnthill(self):
        if self.has_food:
            self.has_food = False
            self.food_amount = 0
            self.direction = -self.direction
