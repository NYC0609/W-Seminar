from sklearn.metrics import r2_score, mean_squared_error
import LinearThresholdModel as ltm
import pandas as pd
import numpy as np
from icecream import ic
import matplotlib.pyplot as plt

y_data = [6, 8, 12, 18, 50, 53, 56, 70, 73, 163, 169, 211, 228, 269, 333, 388 ,452 ,497, 540, 692]
fractions_data = [i/692 for i in y_data]

mean = 0.0
stdev = 0.0

scores: list[float] = []
mean_values: list[float] = []
stdev_values: list[float] = []

for _ in range(100): # increments the sdandard deviation
    for _ in range(300): # increments the mean
        ltm.set_params(meanI=mean, stdevI=stdev, seed_fracI=0.01, num_agentsI=692, num_neighborsI=10)   # set up the simulation 
        y_pred = ltm.run_sim(iterations=20, plot=False)                                                 # run the simulation
        score = mean_squared_error(y_pred=y_pred, y_true=fractions_data)                                # evaluate the MSE
        
        mean_values.append(mean)
        stdev_values.append(stdev)
        scores.append(score)

        # print(f'mean: {mean}, stdev: {stdev}     score: {score}')
        mean += 0.005    # increment mean
        mean = round(mean, ndigits=5)
    mean = 0.0
    stdev += 0.005   # increment stdev
    stdev = round(stdev, ndigits=5)

def write_df(path) -> pd.DataFrame:
    df_out = pd.DataFrame()
    df_out['mean'] = mean_values
    df_out['standard dev'] = stdev_values
    df_out['score'] = scores
    with pd.ExcelWriter(path, mode='w') as writer:
        pd.DataFrame.to_excel(df_out, writer)

    return df_out

def plot():
    ax = plt.axes(projection='3d')
    ax.scatter3D(dataframe['mean'], dataframe['standard dev'], dataframe['score'])
    ax.set_xlabel('mean')
    ax.set_ylabel('stdev')
    ax.set_zlabel('Error')
    plt.show()

dataframe = write_df('errors.xlsx')
print('\n\n\n')
print(dataframe)
print('\nbest score:')
print(dataframe.loc[dataframe['score'].idxmin()])
#plot()
# run_sim(agent_numer=100, thetamax=0.58, thetamin=0.42, seed_frac=0.2, iterations=20, plot=True)