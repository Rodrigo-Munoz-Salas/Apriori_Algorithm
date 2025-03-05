import matplotlib.pyplot as plt

# Define the minsupp values and the corresponding execution times
minsupp_values = [50, 75, 100, 125, 150, 200]
times_frequent_itemsets = []
q1q2= './data/q2q3/'
q4= './data/q4/'

# Read the result files
for i in range(1, 7):
    with open(f'{q1q2}info{i}.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith('Time in seconds to find the frequent itemsets'):
                time = float(line.split(':')[1].strip())
                times_frequent_itemsets.append(time)
# Define colors
background_color = "#213153" # Dark blue background
line_color = "#aabee4" # Light blue line
marker_color = "#c59b41" #Gold marker

# Set figure background color
plt.figure(facecolor = background_color)

# Plot time vs minsupp
plt.plot(minsupp_values, times_frequent_itemsets, marker='o', color=line_color, markerfacecolor=marker_color, markersize=8, label="Time for Frequent Itemsets")
plt.xlabel('Minimum Support Count', color='white')
plt.ylabel('Time To Generate Frequent Itemsets (seconds)', color='white')
plt.title('Time Required vs Minimum Support', color='white')
plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
plt.legend(edgecolor= 'white')

# Set tick colors
plt.xticks(color='white')
plt.yticks(color='white')
plt.show()

# Define the minsupp values and the count of frequent itemsets generated
frequent_itemsets_count = []

# Read the result files
for i in range(1, 7):   # Files info1.txt to info6.txt
    with open(f'{q1q2}info{i}.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith('Total number of frequent itemsets'):
                count = int(line.split(':')[1].strip())
                frequent_itemsets_count.append(count)

# Set figure background color
plt.figure(facecolor = background_color)

# Plot number of frequent itemsets vs minsupp
plt.plot(minsupp_values, frequent_itemsets_count, marker='o',color=line_color, markerfacecolor=marker_color, markersize=8, label="Number of Frequent Itemsets")
plt.xlabel('Minimum Support Count', color='white')
plt.ylabel('Number of Frequent Itemsets', color = 'white')
plt.title('Number of Frequent Itemsets vs Minimum Support', color = 'white')
plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
plt.legend(edgecolor= 'white')

# Set tick colors
plt.xticks(color='white')
plt.yticks(color='white')
plt.show()

# Define the minconf values
minconf_values = [0.7, 0.75, 0.8, 0.85, 0.9]
rules_count = []

# Read the result files
for i in range(7, 12):  # Files info7.txt to info11.txt
    with open(f'{q4}info{i}.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith('Number of high-confidence rules'):
                count = int(line.split(':')[1].strip())
                rules_count.append(count)

# Set figure background color
plt.figure(facecolor=background_color)

# Plot number of rules vs minconf
plt.plot(minconf_values, rules_count, marker='o', color=line_color, markerfacecolor=marker_color, markersize=8, label="Number of High-Confidence Rules")
plt.xlabel('Minimum Confidence Threshold', color='white')
plt.ylabel('Number of Rules', color='white')
plt.title('Number of Rules vs Confidence Thresholds (minsupp=80)', color='white')
plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
plt.legend(edgecolor= 'white')

# Set tick colors
plt.xticks(color='white')
plt.yticks(color='white')
plt.show()