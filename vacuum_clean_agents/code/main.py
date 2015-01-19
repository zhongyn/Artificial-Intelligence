from agent import *
from environment import *
from helper import *

def main():
    # Initial environment
    width = 10
    height = 10
    home = Vector(0,0)
    direction = Vector(0,1)
    room = Environment(width, height, home)

    # Simple reflex agent
    simple_agent = SimpleReflexAgent(home, direction)
    simple_agent.run(room)

    print "hello"
if __name__ == '__main__':
    main()




