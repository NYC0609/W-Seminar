from sklearn.metrics import r2_score
from LinearThresholdModel import run_sim

y_pred = run_sim(agent_numer=100, thetamax=0.3, thetamin=0.2, plot=False)
print(y_pred)
