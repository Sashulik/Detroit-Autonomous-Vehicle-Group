import numpy as np

class Prediction:

    @staticmethod
    def softmax(x):
        '''Compute softmax values for each value in x.'''
        return np.exp(x) / np.sum(np.exp(x), axis=0)

    @classmethod
    def find_weighted_averages(cls, data, window=2):
        ''' Given an array of arrays, calculates the averages along the 0 axis for
            for the past few elements (default 2) weighted by a softmax function,
            with the heaviest weights at the end of the window.
            'window' must be an integer between 1 and the length of the enclosing array.
            Returns a numpy array.
        '''
        result = []
        weights = cls.softmax(np.array(list(range(window))))

        for i in range(len(data)):

            if (i >= window-1):
                # Use the full window previously defined if possible
                avg = np.average(data[i-(window-1):i+1], axis=0, weights=weights)
            else:
                # Otherwise, too close to an edge so recalculate weights for smaller window
                alt_weights = cls.softmax(np.array(list(range(i+1))))
                avg = np.average(data[0:i+1], axis=0, weights=alt_weights)

            result.append(avg)

        return result

    @classmethod
    def predict_next_values(cls, data, window=2):
        ''' Predict the next set of numbers by applying the last weighted avg of the diffs to the last data set '''

        # If empty array, just return it
        if (len(data) == 0):
            return data

        # If there's only one element, return that element as the prediction
        if (len(data) == 1):
            return data[0]

        # Otherwise perform the weighted average of the diffs
        diffs = np.diff(data, axis=0)
        wavgs = cls.find_weighted_averages(diffs, window=window)
        return np.add(wavgs[-1], data[-1])
