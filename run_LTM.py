import LinearThresholdModel as ltm
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_squared_error

brfarmers = [6, 8, 12, 18, 50, 53, 56, 70, 73, 163, 169, 211, 228, 269, 333, 388, 452, 497, 540, 692]  # brfarmers dataset cumulative adopters
kfamily = [69, 163, 244, 330, 395, 457, 510, 563, 636, 673, 1047]                                      # kfamily dataset cumulative adopters
BCG_pakistan = [0.06,0.11,0.12,0.35,0.55,0.62,0.69,0.72,0.77,0.8]                   # vaccine dataset percentages

y_data = kfamily    # set the dataset to be used
fractions_data = BCG_pakistan 
print(fractions_data)

params: list[int] = [0.0847444644049907, 0.05433910381268331, 0.2259887339546392]

mean =  round(params[0], ndigits=3)
stdev = round(params[1], ndigits=3)
update_prob = round(params[2], ndigits=3)

ltm.set_params(meanI=mean, stdevI=stdev, seed_fracI=fractions_data[0], num_agentsI=500, num_neighborsI=10, update_probI=update_prob)

outputs: list[list[float]] = []
errors:  list[float]       = []


# evaluate the average of several runs:
for i in range(50):                                              # run the simulation n times, for each run:
    y_pred = np.array(ltm.run_sim(iterations=len(fractions_data), plot=False))   # store the predicted datapoints in y_pred
    if y_pred[-1] > 0.5:                                        # if the diffusion was successfull:
        errors.append(mean_squared_error(y_true=fractions_data, y_pred=y_pred))
        outputs.append(1*y_pred)                                  # append y_pred to outputs

average_pred: list[float] = []              # initialize an empty array for the average of all runs

plt.figure(figsize=(8,7))
for i in range(len(outputs[0])):            # len(outputs[0]) corresponds to the number of iterations the model used
    s = 0
    for d in outputs:                       # for each dataset in the outputs array,
        plt.plot(d, color='grey', alpha=0.01, linewidth=1)
        s += d[i]                           # add the ith element of the array to a running total
    average_pred.append(s/len(outputs))     # divide the total by the length of the outputs array to get the average value for the ith iteration



plt.title(f'LTM with parameters mean = {mean}, stdev = {stdev}, predicting the Pakistan Vaccine dataset. Average error: {round(np.average(errors), ndigits=3)}', wrap=True)
plt.plot(range(len(fractions_data)), fractions_data, label='dataset')
plt.plot(range(len(average_pred)), average_pred, label='average prediction')
plt.xticks(range(len(fractions_data)), range(1980, 1980+len(fractions_data)))
plt.xlabel('year')
plt.ylabel('adopter fraction')
plt.legend()
plt.show()
