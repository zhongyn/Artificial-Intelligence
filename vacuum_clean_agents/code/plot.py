import matplotlib.pyplot as pl
import numpy as np

def plot():
    points = np.loadtxt("random_agent_result.txt", delimiter=' ', dtype=int)
    random_agent = np.rint(np.mean(points, axis=0)).astype(int)

    clean_cells = [36, random_agent[0], 100]
    total_actions = [75, random_agent[1], 218]

    ticks = np.arange(1,4)

    wid=0.6
    fig,ax2 = pl.subplots()
    ax2.bar(ticks,clean_cells,width = wid, bottom = 0, color = 'blue', alpha = 0.5)
    ax2.set_xticks(ticks+wid/2)
    ax2.set_xticklabels(total_actions, size=15)
    ax2.set_xlabel("The number of actions taken", size=16)
    ax2.set_ylabel("The total number of clean cells", size=16)
    # ax2.set_ylim([0,120])

    pl.show()

if __name__ == '__main__':
    plot()