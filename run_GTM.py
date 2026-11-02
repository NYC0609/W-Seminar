import GameTheoreticModel as gtm
import matplotlib.pyplot as plt
from icecream import ic
import numpy as np
from sklearn.metrics import mean_squared_error

brfarmers = [6, 8, 12, 18, 50, 53, 56, 70, 73, 163, 169, 211, 228, 269, 333, 388, 452, 497, 540, 692]  # brfarmers dataset cumulative adopters
kfamily = [69, 163, 244, 330, 395, 457, 510, 563, 636, 673, 1047]                                      # kfamily dataset cumulative adopters
BCG_pakistan = [0.06,0.11,0.12,0.35,0.55,0.62,0.69,0.72,0.77,0.8]

y_data = BCG_pakistan    # set the dataset to be used
fractions_data = y_data
print(fractions_data)

params =  [3.5744478189968265, 0.2854016348463292, 0.2115900542817224]

alpha = round(params[0], ndigits=3)
sensitivity = round(params[1], ndigits=3)
update_prob = round(params[2], ndigits=3)

gtm.set_params(alphaI=alpha, trend_sensitivityI=sensitivity, seed_fracI=fractions_data[0], num_agentsI=1000, num_neighborsI=50, update_probI=update_prob)

outputs: list[list[float]] = []
errors = []

# evaluate the average of several runs:
for i in range(50):                                              # run the simulation n times, for each run:
    y_pred = gtm.run_sim(iterations=len(y_data), plot=False)     # store the predicted datapoints in y_pred
    if y_pred[-1] >= 0.0:                                        # if the diffusion was successfull:
        outputs.append(y_pred)                                   # append y_pred to outputs
        errors.append(mean_squared_error(y_true=fractions_data, y_pred=y_pred))

average_pred: list[float] = []              # initialize an empty array for the average of all runs

plt.figure(figsize=(8,7))
for i in range(len(outputs[0])):            # len(outputs[0]) corresponds to the number of iterations the model used
    s = 0
    for d in outputs:                       # for each dataset in the outputs array,
        plt.plot(d, color='grey', alpha=0.01, linewidth=1)
        s += d[i]                           # add the ith element of the array to a running total
    average_pred.append(s/len(outputs))     # divide the total by the length of the outputs array to get the average value for the ith iteration

plt.title(f'gtm with parameters alpha = {alpha}, trend sensitivity = {sensitivity}, predicting the vaccine dataset. Average error: {round(np.average(errors), ndigits=3)}', wrap=True)

plt.plot(range(len(y_data)), fractions_data, label='dataset')
plt.plot(range(len(average_pred)), average_pred, label='averaged predictions')
plt.xticks(range(len(fractions_data)), range(1980, 1980+len(fractions_data)))
plt.xlabel('year')
plt.ylabel('adopter fraction')
plt.legend()
plt.show()
