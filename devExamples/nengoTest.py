#!/usr/bin/env python

#############################################################################
##
#############################################################################

import random

import matplotlib.pyplot as plt
import nengo
import numpy as np
from nengo.dists import Uniform

if __name__ == "__main__":
        model = nengo.Network(label='A Single Neuron')
        with model:
            neuron = nengo.Ensemble(1, dimensions=1,  # Represent a scalar
                                    intercepts=Uniform(-.5, -.5),  # Set intercept to 0.5
                                    max_rates=Uniform(100, 100),  # Set the maximum firing rate of the neuron to 100hz
                                    encoders=[[1]])  # Sets the neurons firing rate to increase for positive input
        with model:
            cos = nengo.Node(lambda t: np.cos(8 * t))
        with model:
            # Connect the input signal to the neuron
            nengo.Connection(cos, neuron)
        with model:
            cos_probe = nengo.Probe(cos)  # The original input
            spikes = nengo.Probe(neuron.neurons)  # The raw spikes from the neuron
            voltage = nengo.Probe(neuron.neurons, 'voltage')  # Subthreshold soma voltage of the neuron
            filtered = nengo.Probe(neuron, synapse=0.01)  # Spikes filtered by a 10ms post-synaptic filter
        with nengo.Simulator(model) as sim:  # Create the simulator
            sim.run(1)  # Run it for 1 second
            # Plot the decoded output of the ensemble
            plt.plot(sim.trange(), sim.data[filtered])
            plt.plot(sim.trange(), sim.data[cos_probe])
            plt.xlim(0, 1)

            # Plot the spiking output of the ensemble
            from nengo.utils.matplotlib import rasterplot

            plt.figure(figsize=(10, 8))
            plt.subplot(221)
            rasterplot(sim.trange(), sim.data[spikes])
            plt.ylabel("Neuron")
            plt.xlim(0, 1)

            # Plot the soma voltages of the neurons
            plt.subplot(222)
            plt.plot(sim.trange(), sim.data[voltage][:, 0], 'r')
            plt.xlim(0, 1);
            plt.show()