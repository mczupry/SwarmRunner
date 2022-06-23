/**
 * @file <src/utility/loggers/DataLogger.h>
 * 
 * @brief Provides an interface for the DataLoggers
 *
 * @author Maciej Czuprynko
 */


#ifndef DATA_LOGGER
#define DATA_LOGGER

#include <argos3/core/simulator/space/space.h>
#include <argos3/plugins/robots/e-puck/simulator/epuck_entity.h>
#include <argos3/core/simulator/simulator.h>

#include <vector>
#include <map>
#include <string>
#include <iostream>
#include <sstream>

using namespace argos;

class DataLogger {
    public:
        virtual void BeforeTheExperiment(CSimulator& cSimulator) = 0;
        virtual void CollectData(CSimulator& cSimulator) = 0;
        virtual void EndRun(CSimulator& cSimulator) = 0;
        virtual void LogDataToFile(std::ofstream& ofDataFile) = 0;
};

#endif