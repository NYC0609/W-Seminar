from sklearn.metrics import r2_score
import LinearThresholdModel as ltm
import pandas as pd
import numpy as np

y_data = [6, 8, 12, 18, 50, 53, 56, 70, 73, 163, 169, 211, 228, 269, 333, 388 ,452 ,497, 540, 692]
fractions_data = [i/962 for i in y_data]

thmin = 0.1
thmax = 0.9

scores: list[float] = []
thmin_values: list[float] = []
thmax_values: list[float] = []

for _ in range(100):
    thmax = 0.9
    thmin = round(thmin, ndigits=3)

    for _ in range(100):
        ltm.set_params(thetamaxI=thmax, thetaminI=thmin, num_agentsI=692, num_neighborsI=5, seed_fracI=0.1)
        
        run_: bool = True
        y_pred = []
        while run_:
            try:
                y_pred = ltm.run_sim(iterations = 20) # fit the number of iterations to the length of the dataset (20 for brfarmers)
                # print('run successfull! \n')
                run_ = False
            except:
                print('unsuccessfull run, restarting...')

        score = r2_score(y_true=fractions_data, y_pred=y_pred)
        
        """  
        # output the theta values as well as the score data
        print('*************************************************************************')
        print(f'thetamin: {thmin} \nthetamax: {thmax}')
        print(f'SCORE: {score}')
        print('*************************************************************************') 
        """

        thmax = round(thmax, ndigits=3)
        scores.append(score)
        thmin_values.append(thmin)
        thmax_values.append(thmax)

        thmax -= 0.005
    
    thmin += 0.005


def write_df() -> pd.DataFrame:
    df_out = pd.DataFrame()
    df_out['thetamin'] = thmin_values
    df_out['thetamax'] = thmax_values
    df_out['score'] = scores

    return df_out


dataframe = write_df()
print(dataframe)
print('\nbest score:')
print(dataframe.loc[dataframe['score'].idxmax()])
# run_sim(agent_numer=100, thetamax=0.58, thetamin=0.42, seed_frac=0.2, iterations=20, plot=True)