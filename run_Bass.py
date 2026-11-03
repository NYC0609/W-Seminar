import Bass
import matplotlib.pyplot as plt
from icecream import ic
import numpy as np
from sklearn.metrics import mean_squared_error

refrigerator_data = [0.01, 0.024, 0.043, 0.064, 0.094, 0.128, 0.171, 0.216, 0.247, 0.293, 0.342, 0.411, 0.494, 0.517, 0.56, 0.63, 0.72, 0.718, 0.709, 0.696, 0.675, 0.691, 0.712, 0.766, 0.792, 0.864, 0.867, 0.892, 0.904, 0.924, 0.941, 0.96, 0.973, 0.977, 0.98, 0.982, 0.983, 0.995, 0.991, 0.993, 0.995, 0.996, 0.997, 0.998, 0.998, 0.998, 0.998, 0.999, 0.999, 0.999, 0.999, 0.998, 0.997]

y_data = refrigerator_data    # set the dataset to be used
fractions_data = y_data
print(fractions_data)

params =  [0.02300001905860038, 0.12289924179249556]

p = round(params[0], ndigits=3)
q = round(params[1], ndigits=3)


outputs: list[list[float]] = []

t, y_pred = Bass.solve_bass(p=p, q=q, y0=fractions_data[0], t_max=len(fractions_data)-1, num_points=len(fractions_data))
error = mean_squared_error(y_true=fractions_data, y_pred=y_pred)

plt.title(f'Bass Diffusion Model with parameters p = {p}, q = {q}, fitting the refrigerator dataset. error: {round(error, ndigits=3)}', wrap=True)

plt.plot(range(len(y_data)), fractions_data, label='dataset')
plt.plot(t, y_pred, label='averaged predictions')
plt.xticks(
    range(0, len(fractions_data), 5),
    range(1925, 1925 + len(fractions_data), 5)
)
plt.xlabel('year')
plt.ylabel('adopter fraction')
plt.tight_layout()
plt.legend()
plt.show()
