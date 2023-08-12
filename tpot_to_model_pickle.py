# getting the model pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.kernel_approximation import RBFSampler
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error
from tpot.export_utils import set_param_recursive




file_path = r"processed_data(9).csv"

df = pd.read_csv(file_path)
print(df.shape)
df = df.dropna()
print(df.shape)

X, y = df.drop(["Rating", "Player_Name"], axis=1), df["Rating"]
# X_train


from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)






# NOTE: Make sure that the outcome column is labeled 'target' in the data file
training_features, testing_features, training_target, testing_target = \
            train_test_split(X, y, random_state=42)

# Average CV score on the training set was: -0.09509647721159672
exported_pipeline = make_pipeline(
    PolynomialFeatures(degree=2, include_bias=False, interaction_only=False),
    RBFSampler(gamma=0.55),
    RandomForestRegressor(bootstrap=True, max_features=0.05, min_samples_leaf=7, min_samples_split=13, n_estimators=100)
)
# Fix random state for all the steps in exported pipeline
set_param_recursive(exported_pipeline.steps, 'random_state', 42)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)
# print(results)

y_pred = exported_pipeline.predict(X_test)

# Calculate RMSE
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print('RMSE:', rmse)


import joblib 
# save the model to disk
filename = 'Random_forest_CK(9).sav'
joblib.dump(exported_pipeline, filename)

# some time later...

# load the model from disk
loaded_model = joblib.load(filename)
result = loaded_model.score(X_test, y_test)
print(result)