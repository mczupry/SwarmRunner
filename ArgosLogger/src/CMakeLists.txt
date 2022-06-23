# Set up ARGoS compilation information
include_directories(${CMAKE_SOURCE_DIR} ${ARGOS_INCLUDE_DIRS})
link_directories(${ARGOS_LIBRARY_DIRS})

# Headers
set(LOGGER_HEADERS
	utility/DataCollector.h
	utility/loggers/DataLogger.h
	utility/loggers/BasicLoggers.h
	utility/loggers/SwarmMetricsLoggers.h
	utility/loggers/DataLoggerFactory.h)

# Sources
set(LOGGER_SOURCES
	utility/DataCollector.cpp
	utility/loggers/BasicLoggers.cpp
	utility/loggers/SwarmMetricsLoggers.cpp
	utility/loggers/DataLoggerFactory.cpp)


add_library(logger SHARED ${LOGGER_HEADERS} ${LOGGER_SOURCES})
target_link_libraries(logger argos3plugin_${ARGOS_BUILD_FOR}_epuck)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/bin)
add_executable(argos_logger ArgosLoggerMain.cpp)
target_link_libraries(argos_logger logger argos3core_${ARGOS_BUILD_FOR} argos3plugin_${ARGOS_BUILD_FOR}_epuck argos3_demiurge_loop_functions argos3_demiurge_epuck_dao)

