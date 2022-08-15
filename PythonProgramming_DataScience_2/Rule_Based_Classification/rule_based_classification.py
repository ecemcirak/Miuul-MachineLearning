""""

Lead Calculation with Rule-Based Classification

Business Problem

A game company wants to create level-based new customer definitions (personas)
by using some features of its customers, and to create segments according to
these new customer definitions and to estimate how much the new customers
can earn on average according to these segments.
For example,
It is desired to determine how much a 25-year-old male user from Turkey,
who is an IOS user, can earn on average.


The Persona.csv dataset contains the prices of the products sold by an
international game company and some demographic information of the users
who buy these products. The data set consists of records created in each sales
transaction. This means that the table is not deduplicated. In other words,
a user with certain demographic characteristics may have made more than
one purchase.

"""
import pandas as pd
import numpy as np
import seaborn as sns


df = pd.read_csv("persona.csv")
df.head()

df.info()
df.describe()

df["SOURCE"].nunique()
df["PRICE"].nunique()

df["PRICE"].value_counts()
df["COUNTRY"].value_counts()

df.groupby("COUNTRY")["PRICE"].sum()

df["SOURCE"].value_counts()

df.groupby("COUNTRY")["PRICE"].mean()
df.groupby("SOURCE")["PRICE"].mean()
df.groupby(["SOURCE", "COUNTRY"])["PRICE"].mean()

df2 = df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"])["PRICE"].mean()

agg_df = df2.sort_values(ascending=False)
agg_df = agg_df.reset_index()

bins = [0,18,23,30,40,agg_df["AGE"].max()]
agg_df["AGE_CAT"] = pd.cut(agg_df["AGE"],bins,labels=["0_18","19_23","24_30","31_40","41_"+str(agg_df["AGE"].max())])

agg_df['customers_level_based'] = agg_df[['COUNTRY', 'SOURCE', 'SEX', 'AGE_CAT']].agg(lambda x: '_'.join(x).upper(), axis=1)


# YÖNTEM 3
agg_df["customers_level_based"] = ['_'.join(i).upper() for i in agg_df.drop(["AGE", "PRICE"], axis=1).values]
"""
>>agg_df.drop(["AGE", "PRICE"], axis=1).values
array([['bra', 'android', 'male', '41_66', 'BRA_ANDROID_MALE_41_66'],
       ['usa', 'android', 'male', '31_40', 'USA_ANDROID_MALE_31_40'],
       ['fra', 'android', 'female', '24_30', 'FRA_ANDROID_FEMALE_24_30'],
       ...,
       ['can', 'android', 'female', '24_30', 'CAN_ANDROID_FEMALE_24_30'],
       ['fra', 'android', 'male', '0_18', 'FRA_ANDROID_MALE_0_18'],
       ['deu', 'android', 'male', '24_30', 'DEU_ANDROID_MALE_24_30']],
      dtype=object)
"""

# YÖNTEM 1

for row in agg_df.values:
    print(row)

[row[0].upper() + "_" + row[1].upper() + "_" + row[2].upper() + "_" + row[5].upper() for row in agg_df.values]

agg_df["customers_level_based"] = [row[0].upper() + "_" + row[1].upper() + "_" + row[2].upper() + "_" + row[5].upper() for row in agg_df.values]
agg_df.head()

agg_df = agg_df[["customers_level_based", "PRICE"]]
agg_df.head()

for i in agg_df["customers_level_based"].values:
    print(i.split("_"))

agg_df["customers_level_based"].value_counts()

agg_df = agg_df.groupby("customers_level_based").agg({"PRICE": "mean"})

agg_df = agg_df.reset_index()
agg_df.head()

agg_df["customers_level_based"].value_counts()
agg_df.head()

agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"], 4, labels=["D", "C", "B", "A"])
agg_df.head(30)
agg_df.groupby("SEGMENT").agg({"PRICE": "mean"})

new_user = "TUR_ANDROID_FEMALE_31_40"
agg_df[agg_df["customers_level_based"] == new_user]

new_user = "FRA_IOS_FEMALE_31_40"
agg_df[agg_df["customers_level_based"] == new_user]
