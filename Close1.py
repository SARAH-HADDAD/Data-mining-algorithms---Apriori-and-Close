import numpy as np

def isSubstring(x,y):
    return all([char in y for char in x])
    
def isSubstring_ferm(x,fermeture):
    for val in fermeture.values():
        if isSubstring(x,val):
            return True
    return False

def new_candidates(candidates):
    temp=[]
    taille= len(candidates[0])-1
    for c1 in candidates :
        for c2 in candidates :
            if c1!=c2 :
                if c1[:taille] == c2[:taille] :
                    temp.append("".join(sorted(set(c1+c2))))
    temp = sorted(list(set(temp)))
    return temp

def sup(item,itemset):
    temp=np.zeros((itemset[list(itemset.keys())[0]].size,), dtype=int)
    for char in item :
        temp += itemset[char]
    sup = np.count_nonzero(temp == (len(item)))/itemset[list(itemset.keys())[0]].size
    return sup

def ferm(item,itemset,candidates):
    itemset2= itemset
    fermeture = ""
    for c in candidates :
        if len(c)>= 1 : 
                for i in range(1,len(c)) :
                    temp= np.bitwise_and(itemset2[c[i-1]],itemset2[c[i]]) 
                    itemset2[c]= temp
        if (np.array_equal(np.bitwise_or(itemset2[c],itemset2[item]),itemset2[c])) : 
            fermeture+=c
            pass
    return ''.join(sorted(list(set(fermeture))))

def close(itemset,minsup,candidats) :
    candidates = candidats
    fermetures = {}
    AssociationRules = {}
    it=1
    while candidates != [] :
        fermetures = {}
        it+=1
        candidates2=[]

        i = 0
        n = len(candidates)
        while i < n :
            c = candidates[i]

            if sup(c,itemset) < minsup :
                candidates2.append(c)
                del(candidates[candidates.index(c)])
                n-=1
            else :
                i+=1

        for c in candidates :
            fermetures[c]=ferm(c,itemset,candidates)
            if (sup(c,itemset) >= minsup) and (len(c)!=len(fermetures[c])) :
                fermetures_c = fermetures[c]
                for char in c:
                    fermetures_c = fermetures_c.replace(char, '')
                AssociationRules[c]= fermetures_c

        if candidates != [] :
            candidates = new_candidates(candidates)
            for c in candidates :
                if isSubstring_ferm(c,fermetures) :
                    del(candidates[candidates.index(c)])
    return AssociationRules

data= [['A', 'B', 'C', 'D', 'E'],
       ['A', 'B', 'C', 'D'],
       ['C', 'E'],
       ['A', 'B', 'D', 'E'],
       ['A' , 'C', 'D' ]]

# Créer un ensemble d'éléments unique
items = sorted(set([item for transaction in data for item in transaction]))

# Créer un dictionnaire avec les éléments comme clés et des vecteurs binaires correspondants
itemset = {}
for item in items:
    itemset[item] = np.array([1 if item in transaction else 0 for transaction in data])

candidates = list(itemset.keys())

AssociationRules= close(itemset,0.4,candidates)
for cle, valeur in AssociationRules.items():
    print(cle, "=> ", valeur)


