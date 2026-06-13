from sklearn.metrics import r2_score
import LinearThresholdModel as ltm
import pandas as pd
import numpy as np
from icecream import ic

y_data = [6, 8, 12, 18, 50, 53, 56, 70, 73, 163, 169, 211, 228, 269, 333, 388 ,452 ,497, 540, 692]
fractions_data = [i/962 for i in y_data]

mean = 0.0
stdev = 0.001

scores: list[float] = []
mean_values: list[float] = []
stdev_values: list[float] = []

for _ in range(100): # increments the sdandard deviation
    for _ in range(100): # increments the mean
        ltm.set_params(meanI=mean, stdevI=stdev, seed_fracI=0.1, num_agentsI=692, num_neighborsI=5)    
        y_pred = ltm.run_sim(iterations=20, plot=False)
        score = r2_score(y_pred=y_pred, y_true=fractions_data)
        
        mean_values.append(mean)
        stdev_values.append(stdev)
        scores.append(score)

        print(f'mean: {mean}, stdev: {stdev}     score: {score}')
        mean += 0.01
        mean = round(mean, ndigits=2)
    mean = 0.0
    stdev += 0.001
    stdev = round(stdev, ndigits=3)

def write_df() -> pd.DataFrame:
    df_out = pd.DataFrame()
    df_out['mean'] = mean_values
    df_out['standard dev'] = stdev_values
    df_out['score'] = scores

    return df_out


dataframe = write_df()
print('\n\n\n')
print(dataframe)
print('\nbest score:')
print(dataframe.loc[dataframe['score'].idxmax()])
# run_sim(agent_numer=100, thetamax=0.58, thetamin=0.42, seed_frac=0.2, iterations=20, plot=True)