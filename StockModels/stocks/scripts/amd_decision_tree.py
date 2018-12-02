'''
This code looks for trends in stock market information.
It prints a decision tree visualizing 'breaks' in data, showing where
certain variables are the most important in predicting a target variable.
'''

# Link to video on CART and decision trees: https://www.youtube.com/watch?v=tNa99PG8hR8

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn import tree
import graphviz


#%% 

# What is the main controlling factor on daily change of AMD?

AMD = pd.read_csv(r"C:\Users\Administrator\Google Drive\Programming\Python\ML_stocks\AMD20172018.csv")
# Converting dates to pandas datetime
AMD['Date'] = pd.to_datetime(AMD['Date'])
# Adding in day of the week - might give some additional information
AMD['day'] = [x.weekday() for x in AMD['Date']]
# Which direction did the price move for any given day?
def which_dir(row):
    if row['Close'] < row['Open']:
        return 0 # price goes down
    else:
        return 1 # price goes up

AMD['change_dir'] = AMD[['Close','Open']].apply(which_dir, axis=1)
target_labels = ['down','up'] # index-correct labels for target data, needed for display in the tree
# Remove 'adj close'
AMD = AMD.drop('Adj Close', axis=1)

train_data = AMD.drop(['Date','change_dir'], axis=1)

#Dataframe has 252 samples; this is 252 days
clf = tree.DecisionTreeClassifier(max_depth=5, min_samples_split=20)
clf.fit(train_data, AMD['change_dir'])

# Now visualizing in a decision tree
dot_data = tree.export_graphviz(clf, out_file=None,  
                         filled=True, rounded=True,
                         feature_names=list(train_data.columns),
                         class_names=target_labels,
                         special_characters=True)
graph = graphviz.Source(dot_data)
graph

#graph = pydotplus.graph_from_dot_data(dot_data)
#graph.write_pdf('C://Users//roush//Documents//Python//graph_outputs//AMD_graph.pdf')



#%% Using iris data as an example
iris = load_iris()
test_idx = [0,50,100]

#testing data
train_target = np.delete(iris.target, test_idx)
train_data = np.delete(iris.data, test_idx, axis=0)

# testing data
test_target = iris.target[test_idx]
test_data = iris.data[test_idx]

# training classifier
clf = tree.DecisionTreeClassifier()
clf.fit(train_data, train_target)

print(clf.predict(test_data))
# the classifier works on the test data!

# Now visualizing in a decision tree
dot_data = tree.export_graphviz(clf, out_file=None, 
                         feature_names=iris.feature_names,  
                         class_names=iris.target_names,  
                         filled=True, rounded=True,  
                         special_characters=True)
graph = graphviz.Source(dot_data)
graph
