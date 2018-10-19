from matplotlib import pyplot as plt
import numpy as np
from keras import backend as K
from experiment_mnist import *
from tfshow import *
import pickle

Layers = 3
KLips = 2
NNeurons = 10
activation = 'relu'
scaler = 1.0
epochs = 500
inputs = 2000
acc_param = 5000

def get_results(pfirst = 0.5, reg_type = 'delta', reg_coeff = 1e-4, repetition = 0):
    if reg_type == 0 and reg_coeff != 0:
        return {}
    print(pfirst, reg_type, reg_coeff, repetition)
    P = [pfirst] + [0] * (Layers - 1)
    N = [NNeurons] * Layers
    
    name = 'pfirst_%s_reg_type_%s_coeff_%s_repetition_%s' % (str(pfirst), str(reg_type), str(reg_coeff), str(repetition))
    
    model = MNISTExperiment(N, P, KLips, epochs = epochs, activation = activation, reg_type = reg_type,
                            reg_coeff = reg_coeff, do_print = True, scaler = scaler, name = name)
    
    model.update_C(model.get_inputs(10000))
    
    header = ['mean_exp', 'std_exp', 'mean_bound', 'std_bound', 'output_mean', 'output_variance']
    bound = model.run(inputs = inputs, repetitions = 1000)
    
    acc = model.get_accuracy(acc_param, acc_param, tqdm_ = tqdm)
    acc_orig = model.get_accuracy(acc_param, acc_param, tqdm_ = tqdm, no_dropout = True)
    
    results = {x: y for x, y in zip(header, bound)}
    results['acc_dropout'] = acc
    results['acc_orig'] = acc_orig
    results['W'] = model.W
    results['B'] = model.B
    K.clear_session()
    return results

pfirst_options = np.linspace(0, 1, 10)
reg_type_options = ['delta', 'l1', 'l2', 0]
reg_coeff_options = [0] + np.logspace(-10, 0, 30)
repetitions = range(15)

print(pfirst_options)
print(reg_type_options)
print(reg_coeff_options)
print(repetitions)

results = {(pfirst, reg_type, reg_coeff, repetition): get_results(pfirst = pfirst, reg_type = reg_type, reg_coeff = reg_coeff, repetition = repetition)
 for repetition in repetitions
 for reg_coeff in reg_coeff_options
 for reg_type in reg_type_options
 for pfirst in pfirst_options
}

pickle.dump(results, open('results_repeat.pkl', 'wb'))