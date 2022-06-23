#SwarmRunner 
===

The SwarmRunner package is a tool that aims at facilitating the testing of optimisation algorithms for swarm robots' controllers. It uses the ARGoS3 simulator and the E-puck robots. The supported optimisation algorithms are AutoMoDe-chocolate and ARGoS3-NEAT. 
Moreover, the tool lets the user collect metrics for the optimised controllers.
It contains an example of utilisation in Experiment.py. Also, visualisation examples are given in the visualisation_examples directory.

##Installation 
===
###Dependencies
- [ARGoS3](https://github.com/ilpincy/argos3)
- [argos3-epuck](https://github.com/demiurge-project/argos3-epuck)
- [experiments-loop-functions](https://github.com/demiurge-project/experiments-loop-functions) 
- [demiurge-epuck-dao](https://github.com/demiurge-project/demiurge-epuck-dao)

- [AutoMoDe-chocolate](https://github.com/demiurge-project/ARGoS3-AutoMoDe)
- [ARGoS3-NEAT](https://github.com/demiurge-project/ARGoS3-NEAT)

- Python >= 3.6

and for the visualisations the following packages are needed : matplotlib, numpy and scipy

###Compiling ArgosLogger: 
    $ cd ArgosLogger
    $ mkdir build
    $ cd build
    $ cmake ..
    $ make