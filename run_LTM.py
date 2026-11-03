import LinearThresholdModel as ltm
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_squared_error


y_data = [0.01, 0.024, 0.043, 0.064, 0.094, 0.128, 0.171, 0.216, 0.247, 0.293, 0.342, 0.411, 0.494, 0.517, 0.56, 0.63, 0.72, 0.718, 0.709, 0.696, 0.675, 0.691, 0.712, 0.766, 0.792, 0.864, 0.867, 0.892, 0.904, 0.924, 0.941, 0.96, 0.973, 0.977, 0.98, 0.982, 0.983, 0.995, 0.991, 0.993, 0.995, 0.996, 0.997, 0.998, 0.998, 0.998, 0.998, 0.999, 0.999, 0.999, 0.999, 0.998, 0.997]
fractions_data = y_data 
print(fractions_data)

params: list[int] = [0.02860161601432032, 0.10197594763793821, 0.10410558814968152]

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
        plt.plot(d, color='grey', alpha=0.003, linewidth=1)
        s += d[i]                           # add the ith element of the array to a running total
    average_pred.append(s/len(outputs))     # divide the total by the length of the outputs array to get the average value for the ith iteration



plt.title(f'LTM with parameters mean = {mean}, stdev = {stdev}, fitting the refrigerator dataset. Average error: {round(np.average(errors), ndigits=3)}', wrap=True)
plt.plot(range(len(fractions_data)), fractions_data, label='dataset')
plt.plot(range(len(average_pred)), average_pred, label='average prediction')
plt.xticks(
    range(0, len(fractions_data), 5),
    range(1925, 1925 + len(fractions_data), 5)
)
plt.xlabel('year')
plt.ylabel('adopter fraction')
plt.legend()
plt.show()
