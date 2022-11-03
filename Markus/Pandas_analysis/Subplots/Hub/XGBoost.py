# Import modules
import numpy as np
from tqdm import tqdm
import pandas as pd
import os


def remover(old_list, to_be_removed):
    if type(to_be_removed) == list:
        new_list = [element for element in old_list if element not in to_be_removed]
    else:
        new_list = [element for element in old_list if element != to_be_removed and type(element) == type(to_be_removed)]
    return new_list

# Creates the dataframe from the data
filename = "Markus/Pandas_analysis/Subplots/Hub/EventData.csv"
event_data = pd.DataFrame(pd.read_csv(filename, low_memory = False))

datasets = event_data["dataset"]
particles = remover(event_data["particles"], "nan")
data_variables = remover(event_data["data_variables"], "nan")

event_data = event_data.drop(["Unnamed: 0", "dataset", "particles", "data_variables"], axis = 1)
data = np.array([event_data[column] for column in list(event_data.columns.values)])

event_data = pd.DataFrame(data = data.T, columns = pd.MultiIndex.from_tuples(zip(particles, data_variables)))




import warnings
warnings.simplefilter(action = 'ignore', category = FutureWarning)
import matplotlib.pyplot as plt
import numpy as np
import xgboost as xgb
from sklearn.datasets import load_wine
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split


# Data and real values being split
x = event_data
y = datasets
print(x.shape)
print(y.shape)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 42)
print(x_train.shape)
print(x_test.shape)
print(y_train.shape)
print(y_test.shape)


# Define the model and train it
xgb_model = xgb.XGBClassifier(objective = "multi:softprob", random_state = 22, use_label_encoder = False, eval_metric = 'mlogloss')
xgb_model = xgb.XGBClassifier(objective = "multi:softprob", random_state = 22, use_label_encoder = False, eval_metric = 'mlogloss', max_depth = 3)

# Bruk disse om det er 2 forskjellige type dataset, derfor "binary"
# xgb_model = xgb.XGBClassifier(objective = "binary:logistic", random_state = 22, use_label_encoder = False, eval_metric = 'mlogloss')
# xgb_model = xgb.XGBClassifier(objective = "binary:logistic", random_state = 22, use_label_encoder = False, eval_metric = 'mlogloss', max_depth = 3)


# Train model on data
xgb_model.fit(x_train, y_train)


# Make predictions with model
y_pred = xgb_model.predict(x_test)


# Plot confusion matrix
conf = confusion_matrix(y_test, y_pred)
disp_norm = ConfusionMatrixDisplay.from_predictions(y_test, y_pred, normalize = 'true')
disp = ConfusionMatrixDisplay(confusion_matrix = conf)
disp.plot()
plt.show()


# Plot variables by importance for prediction
sorted_idx = xgb_model.feature_importances_.argsort()
plt.barh(np.array(data_variables)[sorted_idx], xgb_model.feature_importances_[sorted_idx])
plt.xlabel("Xgboost Feature Importance")
plt.show()
