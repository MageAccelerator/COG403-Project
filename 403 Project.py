#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install cjklib3')


# In[2]:


#import sys
#!{sys.executable} -m pip install cjklib
import numpy as np
import pandas as pd
import cjklib
from cjklib import characterlookup


# In[125]:


df = pd.read_csv('Chinese Lexicon Project Sze et al.csv')


# In[4]:


# df


# In[133]:


# Import the xinhua Chinese dictionary
xinhua = pd.read_csv("xinhua.csv")


# In[134]:


char = list(df.Character)
rt = list(df.RT)
xinhua_char = list(xinhua.character)
radical = list(xinhua.radical)


# In[135]:


######################## Study 1 ########################
# Correlation between stroke counts and rt
# check stroke counts
charlookup = characterlookup.CharacterLookup('T')
stroke_count = []
for i in char:
    stroke_count.append(charlookup.getStrokeCount(i))

# Uncomment to check the stroke count
#stroke_count


# In[136]:


######################## Study 2 ########################
# Correlation between radical_removed stroke counts and rt
# get the radical for each character
new_char = []
radical_list = []
for i in range(len(char)):
    for j in range (len(xinhua_char)):
        if char[i] == xinhua_char[j]:
            radical_list.append(radical[j])
            new_char.append(char[i])
            
# print(radical_list)
# print(new_char)


# In[137]:


# Check missing characters
for i in char:
    if i not in new_char:
        print(i)


# In[138]:


# get the stroke count for each charcter in the new list
new_stroke_count = []
for i in new_char:
    new_stroke_count.append(charlookup.getStrokeCount(i))

# get the radical count for each charcter
radical_count = []
for j in radical_list:
    radical_count.append(charlookup.getStrokeCount(j))

#print(radical_count)


# In[139]:


# check radical removed stroke counts
radical_removed = []
for i in range(len(new_stroke_count)):
    x = new_stroke_count[i] - radical_count[i]
    radical_removed.append(x)

#print(radical_removed)


# In[140]:


# get the reaction time list for radical removed characters
new_rt = []
for i in range(len(char)):
    for j in range(len(new_char)):
        if char[i] == new_char[j]:
            new_rt.append(rt[i])
            
# new_rt


# In[141]:


# Check nulls for radical removed characters
for i in range(len(radical_removed)):
    if radical_removed[i] == 0:
        print(new_char[i])


# In[142]:


######################## Study 3 ########################
# Compare rt for radical_removed characters within each radical.

# Get all the radicals used in the study
radicals = []
for k in radical_list: 
    if k not in radicals:
        radicals.append(k)

# Get the dictionary containing all characters for each radical.
radical_dict = {}
for k in radicals:
    l = []
    for i in range(len(new_char)):
        if radical_list[i] == k:
            l.append(new_char[i])
    radical_dict[k] = l


# In[143]:


print(radical_dict)


# In[144]:


len(radicals)


# In[145]:


######################## Data Analysis ########################

import matplotlib.pyplot as plt
from scipy import stats


# In[146]:


# Study 1 linear regression results
slope1, intercept1 =  np.polyﬁt(stroke_count, rt, 1)
result_1 = stats.linregress(stroke_count, rt)
print(result_1)


# In[147]:


# Study 1 result graph
plt.scatter(stroke_count, rt)
plt.plot(stroke_count, np.multiply(slope1, stroke_count) + intercept1, 'r-')
plt.xlabel("Stroke Counts")
plt.ylabel("Reaction Time")


# In[148]:


# Study 2 linear regression results
slope2, intercept2 = np.polyﬁt(radical_removed, new_rt, 1)
result_2 = stats.linregress(radical_removed, new_rt)
print(result_2)


# In[149]:


# Study 2 result graph
plt.scatter(radical_removed, new_rt)
plt.plot(radical_removed, np.multiply(slope2, radical_removed) + intercept2, 'r-')
plt.xlabel("Stroke Counts After Removing Radicals")
plt.ylabel("Reaction Time")


# In[155]:


# Study 3 analysis
r_value_list = []
p_value_list = []
for j in radicals:
    r = []
    for i in range(len(new_rt)):
        if radical_list[i] == j:
            r.append(new_rt[i])
    
    s = []
    for i in range(len(new_char)):
        if radical_list[i] == j:
            s.append(radical_removed[i])
    
    result_3 = stats.linregress(s, r)
    slope, intercept, r_value, p_value, std_err = result_3
    r_value_list.append(r_value)
    if r_value != 0:
        p_value_list.append(p_value)
    print("Radical:", j, "\n" , result_3)
    


# In[151]:


ave_r = sum(r_value_list)/len(r_value_list)
print("Average Pearson's r correlation coefficient is: ", ave_r)

ave_p = sum(p_value_list)/len(p_value_list)
print("Average p value is: ", ave_p)


# In[156]:


fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
ax.bar(radicals, r_value_list)
plt.ylabel("Pearson's r correlation coefficient")
plt.xlabel("Radicals")


# In[153]:


# correlation analysis
from scipy.stats import pearsonr
stroke_cor = pearsonr(stroke_count, rt)
radical_cor = pearsonr(radical_removed, new_rt)

# study 1 correlation
print("Correlation for study 1 is: ", stroke_cor)

# study 2 correlation
print("Correlation for study 2 is: ", radical_cor)


# In[154]:


# Check characters with more than 20 strokes
for i in char:
    if charlookup.getStrokeCount(i) >20:
        print(i)

