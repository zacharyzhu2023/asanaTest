#!/usr/bin/env python
# coding: utf-8

# In[86]:


# Includes the necessary imports
import pandas as pd
import seaborn as sns
import numpy as np
import datetime as dt
from matplotlib import pyplot as plt


# In[45]:


# Read in Data
recurringUsers = '/Users/zacharyzhu/Desktop/asana/recurringUsers.csv'
dfRecur = pd.read_csv(recurringUsers, engine = 'python')
dfRecur['Datetime'] = pd.to_datetime(dfRecur['time_stamp'])
dfRecur['Time Delta'] = pd.to_timedelta(dfRecur['Datetime'], 'D')
dfRecur


# In[56]:


timedeltas = dfRecur['Time Delta'].tolist()

validUserIDs = set()
compare = dt.timedelta(days = 7)
for i in range(len(timedeltas) - 2):
    if userIDs[i] == userIDs[i+2] and timedeltas[i+2] - timedeltas[i] <= compare:
        validUserIDs.add(userIDs[i])
#print(validUsersIDs)


# In[57]:


# Generating a sorted list of IDs
sortedIDs = sorted(validUserIDs)
sortedIDs


# In[58]:


# Load user information
userInfo = '/Users/zacharyzhu/Desktop/asana/userInfo.csv'
dfInfo = pd.read_csv(userInfo, engine = 'python')
dfInfo


# In[62]:


# Subset of users that are an "adopted user"
adoptedUsers = dfInfo[dfInfo['object_id'].isin(validUserIDs)]
adoptedUsers


# In[66]:


unadoptedUsers = dfInfo[~dfInfo['object_id'].isin(validUserIDs)]
unadoptedUsers


# In[67]:


dfInfo['Adopted'] = dfInfo['object_id'].isin(validUserIDs)
dfInfo


# In[93]:


creationSourceList = dfInfo['creation_source'].tolist()
adoptedList = dfInfo['Adopted'].tolist()

numAdopters = adoptedList.count(True)
numUnadopted = adoptedList.count(False)

# Sorting by creation source
adoptedSources = {'GUEST_INVITE': 0, 'ORG_INVITE': 0, 'PERSONAL_PROJECTS': 0, 'SIGNUP': 0, 'SIGNUP_GOOGLE_AUTH': 0}
unadoptedSources = {'GUEST_INVITE': 0, 'ORG_INVITE': 0, 'PERSONAL_PROJECTS': 0, 'SIGNUP': 0, 'SIGNUP_GOOGLE_AUTH': 0}
for i in range(len(creationSourceList)):
    if adoptedList[i]:
        adoptedSources[creationSourceList[i]] += 1
    else:
        unadoptedSources[creationSourceList[i]] += 1

adoptedSourcePercents = {'GUEST_INVITE': adoptedSources['GUEST_INVITE']/numAdopters, 
                  'ORG_INVITE': adoptedSources['ORG_INVITE']/numAdopters, 
                  'PERSONAL_PROJECTS': adoptedSources['PERSONAL_PROJECTS']/numAdopters, 
                  'SIGNUP': adoptedSources['SIGNUP']/numAdopters, 
                  'SIGNUP_GOOGLE_AUTH': adoptedSources['SIGNUP_GOOGLE_AUTH']/numAdopters}
unadoptedSourcePercents = {'GUEST_INVITE': unadoptedSources['GUEST_INVITE']/numUnadopted, 
                  'ORG_INVITE': unadoptedSources['ORG_INVITE']/numUnadopted, 
                  'PERSONAL_PROJECTS': unadoptedSources['PERSONAL_PROJECTS']/numUnadopted, 
                  'SIGNUP': unadoptedSources['SIGNUP']/numUnadopted, 
                  'SIGNUP_GOOGLE_AUTH': unadoptedSources['SIGNUP_GOOGLE_AUTH']/numUnadopted}

print("Adopted User Source Totals: " + str(adoptedSources))
print("Unadopted User Source Totals: " + str(unadoptedSources))
print("Adopted User Source Relative: " + str(adoptedSourcePercents))
print("Unadopted User Source Relative: " + str(unadoptedSourcePercents))




sourceTotalPlot = pd.DataFrame({'Adopted Source Totals': list(adoptedSources.values()),
                            'Unadopted Source Totals': list(unadoptedSources.values())
                               },
                            index = ['Guest Invite', 'Org Invite', 'Personal Projects', 'Signup', 'Google Auth Signup']
                           )
sourceTotalPlot.plot(kind = 'bar')
plt.title('Source Totals')
plt.xlabel("Source of Signup")
plt.ylabel("Number of Users")


# In[110]:


# Graphical Analysis of Souce Fractions
sourceTotalPlot = pd.DataFrame({'Adopted Source Fraction': list(adoptedSourcePercents.values()),
                            'Unadopted Source Fraction': list(unadoptedSourcePercents.values())
                               },
                            index = ['Guest Invite', 'Org Invite', 'Personal Projects', 'Signup', 'Google Auth Signup']
                           )
sourceTotalPlot.plot(kind = 'bar')
plt.title('Source Fractions')
plt.xlabel("Source of Signup")
plt.ylabel("Number of Users")


# In[115]:


# Analysis by mailing list
adoptedMailing = {}
unadoptedMailing = {}
adoptedMailing['Yes'] = adoptedUsers['opted_in_to_mailing_list'].tolist().count(1)
adoptedMailing['No'] = adoptedUsers['opted_in_to_mailing_list'].tolist().count(0)
unadoptedMailing['Yes'] = unadoptedUsers['opted_in_to_mailing_list'].tolist().count(1)
unadoptedMailing['No'] = unadoptedUsers['opted_in_to_mailing_list'].tolist().count(0)
print('Adopted Mailing Opt-ins-YES v NO: ', adoptedMailing['Yes'], ",", adoptedMailing['No'])
print('Unadopted Mailing Opt-ins-YES v NO: ', unadoptedMailing['Yes'], ",", unadoptedMailing['No'])

adoptMailingFraction = [adoptedMailing['Yes']/numAdopters, adoptedMailing['No']/numAdopters]
unadoptMailingFraction = [unadoptedMailing['Yes']/numUnadopted, unadoptedMailing['No']/numUnadopted]
fractionMailingPlot = pd.DataFrame({'Adopted Mailing Opt-In Fraction': adoptMailingFraction,
                            'Unadopted Mailing Opt-In Fraction': unadoptMailingFraction
                               }, index = ['Opt-In', 'Opt-Out'])
fractionMailingPlot.plot(kind = 'bar')
plt.title('Fraction of Mailing Lists')
plt.xlabel("Opt In to Mailing List?")
plt.ylabel("Number of Users")


# In[114]:


# Analysis by marketing drip
adoptedDrip = {}
unadoptedDrip = {}
adoptedDrip['Yes'] = adoptedUsers['enabled_for_marketing_drip'].tolist().count(1)
adoptedDrip['No'] = adoptedUsers['enabled_for_marketing_drip'].tolist().count(0)
unadoptedDrip['Yes'] = unadoptedUsers['enabled_for_marketing_drip'].tolist().count(1)
unadoptedDrip['No'] = unadoptedUsers['enabled_for_marketing_drip'].tolist().count(0)
print('Adopted Drip-YES v NO: ', adoptedDrip['Yes'], ",", adoptedDrip['No'])
print('Unadopted Drip-YES v NO: ', unadoptedDrip['Yes'], ",", unadoptedDrip['No'])

adoptDripFraction = [adoptedDrip['Yes']/numAdopters, adoptedDrip['No']/numAdopters]
unadoptDripFraction = [unadoptedDrip['Yes']/numUnadopted, unadoptedDrip['No']/numUnadopted]
dripFractionPlot = pd.DataFrame({'Adopted Drip Fraction': adoptDripFraction,
                            'Unadopted Drip Fraction': unadoptDripFraction
                               }, index = ['Opt-In', 'Opt-Out'])
dripFractionPlot.plot(kind = 'bar')
plt.title('Fraction of marketing drip')
plt.xlabel("Enabled for marketing drip?")
plt.ylabel("Number of Users")


# In[109]:


# Analysis by Email Domain
emailDomain = dfInfo['email_domain'].tolist()
len(set(emailDomain))


# In[ ]:




