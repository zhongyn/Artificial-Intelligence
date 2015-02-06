import matplotlib.pyplot as pl
import numpy as np

def plot(filename, numdisk):
    astar = np.load(filename)

    # print astar['nodes_expanded']

    aver_expanded = np.mean(astar['nodes_expanded'], axis=-1)
    aver_cputime = np.mean(astar['cputime'], axis=-1)
    aver_length = np.mean(astar['solution_length'], axis=-1)

    print aver_expanded
    print aver_cputime
    print aver_length

    wid=0.8
    ticks = np.arange(numdisk)
    disksize = np.arange(4,4+numdisk)
    fig,ax1 = pl.subplots()
    # ax1.set_title('Number of nodes expanded VS ', size=16)
    ax1.bar(ticks, aver_expanded[0], width = wid, bottom = 0, color = 'blue', alpha = 0.5, label='Admissible')
    ax1.bar(ticks, aver_expanded[1], width = wid, bottom = 0, color = 'green', alpha = 0.5, label='Non-admissible')
    ax1.set_xticks(ticks+wid/2)
    ax1.set_xticklabels(disksize, size=16)
    ax1.set_xlabel("number of disks", size=16)
    ax1.set_ylabel("average number of nodes expanded", size=16)
    ax1.set_yscale('log')
    ax1.legend(fancybox=True,loc='best',fontsize=16)

    fig,ax2 = pl.subplots()
    ax2.bar(ticks, aver_cputime[0], width = wid, bottom = 0, color = 'blue', alpha = 0.5, label='Admissible')
    ax2.bar(ticks, aver_cputime[1], width = wid, bottom = 0, color = 'green', alpha = 0.5, label='Non-admissible')
    ax2.set_xticks(ticks+wid/2)
    ax2.set_xticklabels(disksize, size=16)
    ax2.set_xlabel("number of disks", size=16)
    ax2.set_ylabel("average cpu time (s)", size=16)
    ax2.set_yscale('log')
    ax2.legend(fancybox=True,loc='best',fontsize=16)

    pl.show()




if __name__ == '__main__':
    # plot('../data/astar.npy', 5)
    plot('../data/rbfs.npy', 2)


