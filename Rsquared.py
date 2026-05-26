from sklearn.metrics import r2_score
from LinearThresholdModel import run_sim

y_pred = run_sim(agent_numer=100, thetamax=0.5, thetamin=0.2, iterations=20, plot=True)
print(y_pred)
