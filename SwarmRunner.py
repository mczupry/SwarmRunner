import configparser, os, subprocess
import re
from pathlib import Path
import glob
import shutil
from tkinter import N
import xml.etree.ElementTree as ET

class SwarmRunner:
    def __init__(self, argos_file_dir:str, entities_per_run = None) -> None:
        if not os.path.isabs(argos_file_dir):
            argos_file_dir = f"{os.getcwd()}/{argos_file_dir}"
        self.entities_per_run = entities_per_run
        self.argos_file_dir = argos_file_dir
        self.argos_file = f'{argos_file_dir}/current_experiment/experiment.argos'
        self.runner_list = []
        self.results = {}
    
    def add_runner(self,description:dict) -> None:
        self.runner_list.append(create_runner(description, self.argos_file))
    
    def run_optimization(self):
        for runner in self.runner_list:
            self.build_argos_file(runner.description["wd"], self.entities_per_run)
            runner.run_optimization(self.argos_file)
    
    def benchmark(self, metrics, runs=10):
        results = {}
        for i, runner in enumerate(self.runner_list):
            self.build_argos_file(runner.description["wd"], self.entities_per_run)
            runner.run_benchmark(metrics, runs)
            results[i] = runner.get_benchmark_results()
        return results
    
    def build_argos_file(self, wd, entities_nbr = None):
        experiment_files = glob.glob(f'{self.argos_file_dir}/*.argos') + glob.glob(f'{self.argos_file_dir}/*.xml') 
        if self.argos_file in experiment_files:
            experiment_files.remove(self.argos_file)
        shutil.copyfile(experiment_files[0], self.argos_file)
        base = ET.parse(self.argos_file)
        ref = ET.parse(f'{wd}/controllers.xml')
        root = base.getroot()
        subroot = ref.getroot()

        elem = root.find('controllers')
        if elem is not None:
            root.remove(elem)
        root.append(subroot)
        
        if entities_nbr is not None:
            self.set_number_of_entities(root, entities_nbr)

        with open(self.argos_file, 'wb') as f:
            base.write(f, xml_declaration=True)
    
    def set_number_of_entities(self, experiment, entities):
        if isinstance(entities, int):
            entities = [entities]
        
        variables = experiment.findall("arena/distribute/entity")
        for i, robots in enumerate(variables):
            robots.set('quantity', str(entities[i]))

class Runner:
    exe_paths = {
        "AUTOMODE_EXEC": "automode_main",
        "ARGOS_EXEC":"argos3",
        "IRACE_EXEC": "irace",
        "NEAT_OPTIMIZATION_EXEC": "/home/maciej/SwarmRunner/argos3-NEAT/bin/NEAT-evolution",
        "NEAT_EXEC": "/home/maciej/SwarmRunner/argos3-NEAT/bin/NEAT-launch"
    }

    metric_patterns = {
        "score": re.compile(r"(?<=Score = ).+"),
        "seed": re.compile(r"(?<=seed = ).+")
    }
    
    metric_type = {
        "score": float,
        "seed": int
    }

    def load_config(self) -> dict:
        p = Path(__file__).with_name("config_file.ini")

        parser = configparser.ConfigParser()

        with p.open("r") as config:
            parser.read_file(config)
        return dict(parser["General"])
    
    def __init__(self) -> None:
        self.results = {}
        self.description = {
            "options" : "",
            "wd" : "./"
        }
        self.argos_file = ""

    def run_optimization(self, argos_file:str) -> None:
        pass

    def run_benchmark(self, metrics, runs):
        pass

    def _run_benchmark(self, cmd, wd, metrics, runs):
        for key in metrics:
            self.results[key] = []

        for _ in range(runs):
            for output in self.execute(cmd, wd):
                for key in metrics:
                    res = self.metric_patterns[key].findall(output)
                    if res:
                        self.results[key] += res
        for key in self.results:
            self.results[key] = list(map(self.metric_type[key], self.results[key]))

    def get_benchmark_results(self) -> str:
        return self.results
    
    def add_description(self,description):
        self.description.update(description)
    
    def add_argos_file(self,argos_file):
        self.argos_file = argos_file

    def execute(self, cmd, wd = "./"):
        popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True, shell = True, cwd = wd)
        for stdout_line in iter(popen.stdout.readline, ""):
            yield stdout_line 
        popen.stdout.close()
        return_code = popen.wait()
        if return_code:
            raise subprocess.CalledProcessError(return_code, cmd)
        


class NoRunner(Runner):
    def run_benchmark(self, metrics, runs):
        cmd = f'{self.exe_paths["ARGOS_EXEC"]} -c {self.argos_file} -n'
        wd = os.path.dirname(self.argos_file)

        self._run_benchmark(cmd, wd, metrics, runs)


class IraceRunner(Runner):
    def __init__(self) -> None:
        self.optimized_pfsms = []
        super().__init__()

    def run_optimization(self, argos_file):
        if "options" in self.description:
            options = f'{self.description["options"]}'
        if "wd" in self.description:
            wd = self.description["wd"]
        cmd = f'{self.exe_paths["IRACE_EXEC"]} {options}'

        result_pattern = re.compile(r"\d*\s*(--nstates.*)")
        
        for output in self.execute(cmd, wd):
            res = result_pattern.findall(output)
            if res:
                self.optimized_pfsms += res
            print(output, end="")
    
    def run_benchmark(self, metrics, runs):
        cmd = f'{self.exe_paths["AUTOMODE_EXEC"]} -c {self.argos_file} -n --fsm-config {self.optimized_pfsms[0]}'
        wd = self.description["wd"]

        self._run_benchmark(cmd, wd, metrics, runs)

class NEATRunner(Runner):
    def run_optimization(self, argos_file):
        if "options" in self.description:
            options = f'{self.description["options"]}'
        if "wd" in self.description:
            wd = self.description["wd"]
        cmd = f'{self.exe_paths["NEAT_OPTIMIZATION_EXEC"]} {self.argos_file} {self.description["parameters"]} {self.description["startGen"]} {options}'
        
        for output in self.execute(cmd, wd):
            print(output, end="")
    
    def run_benchmark(self, metrics, runs):
        wd = self.description["wd"]
        champ_gen = f'{wd}/gen/gen_last_1_champ'
        cmd = f'{self.exe_paths["NEAT_EXEC"]} -c {self.argos_file} -n -g {champ_gen}'
        
        self._run_benchmark(cmd, wd, metrics, runs)
    

def create_runner(description:dict, argos_file) -> Runner:
    runner_types = {
        None: NoRunner(),
        "irace": IraceRunner(),
        "neat": NEATRunner()
    }
    runner = runner_types[description["algorithm"]]
    runner.add_description(description)
    runner.add_argos_file(argos_file)
    return runner