/**
 * @file <src/utility/loggers/BasicLoggers.h>
 * 
 * @brief Defines the PositionLogger, BatteryLevelLogger and the ObjectiveFunctionLogger
 *
 * @author Maciej Czuprynko
 */

#ifndef BASIC_LOGGERS
#define BASIC_LOGGERS

#include <argos3/plugins/robots/e-puck/simulator/battery_equipped_entity.h>
#include <argos3/core/simulator/loop_functions.h>
#include <argos3/demiurge/loop-functions/CoreLoopFunctions.h>

#include "DataLogger.h"

class PositionLogger : public DataLogger {
    public:
        void BeforeTheExperiment(CSimulator& cSimulator) ;
        void CollectData(CSimulator& cSimulator) ;
        void EndRun(CSimulator& cSimulator);
        void LogDataToFile(std::ofstream& ofDataFile) ;
    private:
        std::map<std::string, std::vector<CVector3>> m_mapCurrentRunPositions;
        std::vector<std::map<std::string, std::vector<CVector3>>> m_vecPositions;
};

class BatteryLevelLogger : public DataLogger {
    public:
        void BeforeTheExperiment(CSimulator& cSimulator);
        void CollectData(CSimulator& cSimulator);
        void EndRun(CSimulator& cSimulator);
        void LogDataToFile(std::ofstream& ofDataFile) ;
    private:
        std::map<std::string, std::vector<Real>> m_mapCurrentRunBatteryLevels;
        std::vector<std::map<std::string, std::vector<Real>>> m_vecBatteryLevels;
};

class ObjectiveFunctionLogger: public DataLogger {
    public:
        void BeforeTheExperiment(CSimulator& cSimulator);
        void CollectData(CSimulator& cSimulator);
        void EndRun(CSimulator& cSimulator);
        void LogDataToFile(std::ofstream& ofDataFile);
    private:
        std::vector<Real> m_vecScores;
};

#endif