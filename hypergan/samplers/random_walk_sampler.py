from hypergan.samplers.base_sampler import BaseSampler
import tensorflow as tf
import numpy as np

class RandomWalkSampler(BaseSampler):
    def __init__(self, gan, samples_per_row=8):
        BaseSampler.__init__(self, gan, samples_per_row)
        self.z = None
        self.y = None
        self.x = None
        self.step = 0
        self.steps = 30
        self.target = None

    def _sample(self):
        #gan = self.gan
        z_t = self.gan.encoder.sample
        inputs_t = self.gan.inputs.x

        if self.z is None:
            print("heeee0")
            self.z = self.gan.encoder.sample.eval()
            print("heeee1")
            self.target = self.gan.encoder.sample.eval()
            print("heeee2")
            self.input = self.gan.session.run(self.gan.inputs.x)
            print("heeee3")

        if self.step > self.steps:
            self.z = self.target
            self.target = self.gan.encoder.sample.eval()
            self.step = 0

        percent = float(self.step)/self.steps
        z_interp = self.z*(1.0-percent) + self.target*percent
        self.step+=1

        g=tf.get_default_graph()
        with g.as_default():
            tf.set_random_seed(1)
            return {
                'generator': self.gan.session.run(self.gan.generator.sample, feed_dict={z_t: z_interp, inputs_t: self.input})
            }

