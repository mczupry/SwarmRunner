import csv

class SRDataParser:
    """
    Parser made for the values returned by the ArgosLogger founder in the same directory as this file.
    It is used as a static function. 
    """
    @staticmethod
    def parse_results(file, runner_id, results):
        """
        Parses the results from a .csv file. It takes as arguments the file path, the runner_id and the previous 
        results. The latter will be merged with the results from the parsed file such that the number of runs 
        for the metrics collected in the .csv file is given by : current_runs = previous_runs + csv_runs.
        For instance, if the results variable contained the positions for 1 run and the .csv 2, the resulting 
        number of runs for the position metric would be 3.
        """
        current_results = {}
        with open(file, newline='') as csv_file:
            data_reader = csv.reader(csv_file)
            for row in data_reader:
                metric = row[0]
                metric_data = current_results.setdefault(metric, {})
                runner_data = metric_data.setdefault(runner_id, [])
                if metric == "Position":
                    SRDataParser._parse_position(runner_data, row[1:])
                elif metric == "BatteryLevel":
                    SRDataParser._parse_battery_level(runner_data, row[1:])
                elif metric == "ObjectiveFunction":
                    SRDataParser._parse_objective_function(runner_data, row[1:])
                elif metric == "CenterOfMass":
                    SRDataParser._parse_center_of_mass(runner_data, row[1:])
                elif metric in ["LongestPath", "MaximumRadius" ,"AverageNND"]:
                    SRDataParser._parse_real_array_per_run(runner_data, row[1:])
                else:
                    raise ValueError(f"Unrecognized metric found in results file : {metric}")
        SRDataParser._merge_results(results, current_results)

    @staticmethod
    def _parse_position(results, data):
        """
        Assumed pattern of data in : [run_num, robot_id, x0, y0, z0, x1, y1, z1, ...]
        where xyzi arer the coordinates for the step i
        """
        run_data = {}
        run_number = int(data[0])
        if run_number < len(results):
            run_data = results[run_number]
        else:
            results.append(run_data)

        robot_data = run_data.setdefault(data[1], {})
        positions = list(map(float, data[2:]))
        robot_data["x"] = positions[::3]
        robot_data["y"] = positions[1::3]
        robot_data["z"] = positions[2::3]

    @staticmethod
    def _parse_battery_level(results, data):
        """
        Assumed pattern of data in : [run_num, robot_id, bl0, bl1, ...]
        where bli is the battery level for the step i
        """
        run_data = {}
        run_number = int(data[0])
        if run_number  < len(results):
            run_data = results[run_number ]
        else:
            results.append(run_data)
            
        run_data[data[1]] = list(map(float, data[2:]))

    @staticmethod
    def _parse_objective_function(results, data):
        """
        Assumed pattern of data in : [s0, s1, s2, ...]
        where si is the score for the run i
        """
        results += list(map(float,data))

    @staticmethod
    def _parse_center_of_mass(results, data):
        """
        Assumed pattern of data in : [x0, y0, z0, x1, y1, z1, ...]
        where xyzi arer the coordinates for the step i
        """
        run_data = {}
        positions = list(map(float, data))
        run_data["x"] = positions[::3]
        run_data["y"] = positions[1::3]
        run_data["z"] = positions[2::3]
        results.append(run_data)
    
    @staticmethod
    def _parse_real_array_per_run(results, data):
        """
        Assumed pattern of data in : [r0, r1, r2, ...]
        where ri is anny real value for the step i
        """
        results.append(list(map(float, data)))
        

    @staticmethod
    def _merge_results(results, current_results):
        """
        Merges the result found in results and parsed from the .csv file.
        """
        for key in current_results:
            # if a key is not in the previous results set it now
            if key not in results:
                results[key] = current_results[key]
                continue
            # if a key is in the previous results and the value is a dict, continue merging recursively
            if isinstance(current_results[key], dict):
                SRDataParser._merge_results(results[key], current_results[key])
                continue
            # if the value is not a dict merge the values assuming they are lists
            results[key] += current_results[key] 


    