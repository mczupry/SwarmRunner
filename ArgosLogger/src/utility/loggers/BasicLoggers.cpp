#include "BasicLoggers.h"

/********************************************************************************/
/*********************************** Position ***********************************/
/********************************************************************************/

void PositionLogger::BeforeTheExperiment(CSimulator& cSimulator) {}

void PositionLogger::CollectData(CSimulator& cSimulator) {
    CEPuckEntity* pcEpuck;
    CSpace::TMapPerType& tEpuckMap = cSimulator.GetSpace().GetEntitiesByType("epuck");
    for (CSpace::TMapPerType::iterator it = tEpuckMap.begin(); it != tEpuckMap.end(); ++it) {
        pcEpuck = any_cast<CEPuckEntity*>(it->second);
        m_mapCurrentRunPositions[it->first].push_back(pcEpuck->GetEmbodiedEntity().GetOriginAnchor().Position);
    }
}

void PositionLogger::EndRun(CSimulator& cSimulator) {
    m_vecPositions.push_back(m_mapCurrentRunPositions);
    m_mapCurrentRunPositions.clear();
}

void PositionLogger::LogDataToFile(std::ofstream& ofDataFile) {
    for (size_t i = 0; i <  m_vecPositions.size(); i++) {
        for (auto it = m_vecPositions[i].begin(); it != m_vecPositions[i].end(); it++) {
            std::stringstream ssInput;
            ssInput << "Position," << i << "," << it->first;
            for (auto position : it->second) {
                ssInput << "," << position;
            }
            ofDataFile << ssInput.str() << std::endl; 
        }
    }
}


/********************************************************************************/
/********************************* BatteryLevel *********************************/
/********************************************************************************/

void BatteryLevelLogger::BeforeTheExperiment(CSimulator& cSimulator) {}

void BatteryLevelLogger::CollectData(CSimulator& cSimulator) {
    CEPuckEntity* pcEpuck;
    CSpace::TMapPerType& tEpuckMap = cSimulator.GetSpace().GetEntitiesByType("epuck");
    for (CSpace::TMapPerType::iterator it = tEpuckMap.begin(); it != tEpuckMap.end(); ++it) {
        pcEpuck = any_cast<CEPuckEntity*>(it->second);
        m_mapCurrentRunBatteryLevels[it->first].push_back(pcEpuck->GetBatteryEquippedEntity().BatteryLevel());
    }
}
void BatteryLevelLogger::EndRun(CSimulator& cSimulator) {
    m_vecBatteryLevels.push_back(m_mapCurrentRunBatteryLevels);
    m_mapCurrentRunBatteryLevels.clear();
}
void BatteryLevelLogger::LogDataToFile(std::ofstream& ofDataFile) {
    for (size_t i = 0; i <  m_vecBatteryLevels.size(); i++) {
        for (auto it = m_vecBatteryLevels[i].begin(); it != m_vecBatteryLevels[i].end(); it++) {
            std::stringstream ssInput;
            ssInput << "BatteryLevel," << i << "," << it->first;
            for (auto batteryLevel : it->second) {
                ssInput << "," << batteryLevel;
            }
            ofDataFile << ssInput.str() << std::endl; 
        }
    }
}

/********************************************************************************/
/****************************** ObjectiveFunction *******************************/
/********************************************************************************/

void ObjectiveFunctionLogger::BeforeTheExperiment(CSimulator& cSimulator) {}
void ObjectiveFunctionLogger::CollectData(CSimulator& cSimulator) {}

void ObjectiveFunctionLogger::EndRun(CSimulator& cSimulator) {
    CoreLoopFunctions& cLoopFunctions = dynamic_cast<CoreLoopFunctions&>(cSimulator.GetLoopFunctions());
    m_vecScores.push_back(cLoopFunctions.GetObjectiveFunction());
}
void ObjectiveFunctionLogger::LogDataToFile(std::ofstream& ofDataFile) {
    std::stringstream ssOutput;
    ssOutput << "ObjectiveFunction";
    for (auto scores : m_vecScores) {
        ssOutput << "," << scores;
    }
    ofDataFile << ssOutput.str() << std::endl;
}


