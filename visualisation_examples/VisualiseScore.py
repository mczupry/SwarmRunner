import pickle
from matplotlib import pyplot as plt

#   
#   plots the box plot of the ObjectiveFunction
#

with open("../Experiment/results/benchamrk_results.pkl", "rb") as f:
    d = pickle.load(f)

scores = d["ObjectiveFunction"]
scores_list = []

for runner in scores:
    scores_list.append(scores[runner])

plt.figure()

plt.boxplot(scores_list, notch=True)

plt.ylabel("Score", fontsize=20)
plt.tick_params(axis='y', labelsize=15)
plt.xticks([1, 2], ['chocolate', 'evoStick'], fontsize=20)

plt.show()