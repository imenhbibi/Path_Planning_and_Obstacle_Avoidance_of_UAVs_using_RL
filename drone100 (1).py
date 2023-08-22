import numpy as np
import gym
from gym import spaces
import random

class DroneGridEnv(gym.Env):
    def __init__(self):
        # Define the dimensions of the grid
        self.width = 10 #4
        self.height = 10 #4

        # Define the initial position of the drone
        self.start_x = 0
        self.start_y = 0

        # Define the position of the goal
        self.goal_x = self.width - 1
        self.goal_y = self.height - 1

        # Define the positions of the obstacles
        self.obstacle_positions = [(0,8),(1, 6), (2, 4),(3,2),(4,3),(4,8),(5,6),(6,4),(7,2),(8,0)]#(0,1),(0, 9), (1, 4),(3,8),(3,3),(3,5),(6,6),(3,7),(5,2),(6,9),(9,3)] # [(1, 1), (1, 3), (2, 3), (3, 0)] 
        self.obstacle_numbers = [8, 16, 24, 32, 40, 48, 56, 64, 72, 80]#1,9,14,38,33,35,66,37,52,69,93] #[5, 12, 7, 11]

        # Define the action space
        self.action_space = spaces.Discrete(4)

        # Define the observation space
        self.observation_space = spaces.Discrete(self.width * self.height)

        # Set the initial state of the environment
        self.reset()

    def get_state(self):
        return self.x * self.width + self.y

    def reset(self):
        # Reset the position of the drone to the starting position
        self.x = self.start_x
        self.y = self.start_y

        return self.get_state()

    #def rand(self):
        # Reset the position of the drone to the starting position
     #   self.x = random.randint(0,3)
     #   self.y = random.randint(0,3)

     #   return self.get_state()

    def step(self, action):
        # Move the drone based on the chosen action
        if action == 0:  # Move up
            if (self.y < self.height - 1) : #  and (self.x * self.width + self.y + 1) not in self.obstacle_numbers:
                self.y += 1
        elif action == 1:  # Move down
            if self.y > 0 : #  and (self.x * self.width + self.y - 1)  not in self.obstacle_numbers:
                self.y -= 1
        elif action == 2:  # Move left
            if self.x > 0 : #and ((self.x - 1) * self.width + self.y) not in self.obstacle_numbers:
                self.x -= 1 
        elif action == 3 :  # Move right
            if self.x < self.width - 1 : # and ((self.x + 1) * self.width + self.y)not in self.obstacle_numbers:
                self.x += 1

        # Compute the reward and check if the episode is done
        reward = self._get_reward()
        done = self._is_done()

        # Return the next state, reward, and done flag
        return self.get_state(), reward, done, {}

    def _get_reward(self):
        # Compute the reward based on the current position of the drone
        if (self.x * self.width + self.y) in self.obstacle_numbers:
            # Negative reward for hitting an obstacle
            reward = -1 
        elif self.x == self.goal_x and self.y == self.goal_y:
            # Positive reward for reaching the goal
            reward = 2 #1
        else:
            # Small negative reward for each step
            reward = 0 #-0.01 

        return reward

    def _is_done(self):
        # Check if the episode is done based on the current position of the drone
        if (self.x == self.goal_x and self.y == self.goal_y) or ((self.x * self.width + self.y) in self.obstacle_numbers) : 
            return True
        else:
            return False

