from itertools import chain, combinations
import time
import argparse

class Apriori:
    # Initializing all needed attributes for the output files and requirements
    def __init__(self, min_support, min_confidence):
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.frequent_itemsets = {}
        self.association_rules = []
        self.frequent_itemsets_time = 0
        self.association_rules_time = 0
    
    def generate_candidates(self, itemsets, length):
        """Generate candidate itemsets of given length."""
        candidates = set()
        itemsets_list = list(itemsets)

        # Iterate through each pair of itemsets
        for i in range(len(itemsets_list)):
            for j in range(i + 1, len(itemsets_list)):
                # Merge two itemsets using set union to create a new candidate
                candidate = itemsets_list[i] | itemsets_list[j]
                # Check the created candidate has the desired length and add it to the candidates set
                if len(candidate) == length:
                    candidates.add(candidate)
        return candidates
    
    def get_frequent_itemsets(self, transactions):
        """Find all frequent itemsets that meet the minimum support."""

        # start time
        start_time = time.time()

        # Dictionary to store individual item support counts
        item_counts = {}
        
        # Count support for individual items
        for transaction in transactions:
            for item in transaction:
                # Increment item count
                item_counts[frozenset([item])] = item_counts.get(frozenset([item]), 0) + 1

        # Candidate Pruning: Filter out infrequent items based on the min support count threshold
        self.frequent_itemsets[1] = {}  # Initialize an empty dictionary for 1-item frequent itemsets

        # Iterate through all item counts
        for item, count in item_counts.items():
            # Check if the item's support count meets or exceeds the minimum support threshold
            if count >= self.min_support:
                # Add the itemset to the frequent itemsets dictionary
                self.frequent_itemsets[1][item] = count
        
        # Generate frequent itemsets of increasing length
        k = 2
        current_itemsets = set(self.frequent_itemsets[1].keys())

        # Keep generating frequent itemsets until done
        while current_itemsets:
            # Generate candidate k-itemsets from (k-1)-itemsets
            candidates = self.generate_candidates(current_itemsets, k)

            # Initialize candidate counts for all generated candidates
            candidate_counts = {c: 0 for c in candidates}
            
            # Count support for candidates
            for transaction in transactions:
                for candidate in candidates:
                    if candidate.issubset(transaction):
                        candidate_counts[candidate] += 1

            # Filter by minimum support count and store frequent k-itemsets
            self.frequent_itemsets[k] = {}  # Initialize an empty dictionary for k-item frequent itemsets

            # Iterate through all candidate itemsets and their counts
            for itemset, count in candidate_counts.items():
            # Check if the item's support count meets or exceeds the minimum support threshold
                if count >= self.min_support:
                    # Add the itemset to the frequent itemsets dictionary
                    self.frequent_itemsets[k][itemset] = count

            
            # If no frequent itemsets of size k, delete the entry of size 'k' and stop the process
            if not self.frequent_itemsets[k]:
                del self.frequent_itemsets[k]
                break
            
            # Move to the next level
            current_itemsets = set(self.frequent_itemsets[k].keys())
            k += 1

        # end time
        end_time = time.time()

        self.frequent_itemsets_time = end_time - start_time
    
    def generate_association_rules(self):
        """Generate association rules that meet the minimum confidence."""
    
        # Start time
        start_time = time.time()
    
        # Iterate through all frequent itemsets
        for k, itemsets in self.frequent_itemsets.items():
            # Skip frequent itemsets of length 1
            if k < 2:
                continue

            # Iterate over each frequent itemset and its support count
            for itemset, support_count in itemsets.items():
                # Generate all non-empty proper subsets of itemset
                for lhs in chain.from_iterable(combinations(itemset, r) for r in range(1, len(itemset))):
                    # LHS
                    lhs = frozenset(lhs)
                    # RHS
                    rhs = itemset - lhs
                
                    # Ensuring the RHS is not empty
                    if rhs:
                        # Get support count of LHS
                        lhs_support = self.frequent_itemsets[len(lhs)].get(lhs, 0)

                        # Compute confidence: S(itemset) / S(lhs)
                        confidence = support_count / lhs_support if lhs_support else 0
                        confidence = round(confidence, 3)
                        
                        # Add rule if confidence meets the threshold 
                        if confidence >= self.min_confidence:
                            self.association_rules.append((lhs, rhs, confidence))

        # End time
        end_time = time.time()
        self.association_rules_time = end_time - start_time
    
    def print_association_rules(self):
        """Print association rules in an understandable format."""
        formatted_rules = [(set(lhs), set(rhs), confidence) for lhs, rhs, confidence in self.association_rules]
        print("Association Rules:", [f"({lhs} --> {rhs}, {conf:.1f})" for lhs, rhs, conf in formatted_rules])

    def run(self, transactions):
        """Execute the Apriori algorithm."""
        self.get_frequent_itemsets(transactions)
        self.generate_association_rules()
        return self.frequent_itemsets, self.association_rules, self.frequent_itemsets_time, self.association_rules_time
    
# OUTPUT FREQUENT ITEMSETS TXT FILE
def generate_frequent_itemsets_file(frequent_itemsets, transactions_length, output_file="items03.txt"):
    # Write the items txt file
    with open(output_file, "w") as file:
        # Loop through each itemset size (1-itemsets, 2-itemsets, etc.)
        for _, itemsets in frequent_itemsets.items():
            for itemset, support_count in itemsets.items():
                # Format the itemset as a string
                itemset_str = " ".join(itemset) if isinstance(itemset, frozenset) else itemset
                support = support_count / transactions_length
                # Write the line to the file
                file.write(f"{itemset_str}|{support_count}|{support:.3f}\n")

# OUTPUT ASSOCIATION RULES TXT FILE
def generate_association_rules_file(frequent_itemsets, transactions_length, association_rules, output_file="rules03.txt"):
    # Write the rules txt file
    with open(output_file, "w") as file:
        # Loop through each association rule
        for lhs, rhs, confidence in association_rules:
            # Get the support count for the LHS and RHS
            lhs_support_count = sum([support_count for itemset, support_count in frequent_itemsets.get(len(lhs), {}).items() if lhs.issubset(itemset)])
            rhs_support_count = frequent_itemsets.get(len(rhs), {}).get(rhs, 0)
            
            # Calculate the support for LHS and RHS
            lhs_support = lhs_support_count / transactions_length
            rhs_support = rhs_support_count / transactions_length
            
            # Calculate the support of the association rule (LHS ∪ RHS)
            rule_support_count = frequent_itemsets.get(len(lhs.union(rhs)), {}).get(lhs.union(rhs), 0)
            rule_support = rule_support_count / transactions_length
            
            # Calculate lift: rule support / (LHS support * RHS support)
            lift = rule_support / (lhs_support * rhs_support) if lhs_support > 0 and rhs_support > 0 else 0
            
            # Write the rule to the file
            file.write(f"{' '.join(lhs)}|{' '.join(rhs)}|{rule_support_count}|{rule_support:.3f}|{confidence:.3f}|{lift:.3f}\n")

# Output info.txt file
def generate_summary_report(minsuppc, minconf, input_file_name, number_of_transactions, transactions, 
                            frequent_itemsets, association_rules, 
                            frequent_itemset_time, confident_rules_time, output_file="info03.txt"):
    # Calculate required values
    num_items = len(set(item for transaction in transactions for item in transaction))
    max_transaction_length = max(len(transaction) for transaction in transactions)
    
    # Count the number of frequent k-itemsets
    frequent_itemset_counts = {k: len(v) for k, v in frequent_itemsets.items()}
    total_frequent_itemsets = sum(frequent_itemset_counts.values())

    # Find the highest confidence and highest lift rules
    highest_confidence = max(rule[2] for rule in association_rules) if association_rules else 0
    highest_lift = 0
    highest_lift_rules = []
    
    # Dictionary to store lift values for each rule
    rule_lift_values = []
    
    # Iterate through all association rules (LHS → RHS) with their confidence values
    for lhs, rhs, confidence in association_rules:
        # Compute support count for LHS, RHS, and both LHS or RHS (number of transactions that contains the three attributes)
        support_count_lhs = sum(frequent_itemsets[k][lhs] for k in frequent_itemsets if lhs in frequent_itemsets[k])
        support_count_rhs = sum(frequent_itemsets[k][rhs] for k in frequent_itemsets if rhs in frequent_itemsets[k])
        support_count_rule = sum(frequent_itemsets[k][lhs | rhs] for k in frequent_itemsets if (lhs | rhs) in frequent_itemsets[k])

        # Compute the support
        support_lhs = support_count_lhs / number_of_transactions # P(LHS)
        support_rhs = support_count_rhs / number_of_transactions # P(RHS)
        support_rule = support_count_rule / number_of_transactions # P(LHS, RHS)

        # Compute Lift = P(LHS, RHS) / P(LHS) * P(RHS)
        lift = support_rule / (support_lhs * support_rhs)

        # Store the rule
        rule_lift_values.append((lhs, rhs, confidence, lift))

        # Set highest lift
        if lift > highest_lift:
            highest_lift = lift

    # Get all rules with the highest confidence and highest lift
    highest_confidence_rules = [(lhs, rhs, conf) for lhs, rhs, conf in association_rules if conf == highest_confidence]
    highest_lift_rules = [(lhs, rhs, conf, lift) for lhs, rhs, conf, lift in rule_lift_values if lift == highest_lift]

    # Write the info txt file
    with open(output_file, "w") as file:
        file.write(f"minsuppc: {minsuppc}\n")
        file.write(f"minconf: {minconf}\n")
        file.write(f"input file: {input_file_name}\n")
        file.write(f"Number of items: {num_items}\n")
        file.write(f"Number of transactions: {number_of_transactions}\n")
        file.write(f"The length of the longest transaction: {max_transaction_length}\n")

        for k, count in sorted(frequent_itemset_counts.items()):
            file.write(f"Number of frequent {k}-itemsets: {count}\n")
        file.write(f"Total number of frequent itemsets: {total_frequent_itemsets}\n")

        file.write(f"Number of high-confidence rules: {len(association_rules)}\n")

        file.write(f"The rules with the highest confidence ({highest_confidence}):\n")
        for lhs, rhs, conf in highest_confidence_rules:
            file.write(f"{', '.join(lhs)} -> {', '.join(rhs)} | Confidence: {conf}\n")

        file.write(f"The rules with the highest lift ({highest_lift:.3f}):\n")
        for lhs, rhs, conf, lift in highest_lift_rules:
            file.write(f"{', '.join(lhs)} -> {', '.join(rhs)} | Lift: {lift:.3f}\n")

        file.write(f"Time in seconds to find the frequent itemsets: {frequent_itemset_time:.4f}\n")
        file.write(f"Time in seconds to find the confident rules: {confident_rules_time:.4f}\n")

def practice_test(min_support, min_confidence, file_name=''):
    # Transactions simple example
    transactions = [
        ["milk", "bread", "nuts", "apple"],
        ["milk", "bread", "nuts"],
        ["milk", "bread"],
        ["milk", "bread", "apple"],
        ["bread", "apple"],
    ]
    
    # Running Apriori Algorithm
    apriori = Apriori(min_support, min_confidence)
    frequent_itemsets, rules, frequent_itemsets_time, rules_time = apriori.run(transactions)
    
    # Printing all frequent itemsets
    print("Printing the frequent itemset, the number next to the set is the support count.")
    print(f"Time to find all frequent itemsets: {frequent_itemsets_time:.4f} seconds")
    print("Frequent Itemsets:", frequent_itemsets)
    print()

    # Printin all association rules
    print("Printing the association rules based on the frequent itemsets. The number next to the association is the confidence.")
    print(f"Time to find all association rules: {rules_time:.4f} seconds")
    print("Association Rules:", rules)
    #apriori.print_association_rules()

    # create output files
    generate_frequent_itemsets_file(frequent_itemsets, len(transactions))
    generate_association_rules_file(frequent_itemsets, len(transactions), rules)
    generate_summary_report(min_support, min_confidence, "small.txt", len(transactions), transactions, frequent_itemsets, rules, frequent_itemsets_time, rules_time)

def execute_program(min_support, min_confidence, file_name):
    transactions = []
    current_transaction = []  # Initialize an empty list for the current transaction ID
    previous_transaction_id = None  # Track the previous transaction ID
    
    with open(file_name, "r") as file:
        for line in file:
            transaction_id, item_id = map(int, line.split())  # Split the line into two numbers
            
            # If we encounter a new transaction ID, save the previous transaction
            if transaction_id != previous_transaction_id and previous_transaction_id is not None:
                transactions.append(current_transaction)  # Add the current transaction to transactions list
                current_transaction = []  # Reset the list for the new transaction ID
            
            # Add the item ID to the current transaction
            current_transaction.append(str(item_id))
            
            # Update the previous transaction ID
            previous_transaction_id = transaction_id
        
        # Add the last transaction
        if current_transaction:
            transactions.append(current_transaction)
    
    # Check if the transactions were stored in the desired format
    with open("transactions.txt", "w") as file:
        for transaction in transactions:
            file.write(f"{transaction}\n")

    # Running the Apriori Algorithm
    apriori = Apriori(min_support, min_confidence)
    frequent_itemsets, rules, frequent_itemsets_time, rules_time = apriori.run(transactions)
    
    # Print the information of frequent itemsets that were found
    print("Printing the frequent itemset, the number next to the set is the support count.")
    print(f"Time to find all frequent itemsets: {frequent_itemsets_time:.4f} seconds")
    print("Frequent Itemsets:", frequent_itemsets)
    print()

    # Print infomration of association rules that were found
    print("Printing the association rules based on the frequent itemsets. The number next to the association is the confidence.")
    print(f"Time to find all association rules: {rules_time:.4f} seconds")
    print("Association Rules:", rules)
    #apriori.print_association_rules()

    #create output files
    generate_frequent_itemsets_file(frequent_itemsets, len(transactions))
    generate_association_rules_file(frequent_itemsets, len(transactions), rules)
    generate_summary_report(min_support, min_confidence, file_name, len(transactions), transactions, 
                            frequent_itemsets, rules, frequent_itemsets_time, rules_time
    )

    # Confirmation message
    print("\nOUTPUT FILES WERE SUCCESSFULLY GENERATED")
    
# Example usage
if __name__ == "__main__":
    pass

    # Set up argument parser
    parser = argparse.ArgumentParser(description="Process minsup, minconf, and input file name.")
    
    # Add arguments
    parser.add_argument("minsup", type=int, help="Minimum support value (float)")
    parser.add_argument("minconf", type=float, help="Minimum confidence value (float)")
    parser.add_argument("input_file_name", type=str, help="The name of the input file")
    
    # Parse arguments
    args = parser.parse_args()

    # This function executes the test example provided by the skeleton
    #practice_test(args.minsup, args.minconf)

    # This function executes the actual requirements with the three input variables
    # minimum support count, minimum confidence, and input file name (transactions)
    execute_program(args.minsup, args.minconf, args.input_file_name)