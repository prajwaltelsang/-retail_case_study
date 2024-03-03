#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Importing the packages
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns


# In[2]:


cust=pd.read_csv("Customer.csv")
trans=pd.read_csv("Transactions.csv")
prod=pd.read_csv("prod_cat_info.csv")


# In[3]:


cust.head()


# In[4]:


trans.head()


# In[5]:


prod.head()


# In[6]:


prod.rename(columns={"prod_sub_cat_code":"prod_subcat_code"},inplace=True)


# In[7]:


print(cust.shape)
print(trans.shape)
print(prod.shape)


# 1. Merge the datasets customers, Product Hierarchy and Transactions as customer_final

# Merge trans and product

# In[8]:


prod_trans=pd.merge(left=trans, right=prod,on=["prod_cat_code","prod_subcat_code"],how="left")


# In[9]:


prod_trans.head()


# In[10]:


prod_trans.shape


# In[11]:


prod_trans.isnull().sum()


# Merge customer and prod_trans tables

# In[12]:


cust.head()


# In[13]:


customer_final=pd.merge(left=prod_trans,right=cust,
                        left_on="cust_id",right_on="customer_Id",how="left")


# In[14]:


customer_final.head()


# In[15]:


customer_final.shape


# In[16]:


customer_final.dtypes


# In[17]:


customer_final.isnull().sum()


# In[18]:


customer_final['DOB'] = pd.to_datetime(customer_final['DOB'], format='%d-%m-%Y')


# In[19]:


customer_final['tran_date'] = pd.to_datetime(customer_final['tran_date'], format='mixed', dayfirst=True)


# In[20]:


customer_final['DOB'].head(10)


# In[21]:


customer_final['tran_date'].head(10)


# In[22]:


customer_final.duplicated().sum()


# In[23]:


# dropping duplicate rows
customer_final.drop_duplicates(inplace=True)


# In[24]:


customer_final.duplicated().sum()


# 2. Prepare a summary report for merged data set.

# a. column names and their corresponding data types

# In[25]:


# column names
customer_final.columns


# In[26]:


# data types
customer_final.dtypes


# In[27]:


#Top observations
customer_final.head(10)


# In[28]:


#Bottom observations
customer_final.tail(10)


# c."Five number summary" for continuous variables

# In[29]:


customer_final.describe()


# d. Frequency table for all categorical variables

# In[30]:


customer_final.loc[:,customer_final.dtypes=="object"].describe()


# 3. Generate histogram for all continuous variables and frequency bars for categorical variables

# Histogram for all continuous variables

# In[31]:


conti_vari=customer_final.loc[:,['prod_subcat_code','prod_cat_code','Qty', 'Rate', 'Tax', 'total_amt']]


# In[32]:


conti_vari.columns


# In[33]:


for var in conti_vari.columns:
    conti_vari[var].plot(kind='hist')
    plt.title(var)
    plt.show()


# Bar chart for categorical variables

# In[34]:


cate_vari=customer_final.loc[:,customer_final.dtypes=='object']


# In[35]:


cate_vari.head(2)


# In[36]:


plt.figure(figsize=(8, 8))
sns.countplot(data=cate_vari, x='Store_type', hue='Store_type')
plt.xlabel('Store Type')
plt.show()


# In[37]:


cate_vari.dtypes


# In[38]:


plt.figure(figsize=(8, 8))
sns.countplot(data=cate_vari, x='Gender', hue='Gender')
plt.xlabel('Gender')
plt.show()


# In[39]:


plt.figure(figsize=(8, 8))
sns.countplot(data=cate_vari, x='prod_cat', hue='prod_cat')
plt.xlabel('Product Category')
plt.show()


# In[40]:


plt.figure(figsize=(8,8))
cate_vari.groupby('prod_subcat')['prod_subcat'].count().plot(kind='barh')
plt.xlabel('Count')
plt.ylabel('Product Subcategory')
plt.show()


# 4. Ccalculate the following using merged dataset

# a. Time period of transaction data

# In[41]:


customer_final.sort_values(by='tran_date')


# In[42]:


min_date = customer_final["tran_date"].min()


# In[43]:


min_date


# In[44]:


max_date = customer_final["tran_date"].max()


# In[45]:


max_date


# In[46]:


print("Time period of the available transaction data is from "+ pd.Timestamp.strftime(min_date,format="%d-%m-%Y") + " to " + pd.Timestamp.strftime(max_date,format="%d-%m-%Y"))


# b. Count of transactions where the total amount of transaction was negative

# In[47]:


customer_final.head(2)


# In[48]:


# Count of transaction id where total amount is negative
negative_transaction = customer_final.loc[customer_final["total_amt"] < 0,"transaction_id"].count()


# In[49]:


print("Count of transactions where the total amount of transaction was negative is",negative_transaction)


# 5.Analyze which product categories are more popular among female vs male customers

# In[50]:


#groupby the data on the basis of gender amd product_cat
product_gender= customer_final.groupby(["Gender","prod_cat"])[["Qty"]].sum().reset_index()


# In[51]:


product_gender


# In[52]:


#Converting to pivot table for better view
product_gender.pivot(index="Gender",columns="prod_cat",values="Qty")


# Products that are popular among male are
# Books
# clothing
# electronics
# home and kitchen

# Products that are popular among female are 
# bags 
# footwear

# 6. Which City code has the maximum customers and what was the percentage of customers from 
# that city?

# In[53]:


customer_final.head(2)


# In[54]:


customer_group=customer_final.groupby('city_code')['customer_Id'].count().sort_values(ascending=False)


# In[55]:


customer_group


# In[56]:


percentage= round((customer_group[4.0] / customer_group.sum())*100,2)


# In[57]:


percentage


# In[58]:


print("City code 4.0 has the maximum customers and the percentage of customers from that city is ",percentage)


# 7. Which store type sells the maximum products by value and by quantity?
# 

# In[59]:


customer_final.head(2)


# In[60]:


customer_final.groupby("Store_type")[["Qty", "Rate"]].sum().sort_values(by="Qty", ascending=False)


# In[61]:


print('e-Shop store sell the maximum products by value and by quantity')


# 8. What was the total amount earned from the "Electronics" and "Clothing" categories from 
# Flagship Stores?
# 

# In[62]:


store_group = round(customer_final.pivot_table(index = "prod_cat",columns="Store_type", values="total_amt", aggfunc='sum'),2)


# In[63]:


store_group


# In[64]:


store_group.loc[["Clothing","Electronics"],"Flagship store"]


# In[65]:


# if we have to find total amount of both 'Clothing' and 'Electronics' from ' Flagship Store'
store_group.loc[["Clothing","Electronics"],"Flagship store"].sum()


# 9. What was the total amount earned from "Male" customers under the "Electronics" category?

# In[66]:


gender_group = round(customer_final.pivot_table(index = "prod_cat",columns="Gender", values="total_amt", aggfunc='sum'),2)


# In[67]:


gender_group


# In[68]:


male_earning = gender_group.loc["Electronics","M"]


# In[69]:


print("The total amount earned from Male customers under the Electronics category is",male_earning)


# 10. How many customers have more than 10 unique transactions, after removing all transactions 
# which have any negative amounts?
# 

# In[70]:


non_negative_transactions = customer_final[customer_final['total_amt'] >= 0]
customer_unique_transactions = non_negative_transactions.groupby('customer_Id')['transaction_id'].nunique()
customers_with_more_than_10_transactions = customer_unique_transactions[customer_unique_transactions > 10]
num_customers_more_than_10_transactions = len(customers_with_more_than_10_transactions)

print("Number of customers with more than 10 unique transactions, after removing negative amounts:")
print(num_customers_more_than_10_transactions)


# 11. For all customers aged between 25 - 35, find out:

# a. What was the total amount spent for “Electronics” and “Books” product categories?
# 

# In[71]:


customers_25_to_35 = customer_final[(customer_final['DOB'] >= '1989-01-01') & (customer_final['DOB'] <= '1999-12-31')]
electronics_books_data = customers_25_to_35[customers_25_to_35['prod_cat'].isin(['Electronics', 'Books'])]
total_amount_spent_electronics_books = electronics_books_data['total_amt'].sum()

print("Total amount spent for 'Electronics' and 'Books' product categories by customers aged between 25 - 35:")
print(f"Amount: {total_amount_spent_electronics_books:.2f}")


#  b. What was the total amount spent by these customers between 1st Jan, 2014 to 1st Mar, 2014?
# 

# In[72]:


transactions_between_dates = customer_final[(customer_final['tran_date'] >= '2014-01-01') & (customer_final['tran_date'] <= '2014-03-01')]
customers_between_dates = transactions_between_dates[(transactions_between_dates['DOB'] >= '1989-01-01') & (transactions_between_dates['DOB'] <= '1999-12-31')]
total_amount_spent_between_dates = customers_between_dates['total_amt'].sum()

print("\nTotal amount spent by customers aged between 25 - 35 between 1st Jan, 2014, and 1st Mar, 2014:")
print(f"Amount: {total_amount_spent_between_dates:.2f}")


# In[ ]:




