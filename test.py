import LinearThresholdModel as ltm
import matplotlib.pyplot as plt

y_data = [6, 8, 12, 18, 50, 53, 56, 70, 73, 163, 169, 211, 228, 269, 333, 388 ,452 ,497, 540, 692]
fractions_data = [i/692 for i in y_data]
print(fractions_data)

mean = 0.42
stdev = 0.275

ltm.set_params(meanI=mean, stdevI=stdev, seed_fracI=0.01, num_agentsI=692, num_neighborsI=5)

outputs: list[list[float]] = []

# evaluate the average of several runs:
for i in range(50):                                     # run the simulation n times, for each run:
    y_pred = ltm.run_sim(iterations=20, plot=False)     # store the predicted datapoints in y_pred
    if y_pred[-1] > 0.5:                                # if the diffusion was successfull:
        outputs.append(y_pred)                          # append y_pred to outputs

average_pred: list[float] = []              # initialize an empty array for the average of all runs

plt.figure(figsize=(10,10))
for i in range(len(outputs[0])):            # len(outputs[0]) corresponds to the number of iterations the model used
    s = 0
    for d in outputs:                       # for each dataset in the outputs array,
        plt.plot(d, color='grey', alpha=0.03, linewidth=1)
        s += d[i]                           # add the ith element of the array to a running total
    average_pred.append(s/len(outputs))     # divide the total by the length of the outputs array to get the average value for the ith iteration

print(average_pred)

plt.title(f'LTM with parameters mean = {mean}, stdev = {stdev}, predicting the Brazilian farmers dataset')

plt.plot(range(len(y_data)), fractions_data, label='dataset')
plt.plot(range(len(average_pred)), average_pred, label='averaged predictions')
plt.xlabel('timestep')
plt.ylabel('adopter fraction')
plt.legend()
plt.show()
