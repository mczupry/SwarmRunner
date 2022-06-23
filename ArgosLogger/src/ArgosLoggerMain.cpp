/*
 * @file <src/ArgosLoggerMain.cpp>
 *
 * @author Maciej Czuprynko 
 *
 */

#include <argos3/core/simulator/simulator.h>
#include <argos3/core/simulator/space/space.h>
#include <argos3/core/simulator/entity/entity.h>
#include <argos3/core/simulator/entity/controllable_entity.h>
#include <argos3/core/utility/plugins/dynamic_loading.h>
#include <argos3/core/simulator/argos_command_line_arg_parser.h>

#include "./utility/DataCollector.h"

#include <argos3/demiurge/loop-functions/CoreLoopFunctions.h>

using namespace argos;

const std::string ExplainParameters() {
	std::string strExplanation = "Missing metrics to collect. The possible parameters are: \n\n"
		" -f | --save-file \t  Path to the file where the metrics should be saved[OPTIONAL]. \n"
		" -r | --runs \t Number of runs that the metrics sould be collect [OPTIONAL]. \n"
		" -s | --seed \t The seed for the ARGoS simulator [OPTIONAL] \n"
		" --metrics METRICS \t The metrics to collect [MANDATORY]\n"
		"\n The metrics to collect should be placed at the end of the command line, after the other parameters.";
	return strExplanation;
}

int main(int n_argc, char** ppch_argv) {

	bool bMetricsFound = false;
	UInt32 unSeed = 0;
	UInt32 unRuns = 0;
	std::string strSaveFile = "";
	DataCollector dcCollector;

	std::vector<std::string> vecMetrics;

	try {
		// Cutting off the metrics from the command line

		int nCurrentArgument = 1;
		while(!bMetricsFound && nCurrentArgument < n_argc) {
			if(strcmp(ppch_argv[nCurrentArgument], "--metrics") == 0) {
				bMetricsFound = true;
				nCurrentArgument++;
				while (nCurrentArgument < n_argc) {
					vecMetrics.push_back(std::string(ppch_argv[nCurrentArgument]));
					nCurrentArgument++;
				}
				// Do not take the metrics into account in the standard command line parsing.
				n_argc = n_argc - vecMetrics.size() - 1;
			}
			nCurrentArgument++;
		}
		if (!bMetricsFound) {
			THROW_ARGOSEXCEPTION(ExplainParameters());
		}

		// Configure the command line options
		CARGoSCommandLineArgParser cACLAP;

		cACLAP.AddArgument<std::string>('f', "save-file", "", strSaveFile);

		cACLAP.AddArgument<UInt32>('r', "runs", "", unRuns);

		cACLAP.AddArgument<UInt32>('s', "seed", "", unSeed);

		// Parse command line without taking the metrics into account
		cACLAP.Parse(n_argc, ppch_argv);

		CSimulator& cSimulator = CSimulator::GetInstance();

		switch(cACLAP.GetAction()) {
    		case CARGoSCommandLineArgParser::ACTION_RUN_EXPERIMENT: {
				CDynamicLoading::LoadAllLibraries();
				cSimulator.SetExperimentFileName(cACLAP.GetExperimentConfigFile());
				// Setting random seed. Only works with modified version of ARGoS3.
				cSimulator.SetRandomSeed(unSeed);

				cSimulator.LoadExperiment();

				dcCollector.Init(vecMetrics, strSaveFile, cSimulator);

				// Executing the experiment unRuns times 
				for (UInt32 i =  0; i < unRuns; i++){
					LOG << "Run : " << i << std::endl;
					dcCollector.BeforeTheExperiment(cSimulator);
					while (!cSimulator.IsExperimentFinished()){
						cSimulator.UpdateSpace();
						dcCollector.CollectDataPostStep(cSimulator);;
					}
					/* Needed so that the loop function are updated correctly (another way to do this would to directly call the post
					   experiment method on the loop function) */
					cSimulator.Execute();
					dcCollector.EndRun(cSimulator);
					cSimulator.Reset();
				}
				dcCollector.LogDataToFile(cSimulator);

				break;
			}

    		case CARGoSCommandLineArgParser::ACTION_QUERY:
				CDynamicLoading::LoadAllLibraries();
				// QueryPlugins(cACLAP.GetQuery());
				break;
    		case CARGoSCommandLineArgParser::ACTION_SHOW_HELP:
				cACLAP.PrintUsage(LOG);
				break;
		 	case CARGoSCommandLineArgParser::ACTION_SHOW_VERSION:
				cACLAP.PrintVersion();
				break;
      		case CARGoSCommandLineArgParser::ACTION_UNKNOWN:
				// Should never get here
				break;
		}

		cSimulator.Destroy();

	} catch(std::exception& ex) {
    // A fatal error occurred: dispose of data, print error and exit
    LOGERR << ex.what() << std::endl;
#ifdef ARGOS_THREADSAFE_LOG
    LOG.Flush();
    LOGERR.Flush();
#endif
    return 1;
  }

	/* Everything's ok, exit */
  return 0;
}
