import matplotlib.pyplot as plt

# Define the minsupp values and the corresponding execution times
minsupp_values = [50, 75, 100, 125, 150, 200]
times_frequent_itemsets = []

# Read the result files
for i in range(1, 7):
    with open(f'info{i}.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith('Time in seconds to find the frequent itemsets'):
                time = float(line.split(':')[1].strip())
                times_frequent_itemsets.append(time)

# Plot time vs minsupp
plt.plot(minsupp_values, times_frequent_itemsets, marker='o', color='b', label="Time for Frequent Itemsets")
plt.xlabel('Minimum Support Count')
plt.ylabel('Time To Generate Frequent Itemsets (seconds)')
plt.title('Time Required vs Minimum Support')
plt.grid(True)
plt.legend()
plt.show()

# Define the minsupp values and the count of frequent itemsets generated
frequent_itemsets_count = []

# Read the result files
for i in range(1, 7):   # Files info1.txt to info6.txt
    with open(f'info{i}.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith('Total number of frequent itemsets'):
                count = int(line.split(':')[1].strip())
                frequent_itemsets_count.append(count)

# Plot number of frequent itemsets vs minsupp
plt.plot(minsupp_values, frequent_itemsets_count, marker='o', color='g', label="Number of Frequent Itemsets")
plt.xlabel('Minimum Support Count')
plt.ylabel('Number of Frequent Itemsets')
plt.title('Number of Frequent Itemsets vs Minimum Support')
plt.grid(True)
plt.legend()
plt.show()

# Define the minconf values
minconf_values = [0.7, 0.75, 0.8, 0.85, 0.9]
rules_count = []

# Read the result files
for i in range(7, 12):  # Files info7.txt to info11.txt
    with open(f'info{i}.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith('Number of high-confidence rules'):
                count = int(line.split(':')[1].strip())
                rules_count.append(count)

# Plot number of rules vs minconf
plt.plot(minconf_values, rules_count, marker='o', color='r', label="Number of High-Confidence Rules")
plt.xlabel('Minimum Confidence Threshold')
plt.ylabel('Number of Rules')
plt.title('Number of Rules vs Confidence Thresholds (minsupp=80)')
plt.grid(True)
plt.legend()
plt.show()