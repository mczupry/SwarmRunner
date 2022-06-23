from SwarmRunner import SwarmRunner


# defining parameters
execution_dir = "./Experiment/current_experiment"
argos_file = "./Experiment/example_argos_file.argos"
result_dir = "./Experiment/results"


# defining the chocolate and evoStick runners
chocolate = {
    "id":"chocolate",
    "runner": "automode_chocolate",
    "controller":"./controllers/automode_controller.xml",
    "wd": "./Experiment/chocolate",
    "execDir" : "execution-folder"
}

evoStick = {
    "id":"evoStick",
    "runner": "neat",
    "controller":"./controllers/neat_controller.xml",
    "wd": "./Experiment/evoStick",
    "parameters": "evostickParams.ne",
    "startGen": "evostickstartgenesRM11"
}

# initialise the experiment
experiment = SwarmRunner(argos_file, execution_dir, result_dir, robots_num = 5 , loop_function = "lcn")

# adds the runners to the experiment
experiment.add_runner(chocolate)
experiment.add_runner(evoStick)

# runs the optimisation 
experiment.run_optimisation()

# collects the metrics
experiment.benchmark(["ObjectiveFunction"], 100)
experiment.benchmark(["CenterOfMass","Position", "BatteryLevel"], 1)
experiment.benchmark(["LongestPath", "MaximumRadius" ,"AverageNND"], 1)