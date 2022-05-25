from SwarmRunner import SwarmRunner
from matplotlib import pyplot as plt

argos_file_dir = "/home/maciej/SwarmRunner/SwarmRunnerProject/Experiment/experiments"

human = {
    "algorithm": None,
    "fsm": "--nstates 3 --s0 0 --rwm0 4 --n0 1 --n0x0 1 --c0x0 0 --p0x0 0.56 --s1 1 --n1 1 --n1x0 1 \
    --c1x0 5 --p1x0 0.1 --s2 4 --att2 3.79 --n2 2 --n2x0 0 --c2x0 3 --p2x0 10 --w2x0 12.99 --n2x1 1 --c2x1 0 --p2x1 0.9"
}


irace = {
    "algorithm": "irace",
    "wd": "/home/maciej/SwarmRunner/SwarmRunnerProject/Experiment/irace"
}

neat = {
    "algorithm": "neat",
    "wd": "/home/maciej/SwarmRunner/SwarmRunnerProject/Experiment/neat",
    "parameters": "evostickParams.ne",
    "startGen": "evostickstartgenesRM11"
}

experiment = SwarmRunner(argos_file_dir, 10)
#experiment.add_runner(human)
experiment.add_runner(neat)
experiment.add_runner(irace)
experiment.run_optimization()
results = experiment.benchmark(["score"], 50)
list_of_results = []
for res in results:
    list_of_results.append(results[res]["score"])
plt.figure()
plt.boxplot(list_of_results, notch=True)
plt.show()