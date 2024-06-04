import matplotlib.pyplot as plt
import time
import numpy as np


feedbacks = [[],[],[],[3,2],[4,3],
             [5,3],[6,5],[7,6],[8,6,5,4],[9,5],
             [10,7],[11,9],[12,11,10,4],[13,12,11,8],[14,13,12,2],
             [15,14],[16,14,13,11],[17,14],[18,11],[19,18,17,14],
             [20,17],[21,19],[22,21],[23,18],[24,23,22,17]
            ]


def calculate_lfsr(initNumber, bits):
    num = initNumber # initial number
    maxrounds = 2**bits
    formater = "0" + str(bits) + "b"
    
    rands = []

    for i in range(maxrounds):
        # print(num, "(" , format(num, formater), ")")
        rands.append(num)
        
        a = (num << 1) & (maxrounds-1)
        
        #seems both acceptable, but b=1 would become more complex and difficult to estimate
        b = 1
        # b = 0
        
        for j in range(len(feedbacks[bits])):
            target = feedbacks[bits][j] - 1
            b = ((b & 1) ^ (num >> target) & 1) & 1

        num = a+(b&1)

    return rands


def plot_results_a(rands, bits):
    nums = range(2**bits)
    title_str = "Random number generation ({:d} bits MLS)".format(bits)
    plt.scatter(nums, rands)
    plt.title(title_str)
    plt.xlabel("round")
    plt.ylabel("generated number")
    plt.show()


def plot_results_b(rands, bits):
    title_str = "Random number generation ({:d} bits MLS)".format(bits)
    plt.figure()
    plt.hist(rands, bins=2**bits, range=[0,2**bits])
    plt.title(title_str)
    plt.xlabel("random_number")
    plt.ylabel("counts/bin")
    plt.show()


def random_walk(rands, bits, checkpoints):
    x=0
    pos_at_checkpoints = [0]
    
    for t in range(1, max(checkpoints)+1):
        if rands[(t-1)%(2**bits)] & 1 == 0: # this is the equivalent of "rands[] % 2 == 0"
            x = x+1
        else:
            x = x-1

        if t in checkpoints:
            pos_at_checkpoints.append(x)

    # print(checkpoints)

    return pos_at_checkpoints


def main():
    # this program can calculate from 3 bits to 24 bits, but calculating 24 bits never finishes ! (due to the amount of calculation)

    # change variants under here
    bits = 12
    cycle = 2**bits # but DO NOT CHANGE HERE!
    trials = int(cycle*0.7)
    # trials = 1
    # checkpoints = range(cycle)
    checkpoints = [0,int(0.0375*cycle),int(0.075*cycle),int(0.15*cycle),int(0.3*cycle),int(0.5*cycle),int(0.7*cycle),int(0.85*cycle),int(0.925*cycle),int(0.9625*cycle),cycle]
    checkpoints.sort()
    markers = ['+','x','D','d']
    # change variants above here
    
    all_pos_at_checkpoints = []
    means = []
    stds = []
    
    for i in range(trials):
        init = int(time.time()*1000000) % (2**bits)
        rands = calculate_lfsr(init, bits)
        pos_at_checkpoints = random_walk(rands, bits, checkpoints)
        all_pos_at_checkpoints = np.append(all_pos_at_checkpoints, pos_at_checkpoints, axis=0)

    all_pos_at_checkpoints = np.reshape(all_pos_at_checkpoints, [trials, len(checkpoints)]).astype(np.int64)
    
    for i in range(len(checkpoints)):
        calculating_set = all_pos_at_checkpoints[:, i]
        plt.hist(calculating_set, histtype = "step", label = "steps = {:d}".format(checkpoints[i]))

        mean = np.mean(calculating_set)
        means = np.append(means, mean)
        std = np.std(calculating_set)
        stds = np.append(stds, std)

        print(means, stds)

    plt.title("x position counts vs. x position")
    plt.xlabel("x positions at certain times")
    plt.ylabel("counts/bin")
    plt.yscale("log")
    plt.legend()
    plt.show()

    plt.clf()
    plt.close()

    plt.title("times vs. means at that times")
    plt.xlabel("times")
    plt.ylabel("means of x positions")
    plt.scatter(checkpoints, means)
    plt.show()

    plt.clf()
    plt.close()

    plt.title("times vs. standard deviations at that times")
    plt.xlabel("times")
    plt.ylabel("standard deviations of x positions")
    plt.scatter(checkpoints, stds)
    plt.show()

    
if __name__ == "__main__":
    main()

