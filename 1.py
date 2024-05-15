import matplotlib.pyplot as plt

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
    nums = range(maxrounds)

    for i in range(maxrounds):
        # print(num, "(" , format(num, formater), ")")
        rands.append(num)
        
        a = (num << 1) & (2**(bits)-1)
        
        #seems both acceptable, but b=1 would become more complex and difficult to estimate
        # b = 1
        b = 0
        
        for j in range(len(feedbacks[bits])):
            target = feedbacks[bits][j] - 1
            b = (b ^ (num >> target)) & 1

        num = a+(b&1)

    return nums, rands, bits

def plot_results_a(nums, rands, bits):
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
    
def main():
    init = 3 # change variants here
    bits = 18 # change variants here
    # this program can calculate from 3 bits to 24 bits, but calculating 24 bits never finishes ! (due to the amount of calculation) 
    local_nums, local_rands, local_bits = calculate_lfsr(init, bits)
    plot_results_a(local_nums, local_rands, local_bits)
    plot_results_b(local_rands, local_bits)
    
if __name__ == "__main__":
    main()

