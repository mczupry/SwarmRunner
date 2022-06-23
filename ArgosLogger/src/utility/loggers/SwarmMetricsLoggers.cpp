#include "SwarmMetricsLoggers.h"

/**
*   Function that finds the center of mass of the swarm
*/
CVector3 CenterOfMassLogger::FindCenterOfMass(CSimulator& cSimulator) {
    CEPuckEntity* pcEpuck;
    CSpace::TMapPerType& tEpuckMap = cSimulator.GetSpace().GetEntitiesByType("epuck");
    CVector3 vPosSum = CVector3();
    for (CSpace::TMapPerType::iterator it = tEpuckMap.begin(); it != tEpuckMap.end(); ++it) {
        pcEpuck = any_cast<CEPuckEntity*>(it->second);
        vPosSum += pcEpuck->GetEmbodiedEntity().GetOriginAnchor().Position;
    }
    return vPosSum / tEpuckMap.size();
}


/********************************************************************************/
/********************************* CenterOfMass *********************************/
/********************************************************************************/

void CenterOfMassLogger::BeforeTheExperiment(CSimulator& cSimulator) {}
void CenterOfMassLogger::CollectData(CSimulator& cSimulator) {
    m_vecCurrentRunCenterOfMass.push_back(CenterOfMassLogger::FindCenterOfMass(cSimulator));
}
void CenterOfMassLogger::EndRun(CSimulator& cSimulator) {
    m_vecCenterOfMass.push_back(m_vecCurrentRunCenterOfMass);
    m_vecCurrentRunCenterOfMass.clear();
}
void CenterOfMassLogger::LogDataToFile(std::ofstream& ofDataFile) {
    for (size_t i = 0; i <  m_vecCenterOfMass.size(); i++) {
        std::stringstream ssInput;
        ssInput << "CenterOfMass";
        for (auto centerOfMass : m_vecCenterOfMass[i]) {
            ssInput << ',' << centerOfMass;
        }
        ofDataFile << ssInput.str() << std::endl; 
    }
}

/********************************************************************************/
/********************************* LongestPath **********************************/
/********************************************************************************/

void LongestPathLogger::BeforeTheExperiment(CSimulator& cSimulator) {
    CEPuckEntity* pcEpuck;
    CSpace::TMapPerType& tEpuckMap = cSimulator.GetSpace().GetEntitiesByType("epuck");
    for (CSpace::TMapPerType::iterator it = tEpuckMap.begin(); it != tEpuckMap.end(); ++it) {
        pcEpuck = any_cast<CEPuckEntity*>(it->second);
        m_mapOrigins[it->first] = pcEpuck->GetEmbodiedEntity().GetOriginAnchor().Position;
    }
}
void LongestPathLogger::CollectData(CSimulator& cSimulator) {
    CEPuckEntity* pcEpuck;
    CSpace::TMapPerType& tEpuckMap = cSimulator.GetSpace().GetEntitiesByType("epuck");
    Real fMaxDistanceSquared = 0.0;
    Real fDistanceFromOrigin;
    for (CSpace::TMapPerType::iterator it = tEpuckMap.begin(); it != tEpuckMap.end(); ++it) {
        pcEpuck = any_cast<CEPuckEntity*>(it->second);
        fDistanceFromOrigin = (pcEpuck->GetEmbodiedEntity().GetOriginAnchor().Position - m_mapOrigins[pcEpuck->GetId()]).SquareLength();
        if (fDistanceFromOrigin > fMaxDistanceSquared) {
            fMaxDistanceSquared = fDistanceFromOrigin;
        }
    }
    m_vecCurrentRunLongestPaths.push_back(Sqrt(fMaxDistanceSquared));
}
void LongestPathLogger::EndRun(CSimulator& cSimulator) {
    m_vecLongestPaths.push_back(m_vecCurrentRunLongestPaths);
    m_vecCurrentRunLongestPaths.clear();
    m_mapOrigins.clear();
}; 
void LongestPathLogger::LogDataToFile(std::ofstream& ofDataFile) {
    for (size_t i = 0; i <  m_vecLongestPaths.size(); i++) {
        std::stringstream ssInput;
        ssInput << "LongestPath";
        for (auto longestPath : m_vecLongestPaths[i]) {
            ssInput << ',' << longestPath;
        }
        ofDataFile << ssInput.str() << std::endl; 
    }
}


/********************************************************************************/
/********************************* MaximumRadius ********************************/
/********************************************************************************/


void MaximumRadiusLogger::BeforeTheExperiment(CSimulator& cSimulator) {}
void MaximumRadiusLogger::CollectData(CSimulator& cSimulator) {
    CEPuckEntity* pcEpuck;
    CSpace::TMapPerType& tEpuckMap = cSimulator.GetSpace().GetEntitiesByType("epuck");
    CVector3 cCenterOfMass = CenterOfMassLogger::FindCenterOfMass(cSimulator);
    Real fMaxDistanceSquared = 0.0;
    Real fDistanceFromCOM;
    for (CSpace::TMapPerType::iterator it = tEpuckMap.begin(); it != tEpuckMap.end(); ++it) {
        pcEpuck = any_cast<CEPuckEntity*>(it->second);
        fDistanceFromCOM = (pcEpuck->GetEmbodiedEntity().GetOriginAnchor().Position - cCenterOfMass).SquareLength();
        if (fDistanceFromCOM > fMaxDistanceSquared) {
            fMaxDistanceSquared = fDistanceFromCOM;
        }
    }
    m_vecCurrentRunMaximumRadius.push_back(Sqrt(fMaxDistanceSquared));
}
void MaximumRadiusLogger::EndRun(CSimulator& cSimulator) {
    m_vecMaximumRadius.push_back(m_vecCurrentRunMaximumRadius);
    m_vecCurrentRunMaximumRadius.clear();
}
void MaximumRadiusLogger::LogDataToFile(std::ofstream& ofDataFile){
    for (size_t i = 0; i <  m_vecMaximumRadius.size(); i++) {
        std::stringstream ssInput;
        ssInput << "MaximumRadius";
        for (auto longestPath : m_vecMaximumRadius[i]) {
            ssInput << ',' << longestPath;
        }
        ofDataFile << ssInput.str() << std::endl; 
    }
}

/********************************************************************************/
/********************************** AverageNND **********************************/
/********************************************************************************/

void AverageNNDLogger::BeforeTheExperiment(CSimulator& cSimulator) {}
void AverageNNDLogger::CollectData(CSimulator& cSimulator) {
    CEPuckEntity* pcEpuck;
    CEPuckEntity* pcComparedEpuck;
    CSpace::TMapPerType& tEpuckMap = cSimulator.GetSpace().GetEntitiesByType("epuck");
    Real fNNDSum = 0.0;
    // for each robot, finds its nearest neighbour
    for (CSpace::TMapPerType::iterator it = tEpuckMap.begin(); it != tEpuckMap.end(); ++it) {
        pcEpuck = any_cast<CEPuckEntity*>(it->second);
        CVector3 cEpuckPosition = pcEpuck->GetEmbodiedEntity().GetOriginAnchor().Position;
        CVector3 cComparedEpuckPosition;
        Real fMinDistanceSquared = std::numeric_limits<Real>::max();
        Real fDistanceFromNeighbour;
        for (CSpace::TMapPerType::iterator it2 = tEpuckMap.begin(); it2 != tEpuckMap.end(); ++it2) {
            pcComparedEpuck = any_cast<CEPuckEntity*>(it2->second);
            if (pcComparedEpuck->GetId() == pcEpuck->GetId()) {
                continue;
            }
            cComparedEpuckPosition = pcComparedEpuck->GetEmbodiedEntity().GetOriginAnchor().Position;
            fDistanceFromNeighbour = (cEpuckPosition - cComparedEpuckPosition).SquareLength();
            if (fDistanceFromNeighbour < fMinDistanceSquared) {
                fMinDistanceSquared = fDistanceFromNeighbour; 
            }
        }
        fNNDSum += Sqrt(fMinDistanceSquared);
    }
    m_vecCurrentRunAverageNND.push_back(fNNDSum/tEpuckMap.size());
}
void AverageNNDLogger::EndRun(CSimulator& cSimulator) {
    m_vecAverageNND.push_back(m_vecCurrentRunAverageNND);
    m_vecCurrentRunAverageNND.clear();
}
void AverageNNDLogger::LogDataToFile(std::ofstream& ofDataFile) {
    for (size_t i = 0; i <  m_vecAverageNND.size(); i++) {
        std::stringstream ssInput;
        ssInput << "AverageNND";
        for (auto longestPath : m_vecAverageNND[i]) {
            ssInput << ',' << longestPath;
        }
        ofDataFile << ssInput.str() << std::endl; 
    }
}
