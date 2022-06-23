/**
 * @file <src/utility/loggers/SwarmMetricsLoggers.h>
 * 
 * @brief  Defines the CenterOfMassLogger, LongestPathLogger, MaximumRadiusLogger and the AverageNNDLogger
 *
 * @author Maciej Czuprynko
 */

#ifndef SWARM_METRICS_LOGGER
#define SWARM_METRICS_LOGGER

#include <limits>

#include "DataLogger.h"

/*
*   The center of mass of the swarm is computed as the sum of the positions of each robot divided by the number of robots.
*
*/
class CenterOfMassLogger: public DataLogger {
    public:
        void BeforeTheExperiment(CSimulator& cSimulator);
        void CollectData(CSimulator& cSimulator);
        void EndRun(CSimulator& cSimulator); 
        void LogDataToFile(std::ofstream& ofDataFile);
        static CVector3 FindCenterOfMass(CSimulator& cSimulator);
    private:
        std::vector<CVector3> m_vecCurrentRunCenterOfMass;
        std::vector<std::vector<CVector3>> m_vecCenterOfMass;
};

/*
*   Logs the maximum of the euclidean distances from the original position of each robot to their current position. 
*   This is done for each step of the simulation.
*/
class LongestPathLogger: public DataLogger {
    public:
        void BeforeTheExperiment(CSimulator& cSimulator);
        void CollectData(CSimulator& cSimulator);
        void EndRun(CSimulator& cSimulator); 
        void LogDataToFile(std::ofstream& ofDataFile);
    private:
        std::map<std::string, CVector3> m_mapOrigins;
        std::vector<Real> m_vecCurrentRunLongestPaths;
        std::vector<std::vector<Real>> m_vecLongestPaths;
};

/*
*   Logs the maximum of the euclidean distances from the current position to the center of mass of each robot. 
*   This is done for each step of the simulation.
*/
class MaximumRadiusLogger: public DataLogger {
    public:
        void BeforeTheExperiment(CSimulator& cSimulator);
        void CollectData(CSimulator& cSimulator);
        void EndRun(CSimulator& cSimulator); 
        void LogDataToFile(std::ofstream& ofDataFile);
    private:
        std::vector<Real> m_vecCurrentRunMaximumRadius;
        std::vector<std::vector<Real>> m_vecMaximumRadius;
};

/*
*   Logs the sum of the euclidean distance to the nearest neighbour of each robot averaged over the total number of robots.
*   This is done for each step of the simulation.
*/
class AverageNNDLogger: public DataLogger {
    public:
        void BeforeTheExperiment(CSimulator& cSimulator);
        void CollectData(CSimulator& cSimulator);
        void EndRun(CSimulator& cSimulator); 
        void LogDataToFile(std::ofstream& ofDataFile);
    private:
        std::vector<Real> m_vecCurrentRunAverageNND;
        std::vector<std::vector<Real>> m_vecAverageNND;
};

#endif