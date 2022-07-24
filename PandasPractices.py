import pandas as pd
import numpy as np
import seaborn as sns
from statistics import mode


# Titanic dataset is loaded
df = sns.load_dataset("titanic")
pd.set_option('display.max_columns',None)
df.head()

# Female and male passenger numbers in dataset
df["sex"].value_counts()

# The number of unique values for each column.
df.nunique()
"""
survived         2
pclass           3
sex              2
age             88
sibsp            7
"""

# The number of unique values for "pclass" variable.
df["pclass"].nunique()

# The number of unique values for "pclass" and "parch" variables.
df[["pclass","parch"]].nunique()

# Checking the type of "embarked" variable and change the type as "category"
df["embarked"].dtype
df["embarked"]=df["embarked"].astype("category")

# All information of those with embarked value C
df[df["embarked"] == 'C']

# All information of those with embarked non value S
df[df["embarked"] != 'S']

# All information for passengers younger than 30 years old and female.
df.loc[(df["age"]<30) & (df["sex"] == "female")]

# Information for passengers whose are over 500 or over 70 years old.
df.loc[(df["fare"]>500) | (df["age"]>70)]

# The sum of the null values in each variable.
df.isnull().sum()

# Drop the "who" variable from the dataset.
df.drop("who", axis=1, inplace=True)

# Filled the empty values in the "deck" variable
# with the most repeated value (mode) of the deck variable.
df["deck"].fillna(value=mode(df["deck"]),inplace=True)
""""
type(df["deck"].mode())
df["deck"].mode()[0]
df["deck"].fillna(df["deck"].mode()[0], inplace=True)
df["deck"].isnull().sum()
"""

# Filling the blank values in the age variable with the median of the age variable.
df["age"].fillna(value=np.median(df["age"]), inplace=True)

# The sum, count, mean values of the pclass and gender variables of the survived variable.
df.groupby(["pclass", "sex"]).agg({"survived": ["sum", "count", "mean"]})

# A function that will return 1 for those under 30,
# 0 for those equal to or above 30. Using the function you wrote, create a variable
# named age_flag in the titanic data set.
df["age_flag"] = df["age"].apply(lambda x: 1 if x < 30 else 0)

# Defined the Tips dataset from the Seaborn library
df2 = sns.load_dataset("tips")
pd.set_option('display.max_columns', None)
df2.head()

# Found the sum, min, max and mean values of the total_bill value according
# to the categories (Dinner, Lunch) of the time variable.
df2.groupby("time").agg({"total_bill": ["sum", "min", "max", "mean"]})

# Found the sum, min, max and mean values of total_bill values
# according to day and time.
df2.groupby(["day", "time"]).agg({"total_bill": ["sum", "min", "max","mean"]})

# Found the sum, min, max and mean values of the total_bill and type values
# of the lunch time and female customers according to the day.
df_new = df2.loc[(df2["time"] == "Lunch") & (df2["sex"] == "Female")]
df_new.groupby("day").agg({"total_bill": ["sum", "min", "max", "mean"],
                           "tip": ["sum", "min", "max", "mean"]})

# Found the average of orders
# with size less than 3 and total_bill greater than 10?
df2.loc[(df2["size"] < 3) & (df2["total_bill"] > 10),"total_bill"].mean()


# Create a new variable called total_bill_tip_sum.
# Let him give the sum of the total bill and tip paid by each customer.
df2["total_bill_tip_sum"] = df2["total_bill"] + df2["tip"]

# Found the mean of the total_bill variable separately for men and women.
# Create a new total_bill_flag variable, giving 0 for those below the averages
# you found, 1 for those above and 1 for those that are equal.
# The averages of Female for women and Male for men will be taken into account.

f_avg = df2[df2["sex"]=="Female"]["total_bill"].mean() # 18.056
m_avg = df2[df2["sex"]=="Male"]["total_bill"].mean() # 20.744

def func(sex,total_bill):

    if sex == "Female":
        if total_bill < f_avg:
            return 0
        else:
            return 1
    else:
        if total_bill < m_avg:
            return 0
        else:
            return 1

df2["total_bill_flag"] = df2[["sex","total_bill"]].apply(lambda x: func(x["sex"],x["total_bill"]),axis=1)

# By total_bill_flag variable,
# observed the number of people below and above the mean by gender.
df2.groupby(["sex","total_bill_flag"]).agg({"total_bill_flag":"count"})

# Sorted the data from largest to smallest according to the total_bill_tip_sum
# variable and assign the first 30 people to a new dataframe.
df3 = df2.sort_values(by="total_bill_tip_sum", ascending=False)
df3.head()

