#include "DataLoggerFactory.h"

DataLogger* DataLoggerFactory(std::string sDataToLog) {
    if (sDataToLog == "Position") {
        return new PositionLogger();
    } else if (sDataToLog == "ObjectiveFunction") {
        return new ObjectiveFunctionLogger();
    } else if (sDataToLog == "BatteryLevel") {
        return new BatteryLevelLogger();
    } else if (sDataToLog == "CenterOfMass") {
        return new CenterOfMassLogger();
    } else if (sDataToLog == "LongestPath") {
        return new LongestPathLogger();
    } else if (sDataToLog == "MaximumRadius") {
        return new MaximumRadiusLogger();
    } else if (sDataToLog == "AverageNND") {
        return new AverageNNDLogger();
    }

    LOGERR << "[WARNING] Unrecognized metric : " << sDataToLog << std::endl;
    return NULL;
}