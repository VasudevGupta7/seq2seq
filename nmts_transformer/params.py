"""
PARAMS USED FOR TRAINING TRANSFORMER

@author: vasudevgupta
"""
import tensorflow as tf
import os

os.chdir('/Users/vasudevgupta/Desktop/GitHub/seq2seq/nmts_transformer')

class params:
    pass

# scheduling learning rate as per given in paper
class LearningRate(tf.keras.optimizers.schedules.LearningRateSchedule):
    """
    SCHEDULING THE LEARNING RATE AS PER GIVEN IN PAPER
    """
    def __init__(self, dmodel, warmup_steps= 4000):
        super(LearningRate, self).__init__()
        self.dmodel= dmodel
        self.warmup_steps= warmup_steps
        
    def __call__(self, step_num):
        arg1= 1/tf.math.sqrt(tf.cast(step_num, tf.float32))
        arg2= step_num*tf.math.pow(tf.cast(self.warmup_steps, tf.float32), -1.5)
        return (1/ tf.math.sqrt(tf.cast(self.dmodel, tf.float32)))*tf.minimum(arg1, arg2)

params.warmup_steps= 4000
params.num_blocks= 4
params.dmodel= 256
params.num_heads= 4
params.depth= params.dmodel/params.num_heads
params.batch_size= 32
params.learning_rate= LearningRate(params.dmodel, params.warmup_steps)
params.optimizer= tf.keras.optimizers.Adam(params.learning_rate)
params.epochs= 20
params.k = 5 # beam width

# don't tune it now
params.eng_vocab = 5776 # got this after tokenizing dataset- english
params.ger_vocab = 8960 # got this after tokenizing dataset- german
params.dec_max_len= 17
params.en_max_len= 20
