# Fp algorithm
from collections import defaultdict

class FPNode:
    def __init__(self, item, count, parent):
        self.item = item
        self.count = count
        self.parent = parent
        self.children = {}
        self.link = None

    def increment(self, count):
        self.count += count

class FPTree:
    def __init__(self, transactions, min_support):
        self.root = FPNode(None, 1, None)
        self.header_table = defaultdict(list)
        self.min_support = min_support
        self.freq_items = self.find_frequent_items(transactions)
        self.build_tree(transactions)

    def find_frequent_items(self, transactions):
        item_counts = defaultdict(int)
        for transaction in transactions:
            for item in transaction:
                item_counts[item] += 1
        return {item: count for item, count in item_counts.items() if count >= self.min_support}

    def build_tree(self, transactions):
        for transaction in transactions:
            ordered_items = [item for item in sorted(transaction, key=lambda x: self.freq_items.get(x, 0), reverse=True)
                             if item in self.freq_items]
            self.insert_tree(ordered_items, self.root)

    def insert_tree(self, items, node):
        if not items:
            return
        first = items[0]
        if first in node.children:
            node.children[first].increment(1)
        else:
            new_node = FPNode(first, 1, node)
            node.children[first] = new_node
            self.update_header(first, new_node)
        self.insert_tree(items[1:], node.children[first])

    def update_header(self, item, node):
        if self.header_table[item]:
            current = self.header_table[item][-1]
            while current.link:
                current = current.link
            current.link = node
        self.header_table[item].append(node)

    def mine_patterns(self):
        patterns = {}
        items = sorted(self.freq_items.items(), key=lambda x: x[1])
        for item, support in items:
            suffixes = []
            node = self.header_table[item][0]
            while node:
                path = []
                parent = node.parent
                while parent and parent.item:
                    path.append(parent.item)
                    parent = parent.parent
                if path:
                    suffixes.append((list(reversed(path)), node.count))
                node = node.link
            cond_tree = FPTree([path for path, count in suffixes for _ in range(count)], self.min_support)
            suffix_patterns = cond_tree.mine_patterns()
            for pattern, count in suffix_patterns.items():
                patterns[tuple(sorted((item,) + pattern))] = count
            patterns[(item,)] = self.freq_items[item]
        return patterns
