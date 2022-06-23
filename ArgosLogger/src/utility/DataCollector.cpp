#include "DataCollector.h"


void DataCollector::Init(std::vector<std::string> vecMetrics, std::string strOutputFile, CSimulator& cSimulator) {
    m_strFilename = strOutputFile;

    for (auto& metric : vecMetrics) {
        DataLogger* logger = DataLoggerFactory(metric);
        
        if (logger == NULL) {
            continue;
        }
        m_vecLoggers.emplace_back(logger);
    }
}

void DataCollector::BeforeTheExperiment(CSimulator& cSimulator) {
    for (auto& logger : m_vecLoggers) {
        logger->BeforeTheExperiment(cSimulator);
    }
}

void DataCollector::CollectDataPostStep(CSimulator& cSimulator) {
    for (auto& logger : m_vecLoggers) {
        logger->CollectData(cSimulator);
    }
}

void DataCollector::EndRun(CSimulator& cSimulator) {
    for (auto& logger : m_vecLoggers) {
        logger->EndRun(cSimulator);
    }
}

void DataCollector::LogDataToFile(CSimulator& cSimulator) {
    if (m_strFilename.empty()) {
        return;
    }
    std::ofstream ofDataFile;
    ofDataFile.open(m_strFilename.c_str(), std::ofstream::out | std::ofstream::trunc);
    if(ofDataFile.fail()) {
        THROW_ARGOSEXCEPTION("Error opening file \"" << m_strFilename);
    }

    for (auto& logger : m_vecLoggers) {
        logger->LogDataToFile(ofDataFile);
    }
    ofDataFile.close();
}