#importing packages
import pandas as pd
import numpy as np
#due to incompatibility treats and nature of our dataset we need to check the prefix
def same_prefix(item1, item2):
    nbr1 = len(item1)
    for i in range(0, nbr1 - 1):
        if item1[i] != item2[i]:
            return False
    return True
def closer_checking(final_list, fem_item1, fem_item2):
    #we need to check that our new closer doesn't exist of the two other closers 
    if set(final_list).issubset(set(fem_item1)) or set(final_list).issubset(set(fem_item2)):
            return False
    return True
def item_setting(df_fermetures):
    item_set = []
    for i in range(len(df_fermetures)):
        #we take the closer of every item along side it 
        item = df_fermetures.values[i, 0]
        fem_item = df_fermetures.values[i, 2]
        # we concat the fermetures in case it didn't exist before and append it as an item set
        for j in range(i + 1, len(df_fermetures)):
            if not same_prefix(item, df_fermetures.values[j, 0]):
                new_item_candidat = item+"-"+df_fermetures.values[j, 0]
                if closer_checking(new_item_candidat, fem_item, df_fermetures.values[j, 2]):
                    item_set.append(new_item_candidat)
    return item_set
#calculating the support  with two cases one for the first
# iteration and for next iterations 
def sup_calcuation(item_set, data_frame, min_supp,iteration):
    transactions = len(data_frame)
    sups = []
    res_prod = []
    if iteration==1:      
        for item in item_set:
          #count the ones  in the dataframe for every item_set
            count = data_frame[item].value_counts()[1]
            sup = count / transactions
            if sup >= min_supp:
                sups.append(sup)
                res_prod.append(item)
    else:
        for l in item_set:
            res = np.ones(shape=len(data_frame))
          # due to our structure us concatinating the items requires
          # us to  split  calculate and reconcat again  
            word=l.split("-")
          #populate the res  with ones to make the product from the dataset
            for k in word:
                res = data_frame[k].to_numpy() * res
            count = np.count_nonzero(res == 1)
            sup = count / transactions
            if sup >= min_supp:
                sups.append(sup)     
                s=word[0]
                for x in range(1,len(word)):
                  s=s+'-'+word[x]
                res_prod.append(s)
    return sups, res_prod
def fermetures(product_list, supports, df,iteration):
    df_res = pd.DataFrame(columns=['itemset', 'support', 'Ferm'])
    
    i = 0
    #Basically what we want to do here is calculate the closers and multiply of the matrix 
    for proned_item in product_list:
        ferm_list = []
        if iteration==1 :  # item set 1
            for item in df.columns:
                res = df[item].to_numpy() * df[proned_item].to_numpy()
                if np.array_equiv(df[proned_item].to_numpy(), res):
                    ferm_list.append(item)
            df_res.loc[len(df_res)] = [proned_item, supports[i], ferm_list]
            i += 1
  

        else:  # item sets for iterations after the first 
            ferm_list = []
            res_join = np.ones(shape=len(df))
            #splitting the data
            word=proned_item.split("-")
          #we check the items of the joined closer and check 
          #its equivalance  of the product of any of the columns 
          # it is the most consuming part for calculation with our 
          #30+ columns  and 600 data  cartesien product grows exponentially 
          #and thus we tried to modify the data set to test  
            for k in word:
                res_join = df[k].to_numpy() * res_join
            for item in df.columns:
                res = df[item].to_numpy() * res_join
                if np.array_equiv(res_join, res):
                    ferm_list.append(item)
          #re concatinating the data         
            s=word[0]
            for x in range(1,len(word)):
              s=s+'-'+word[x]
            df_res.loc[len(df_res)] = [s, supports[i], ferm_list]
            i += 1
    return df_res

def close(df_init, min_sup):
    item_set = df_init.columns
    df_res = pd.DataFrame(columns=['itemset', 'support', 'Ferm'])
    fin = True
    iteration = 1
    item_set_length = len(item_set)
    while fin and len(item_set) > 0:
        sups, result_product = sup_calcuation(item_set, df_init, min_sup,iteration)
        if len(result_product) == 0 or iteration ==4:
            break        
        df = fermetures(result_product, sups, df_init,iteration)
        item_set = item_setting(df)
        print('item_set {} ####################:'.format( str(iteration))  )
        print(df)
        df_res = pd.concat([df_res, df], axis=0, ignore_index=True)
        
        iteration += 1

    return df_res
# calculating the lift 
def lift( df_init,df_ferm,item_ferm,sup_all,df_ferm_val):
  res = np.ones(shape=len(df_init))
  for x in item_ferm:
      res = df_init[x].to_numpy() * res
  count  = np.count_nonzero(res == 1)
  sup_ferm = count  / len(df_init)   
  return  sup_all / (df_ferm_val * sup_ferm)
# calculating the confidence 
def confidence( df_init,df_ferm,item_item_ferm,df_ferm_val):
  res = np.ones(shape=len(df_init))
  for x in item_item_ferm:
      res = df_init[x].to_numpy() * res
  count = np.count_nonzero(res == 1)
  sup_all = count / len(df_init)
  return  (sup_all,sup_all / df_ferm_val)

#all the rules metrics 
def metrics(df_init,df_ferm,item_item_ferm,df_ferm_val,item_ferm):
  sup_all,confidence_res = confidence( df_init,df_ferm,item_item_ferm,df_ferm_val)
  lift_res =lift( df_init,df_ferm,item_ferm,sup_all,df_ferm_val)
  return (confidence_res , lift_res)

def rules(df_ferm, df_init):
    rule_list=["item","closer","confidence","lift"]
    df_rules=pd.DataFrame(columns=rule_list)
    for i in range(len(df_ferm)):
        item = df_ferm.values[i, 0]
        fermeture = df_ferm.values[i, 2]
        item_ferm = [x for x in fermeture if x not in item]
        if len(item_ferm) > 0:
            if isinstance(item, str):
                item = item.split("-")
            item_item_ferm = item + item_ferm
            df_ferm_val=df_ferm.values[i, 1]
            confidence, lift=metrics(df_init,df_ferm,item_item_ferm,df_ferm_val,item_ferm)
            data_rule=dict(zip(rule_list,[item,item_ferm,confidence,lift]))
            df_rules=df_rules.append(data_rule,ignore_index=True)
    return df_rules
#Data path toward the csv File
DATA_PATH='new_data.csv'
#reading using panda's read_csv function
data = pd.read_csv(DATA_PATH)
#viewing the first 5 elements of the data set
data.info()
Min_sup=0.20
data_close=data
# data_close=data_nowork

df = close(data_close, Min_sup)
# df.head()
print(df)
df_rules=rules(df, data_close)
print(df_rules)