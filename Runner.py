from abc import abstractmethod, ABC
import os, shutil
from utils import execute, get_absolute_path
import re
import xml.etree.ElementTree as ET

class BaseRunner(ABC):
    """
    Defines the base runner. The role of the runner is to set up the controller in the .argos file, run 
    the optimisation and save the resulting configurations. This class should not be instantiated directly. 
    """
    exe_paths = {}
    controllers = {}

    def __init__(self):
        #default values of the description
        self.description = {
            "options" : "",
            "wd" : "./",
        }
        self.argos_file = ""

    @staticmethod
    def load_config(data):
        """
        Loads the execution paths defined in the data 
        """
        if not (len(BaseRunner.exe_paths) == 0 and len(BaseRunner.exe_paths) == 0):
            return
        if "exe_paths" in data:
            BaseRunner.exe_paths = data["exe_paths"]
    
    @abstractmethod
    def run_optimisation(self):
        """Runs the optimisation. Should be defined in derived classes."""
        pass

    @abstractmethod
    def save_optimisation_results(self, results_dir):
        """Saves the results of optimisation in the results_dir. Should be defined in derived classes."""
        pass

    @abstractmethod
    def prepare_benchmark_argos_file(self, root):
        """Prepares the controls located in the variable root for a benchmark. Should be defined in derived classes."""
        pass
    
    def add_description(self, description):
        self.description.update(description)
        self.description["wd"] = get_absolute_path(self.description["wd"])
    
    def add_argos_file(self,argos_file):
        """Sets the path to the argos file used in optimisations"""
        self.argos_file = argos_file
    
    def add_controller(self, root, for_betchmark = False):
        """Adds the controller to the argos file"""
        controller_path = get_absolute_path(self.description["controller"])
        controller = ET.parse(controller_path)
        controller_root = controller.getroot()

        elem = root.find("controllers")
        if elem is not None:
            root.remove(elem)
        root.append(controller_root)

        if for_betchmark:
            self.prepare_benchmark_argos_file(root)
        

class NoRunner(BaseRunner):
    """
    This runner should be used if some predefined controls needs to be benchmaked 
    and do not need to be optimised.
    """
    def run_optimisation(self):
        pass

    def save_optimisation_results(self, results_dir):
        pass

    def prepare_benchmark_argos_file(self, root):
        pass

class AutomodeChocolateRunner(BaseRunner, ABC):
    """
    Implements AutoMoDe-chocolate that can be found here https://github.com/demiurge-project/ARGoS3-AutoMoDe. 
    The controller that is used for the benchmarks, is the first configuration of the probabilistic finite state machine 
    returned by the IRace algorithm.
    In the result_dir are saved : all the configurations returned by IRace and the .Rdata file found in the working directory.
    """

    def __init__(self):
        self.optimized_pfsms = []
        super().__init__()

    def run_optimisation(self):
        if "options" in self.description:
            options = f'{self.description["options"]}'
        if "wd" in self.description:
            wd = self.description["wd"]
        cmd = f'{BaseRunner.exe_paths["irace_exe"]} {options}'

        result_pattern = re.compile(r"(\d*)\s*(--nstates.*)")
        
        for output in execute(cmd, wd):
            res = result_pattern.findall(output)
            if res:
                self.optimized_pfsms += res
            print(output, end="")
    
    def save_optimisation_results(self, results_dir):
        results_dir += f'/{self.description["id"]}'

        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
        
        # saves the parsed configurations
        with open(f"{results_dir}/best_configurations.txt", "w") as f:
            for pfsms in self.optimized_pfsms:
                f.write(f"{pfsms[0]} {pfsms[1]}\n")

        # saves the contents of the execDir, such as the .Rdata file containing the optimisation history
        optimization_res_dir = f'{self.description["wd"]}/{self.description["execDir"]}'
        for file in os.listdir(optimization_res_dir):
            shutil.copy(f"{optimization_res_dir}/{file}", results_dir)

    def prepare_benchmark_argos_file(self, root):
        """Adds the optimised pfsm to the controller"""
        params = root.find("controllers").getchildren()[0].find("params")
        params.set("fsm-config", self.optimized_pfsms[0][1])

class NEATRunner(BaseRunner):
    """
    Implements NEAT that can be found here https://github.com/demiurge-project/ARGoS3-NEAT. 
    The controller that is used for the benchmarks, is the champion from the last generation of the first run. It can
    be found in the gen/ directory which itself is in the working directory.
    In the result_dir are saved : all the contents of the gen/ directory.
    """

    def run_optimisation(self):
        if "options" in self.description:
            options = self.description["options"]
        if "wd" in self.description:
            wd = self.description["wd"]
        cmd = f'{BaseRunner.exe_paths["neat_optimization_exe"]} {self.argos_file} {self.description["parameters"]} {self.description["startGen"]} {options}'
        
        for output in execute(cmd, wd):
            print(output, end="")
    
    def save_optimisation_results(self, results_dir):
        results_dir += f'/{self.description["id"]}'

        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        execution_dir = f'{self.description["wd"]}/gen'
        for file in os.listdir(execution_dir):
            shutil.copy(f"{execution_dir}/{file}", results_dir)
    
    def prepare_benchmark_argos_file(self, root):
        """Adds to the controller the genome of the champion from last generation from the first run"""
        params = root.find("controllers").getchildren()[0].find("params")
        params.set("genome_file", f'{self.description["wd"]}/gen/gen_last_1_champ')

def create_runner(description, argos_file) -> BaseRunner:
    """factory for the BaseRunner to which a description and an argos_file are added"""
    runner_types = {
        "none": NoRunner(),
        "automode_chocolate": AutomodeChocolateRunner(),
        "neat": NEATRunner()
    }
    try:
        runner = runner_types[description["runner"]]
    except KeyError:
        print(f"Runner {description['runner']} was not defined as a valid runner")
        raise
    runner.add_description(description)
    runner.add_argos_file(argos_file)
    return runner