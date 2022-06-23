/**
 * @file <src/utility/DataCollector.h>
 * 
 * @brief  Provides an easy to use class for data collection
 *
 * @author Maciej Czuprynko
 */


#ifndef DATA_COLLECTOR
#define DATA_COLLECTOR

#include <argos3/core/simulator/space/space.h>
#include <argos3/plugins/robots/e-puck/simulator/epuck_entity.h>
#include <argos3/core/simulator/simulator.h>

#include <string>
#include <iostream>
#include <vector>

#include "./loggers/DataLogger.h"
#include "./loggers/DataLoggerFactory.h"

using namespace argos;

class DataCollector {
    public :
        DataCollector() {};

        ~DataCollector() {};

        /**
         * Initialises all the DataCollectors and sets the output file 
         */
        void Init(std::vector<std::string> vecMetrics, std::string strOutputFile, CSimulator& cSimulator);

        void BeforeTheExperiment(CSimulator& cSimulator);

        void CollectDataPostStep(CSimulator& cSimulator);

        void EndRun(CSimulator& cSimulator);

        void LogDataToFile(CSimulator& cSimulator);

    private:
        std::string m_strFilename;
        std::vector<std::unique_ptr<DataLogger>> m_vecLoggers;
};

#endif