import glob, os
import xml.etree.ElementTree as ET
import pickle
import json
import re
from pathlib import Path

from Runner import BaseRunner, create_runner
from SRDataParser import SRDataParser
from utils import execute, show, get_absolute_path

class SwarmRunner:
    """
    The SwarmRunner orchestrates the execution of the optimisation, the benchmark and the loading of the parameters defined in the 
    config_file.json file. 
    """
    _loop_functions = {}        # description of the loop functions
    _data_logger_exe = ""       # execution path of the data logger

    def __init__(self, argos_file, execution_dir, results_dir = None, robots_num = None, loop_function = None) -> None:
        self.robots_num = robots_num
        self.base_argos_file = get_absolute_path(argos_file)                    # absolute path the argos file used in the experiment
        self.execution_dir = get_absolute_path(execution_dir)                   
        self.current_argos_file = f"{self.execution_dir}/experiment.argos"      # absolute path the argos file used by the optimisers
        self.benchmar_res_file = f"{self.execution_dir}/data.csv"
        self.results_dir = get_absolute_path(results_dir)
        self.runner_list = []                                                   # list of runners
        self.benchmark_results = {}
        self.id_dict = {}                                                       # dictionary of the runners' ids with the number of apparitions 
        self.load_config()
        self.add_loop_function(loop_function)
    
    def load_config(self):
        """Loads the config_file.json file"""
        if (len(self._loop_functions) == 0):
            p = Path(__file__).with_name("config_file.json")

            with p.open("r") as config:
                data = json.load(config)
            
            data = get_absolute_paths_relative_to_file(data)

            SwarmRunner._loop_functions = data["loop_functions"]
            SwarmRunner._data_logger_exe = data["exe_paths"]["data_logger_exe"]
        
        BaseRunner.load_config(data)
    
    def add_loop_function(self, loop_function):
         if loop_function is not None:
            try:
                self.loop_function = self._loop_functions[loop_function]
            except KeyError:
                print(f"Loop function {loop_function} was not found in the config file")
                raise
    
    def add_runner(self,description):
        # makes sure that each runner has a unique id
        id = description.setdefault("id", str(description["runner"]))
        self.id_dict.setdefault(id, 0)
        if self.id_dict[id] != 0:
            description["id"] += str(self.id_dict[id])
        self.id_dict[id] += 1
            
        self.runner_list.append(create_runner(description, self.current_argos_file))
    
    def run_optimisation(self):
        for runner in self.runner_list:

            self.clear_exe_folder()
            self.build_argos_file(runner, self.robots_num)
            
            runner.run_optimisation()

            if self.results_dir is not None:
                runner.save_optimisation_results(self.results_dir)

    def clear_exe_folder(self):
        files = glob.glob(f'{self.execution_dir}/*')
        for f in files:
            os.remove(f)
    
    def benchmark(self, metrics, runs=1):

        run_number_pattern = re.compile(r"(?<=Run : )\d+")      # pattern used to keep track of the run number so that a progress 
                                                                # bar can be displayed
        metrics = list(set(metrics))

        print(f'\n\n {"-"*30} Benchmark {"-"*30}\n\n')

        print(f"Metrics being collected : {metrics} \n")

        for runner in self.runner_list:
            self.build_argos_file(runner, self.robots_num, metrics)
            cmd = f"{SwarmRunner._data_logger_exe} -n -c {self.current_argos_file} -r {runs} -f data.csv --metrics"
            for metric in metrics:
                cmd += " " + metric 

            for output in execute(cmd, self.execution_dir):
                run_num = run_number_pattern.findall(output)
                if (len(run_num) != 0):
                    show(f'Benchmarking {runner.description["id"]} ', int(run_num[0]) + 1, runs)
            self.pars_results(runner)

        self.save_results()
        return self.benchmark_results
    
    def save_results(self):
        if self.results_dir is None:
            return
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)
        with open(f"{self.results_dir}/benchamrk_results.pkl", "wb") as output_file:
            pickle.dump(self.benchmark_results, output_file)
    
    def pars_results(self, runner):
        SRDataParser.parse_results(self.benchmar_res_file, runner.description["id"], self.benchmark_results)
    
    def build_argos_file(self, runner, entities_nbr = None, metrics = None):
        base = ET.parse(self.base_argos_file)
        root = base.getroot()

        runner.add_controller(root, metrics is not None)    # if metrics are not none it means the .argos file should be build for a benchmark
        self.set_number_of_entities(root, entities_nbr)
        self.set_loop_function(root)

        with open(self.current_argos_file, 'wb') as f:
            base.write(f, xml_declaration=True)
    
    def set_number_of_entities(self, experiment, entities):
        if entities is None:
            return
        if isinstance(entities, int):
            entities = [entities]
        
        variables = experiment.findall("arena/distribute/entity")
        for i, robots in enumerate(variables):
            robots.set("quantity", str(entities[i]))
    
    def set_loop_function(self, experiment):
        if len(self.loop_function) == 0:
            return
        loop_func = experiment.findall("loop_functions")[0]
        loop_func.set("library", self.loop_function["lib"])
        loop_func.set("label", self.loop_function["label"])

def get_absolute_paths_relative_to_file(files):
    """
    Recursively searches through the varible files until the value is a string. In this case the value 
    is assumed to be a path if it contains a "/" character. If so, the path is replace by the absolute path 
    relative to the location of this file. 
    """
    path = os.path.abspath(os.path.dirname(__file__))
    for keys in files:
        if isinstance(files[keys], dict):
            files[keys] = get_absolute_paths_relative_to_file(files[keys])
            continue
        if "/" not in files[keys]:
            continue
        if os.path.isabs(files[keys]):
            continue
        files[keys] = os.path.join(path, files[keys])
    return files
    