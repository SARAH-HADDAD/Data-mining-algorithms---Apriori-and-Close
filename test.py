from itertools import combinations

def generate_combinations(candidates, k):
    return list(combinations(candidates, k))
candidates = ['Alice', 'Bob', 'Charlie', 'Dave', 'Eve']
k = 4

combinations = generate_combinations(candidates, k)
new_candidates=[]
for c in combinations:
    new_candidates.append(list(c))
print(new_candidates)


