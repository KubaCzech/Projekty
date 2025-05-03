# Perform classification using knn classifier.
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import time
import pandas as pd
from sklearn.preprocessing import StandardScaler
import re

# Load the dataset
data = pd.read_csv('train.csv')

# Drop unnecessary columns including 'Lname' if present
X = data.drop(['Survived', 'PassengerId', 'Ticket', 'Cabin'], axis=1)

# Fill missing values
X['Embarked'] = X['Embarked'].fillna(X['Embarked'].mode()[0])
X['Age'] = X['Age'].fillna(X['Age'].mean())  # Ensure Age is filled before binning

# Standardize the 'Fare' column
scaler = StandardScaler()
X['Fare'] = scaler.fit_transform(X[['Fare']])

# Extract titles from 'Name' using a corrected regex pattern with a raw string
def extract_title(name):
    title_search = re.search(r' ([A-Za-z]+)\.', name)
    if title_search:
        return title_search.group(1)
    return ""

X['Title'] = X['Name'].apply(extract_title)

# Simplify titles to common ones
title_mapping = {'Mr': 'Mr', 'Miss': 'Miss', 'Mrs': 'Mrs', 'Master': 'Master'}
X['Title'] = X['Title'].apply(lambda x: title_mapping[x] if x in title_mapping else 'Other')

# Define age bins and assign
bins = [0, 9, 14, 42, 57, 59, 100]
labels = range(len(bins) - 1)
X['AgeBin'] = pd.cut(X['Age'], bins=bins, labels=labels)

# Now drop the original 'Age' column
X = X.drop(['Age'], axis=1)

# Calculate FamilySize
X['FamilySize'] = X['SibSp'] + X['Parch'] + 1

# One hot encode 'Embarked', 'Title', and 'Sex'
X = pd.get_dummies(X, columns=['Embarked', 'Title', 'Sex'], drop_first=True)

# Drop 'Name', 'SibSp', and 'Parch' columns
X = X.drop(['Name', 'SibSp', 'Parch'], axis=1)

# Extract 'Survived' column and convert to boolean
y = data['Survived'].astype(bool)

# Combine the features with the target column
X['Survived'] = y

# Save the fully preprocessed DataFrame to a CSV file
# X.to_csv('titanic_preprocessed.csv', index=False)

X
# create tables for different parameters of classifier
k_values = range(1, 21)
metric_values = ['chebyshev', 'minkowski']
p_values = [1, 2, 3, 4, 5]  # 1 is manhattan, 2 is euclidean
search_method_values = ['ball_tree', 'kd_tree', 'brute']
weights_values = ['uniform', 'distance']
leaf_size_values = [10, 20, 30, 40, 50]  # for trees
results = []

# iterate over all possible combinations of parameters
for _ in range(1):
    start = time.time()
    for k in k_values:
        startk = time.time()
        for metric in metric_values:
            for search_method in search_method_values:
                for weight in weights_values:
                    for leaf_size in leaf_size_values:
                        for p in p_values:
                        # average the results over 10 runs
                            accuracy = 0
                            for i in range(10):
                                X_train, X_test, y_train, y_test = train_test_split(X.drop('Survived', axis=1), y, test_size=0.1)
                                knn = KNeighborsClassifier(n_neighbors=k, metric=metric, algorithm=search_method, weights=weight, leaf_size=leaf_size, p=p)
                                knn.fit(X_train, y_train)
                                y_pred = knn.predict(X_test)
                                accuracy += accuracy_score(y_test, y_pred)
                            accuracy *= 10
                            results.append((k, metric, search_method, weight, leaf_size, p, accuracy))
        endk = time.time()
        print(f'k={k} time: {endk - startk}')
    end = time.time()
    print(f'Iteration time: {end - start}')

# create a DataFrame from the results and display 10 best results
results_df = pd.DataFrame(results, columns=['k', 'metric', 'search_method', 'weight', 'leaf_size', 'p', 'accuracy'])
results_df = results_df.sort_values('accuracy', ascending=False)
print(results_df.head(10))