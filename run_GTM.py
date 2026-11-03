import GameTheoreticModel as gtm
import matplotlib.pyplot as plt
from icecream import ic
import numpy as np
from sklearn.metrics import mean_squared_error

y_data = [0.01, 0.024, 0.043, 0.064, 0.094, 0.128, 0.171, 0.216, 0.247, 0.293, 0.342, 0.411, 0.494, 0.517, 0.56, 0.63, 0.72, 0.718, 0.709, 0.696, 0.675, 0.691, 0.712, 0.766, 0.792, 0.864, 0.867, 0.892, 0.904, 0.924, 0.941, 0.96, 0.973, 0.977, 0.98, 0.982, 0.983, 0.995, 0.991, 0.993, 0.995, 0.996, 0.997, 0.998, 0.998, 0.998, 0.998, 0.999, 0.999, 0.999, 0.999, 0.998, 0.997]
fractions_data = y_data
print(fractions_data)

params = [1.3047334590065103, 0.3477860886329542, 0.11141083105647628]
print(1925+len(y_data))

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
plt.xticks(
    range(0, len(fractions_data), 5),
    range(1925, 1925 + len(fractions_data), 5)
)
plt.xlabel('year')
plt.ylabel('adopter fraction')
plt.legend()
plt.show()
