import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler, PolynomialFeatures
from sklearn.model_selection import learning_curve, train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Masking
from tensorflow.keras.callbacks import EarlyStopping


############################################         PREPROCESSING         ############################################


# Import data
data = pd.read_csv(r'Data\Sentiment\Sentiment.csv')

# Correct the organization column for media tweets
data['organization'][data['job'] == 'Media'] = data['name'][data['job'] == 'Media']

# Drop NA's
data = data.dropna(subset=)

# Punctuation delete function
def df_punct(df):

    # Reset index
    df = df.reset_index(drop=True)

    # Delete all urls from the strings, which are almost solely used to retweet, and 'rt' which indicates a Retweet
    df['text'] = [re.sub(r'http\S+', "", txt) for txt in df['text']]
    df['text'] = [re.sub(r'rt', "", txt) for txt in df['text']]

    # Delete punctuation
    df['text'] = [re.sub(r'[^\w\s]', '', str(txt).lower().strip()) for txt in df['text']]

    return df


# Delete punctuation
data = df_punct(data)

# Creating dummy variables for job
Job = pd.get_dummies(data['job'], drop_first=True)
data = pd.concat([data, Job], axis=1).drop(columns=['job'])

# Interactions features for Goalkeepers and Defenders
for role in ['GKP', 'DEF']:
    for var in ['Goals conceded', 'Team_xGA', 'Opp_Avg_xG']:
        data.insert(len(data.columns), role + '*' + var, Role[role]*data[var])

# Interactions features for Midfielders and Forwards
for role in ['MID', 'FWD']:
    for var in ['Goals scored', 'Team_xG', 'Opp_Avg_xGA']:
        data.insert(len(data.columns), role + '*' + var, Role[role]*data[var])

# Dropping categorical columns
data = data.drop(columns=['Player', 'Team', 'Opponent', 'Sel.'])

# Dropping features which are highly unlikely to effect the dependent variable
data = data.drop(columns=['Own goals', 'Penalties saved', 'Penalties missed', 'Red cards'])

# Dropping Price fall column due to collinearity with the Price rise column
data = data.drop(columns=['Price fall'])

# Dropping the advanced xG (etc) stats which are not regularized to 90 minutes
data = data.drop(columns=['Player_xG',
                          'Player_NPxG',
                          'Player_xA',
                          'Player_xGChain',
                          'Player_xGBuildup'])

# Dropping observations with the highest number of points, which doesn't represent typical players' performance
data = data[data['Pts.'] <= 16]

# Dropping observations with negative number of points, which doesn't represent typical players' performance
data = data[data['Pts.'] >= 0]

# Dropping players who played less than 10 minutes per appearance
data = data[data['Minutes played'] / data['Player_Appearances'] > 10]

# Introduce a penalty taker dummy feature
data['Penalty taker'] = [0 if data['Player_xG90'][i] == data['Player_NPxG90'][i] else 1 for i in data.index.tolist()]

# Define X vector of independent variables and y dependent variable we want to predict (points)
X = data.drop('Pts.', axis=1)
# X = data[['Form', 'Minutes played', 'Goals scored', 'Assists', 'Clean sheets', 'Goals conceded', 'Bonus']]
y = data['Pts.']

# Introducing Polynomial Features
# trans2 = PolynomialFeatures(degree=2)
# poly2 = pd.DataFrame(trans2.fit_transform(X[['Goals scored', 'Assists', 'Cost']]))
# X = pd.concat([X.drop(columns=['Goals scored', 'Assists', 'Cost']).reset_index(drop=True), poly2.reset_index(drop=True)], axis=1)

# Feature scaling
scaler = MinMaxScaler()
scaler.fit(X)
X = scaler.transform(X)

# Define train, cross validation and test sets
# First split - train and test
X_train, X_test, y_train, y_test = train_test_split(X,
                                                    y,
                                                    test_size=0.4,
                                                    random_state=42)

# Second split - cross validation and test
X_cv, X_test, y_cv, y_test = train_test_split(X_test, y_test, test_size=0.5)


#######################################        ARTIFICIAL NEURAL NETWORK         #######################################


# Building a simple neural network
ann = Sequential()

# Add three dense layers with decreasing number of neurons, each with dropout layers
ann.add(Dense(5, activation='selu'))
ann.add(Dropout(0.5))

# Add final output layer, which will predict the number of points
ann.add(Dense(1))
ann.compile(optimizer='adam',
            loss='mse')

# Set early stopping rule
early_stop = EarlyStopping(monitor='val_loss',
                           mode='min',
                           patience=50)

# Train
ann.fit(x=X_train,
        y=y_train,
        validation_data=(X_cv, y_cv),
        batch_size=128,
        epochs=500,
        callbacks=[early_stop],
        verbose=0)


##########################################            EVALUATING             ##########################################


# Learning curve - describing test and validation errors over epochs
LC = pd.DataFrame(ann.history.history)
LC.plot()

# Checking the MSE against the true y value, to see if they are correlated
y_hats = ann.predict(X_test)
y_hats = pd.Series(y_hats.reshape(len(y_hats),))

true_hats = pd.DataFrame({'true y': y_test.values,
                          'y hat': y_hats})


# Define mse function for convenience
def mse(y_true, y_hat):
    r = np.square(np.subtract(y_true, y_hat)).mean()
    return r


# Calculate the mse for each observation
true_hats['mse'] = true_hats['true y'].apply(lambda x: mse(x, true_hats['y hat']))

sns.scatterplot(x='true y',
                y='mse',
                data=true_hats)

