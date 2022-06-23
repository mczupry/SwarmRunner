/**
 * @file <src/utility/loggers/DataLoggerFactory.h>
 * 
 * @brief Provides a factory for the DataLoggers
 *
 * @author Maciej Czuprynko
 */



#ifndef DATA_LOGGER_FACTORY
#define DATA_LOGGER_FACTORY

#include <argos3/core/simulator/space/space.h>

#include "DataLogger.h"
#include "BasicLoggers.h"
#include "SwarmMetricsLoggers.h"

using namespace argos;

DataLogger* DataLoggerFactory(std::string sDataToLog);

#endif