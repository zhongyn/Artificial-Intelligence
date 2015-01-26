from agent import *
from environment import *
from helper import *
import numpy as np


def main():
    # Initial environment
    width = 10
    height = 10
    home = Vector(0,0)
    direction = Vector(0,1)

    # Simple reflex agent
    room = Environment(width, height, home)
    simple_agent = SimpleReflexAgent(home, direction)
    simple_agent.run(room)


    # Randomized reflex agent
    trial = 50
    result = np.empty([trial, 2])
    for i in range(trial):    
        room = Environment(width, height, home)
        random_agent = RandomizedReflexAgent(home, direction)
        random_agent.run(room)
        result[i][0] = random_agent.sucks_count
        result[i][1] = random_agent.actions_count

    np.savetxt("random_agent_result.txt", result, fmt='%1d')

    # Model-based reflex agent
    room = Environment(width, height, home)
    model_agent = ModelBasedReflexAgent(home, direction)
    model_agent.run(room)


if __name__ == '__main__':
    main()




