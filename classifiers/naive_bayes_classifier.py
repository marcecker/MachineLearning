
class NaiveBayesClassifier:

    def __init__(self, names, dataset, class_key):
        self.names = names
        self.dataset = dataset.values
        self.class_key = class_key
        self.class_index = names.index(class_key)

    def get_class_vect(self):
        res = []
        cou = []
        for vector in self.dataset:
            current_class = vector[self.class_index]
            if current_class not in res:
                res.append(current_class)
                cou.append(1)
            else:
                cou[res.index(current_class)] += 1
        return res, cou

    def count_one_attr_of_class(self, attribute, attribute_index, class_name):
        rl_attri_matches = 0

        for vector in self.dataset:
            if vector[self.class_index] == class_name and vector[attribute_index] == attribute:
                rl_attri_matches += 1

        return rl_attri_matches

    def classify(self, attribute_vector):
        # The variables used to search the class with the highest probability
        max_class = None
        max_prob = None
        # get vector of all classes plus one that contains the nr of instances
        # representing these ones.
        class_vector, class_count = self.get_class_vect()
        # The algorithm compares the probabilities for each class and takes the
        # one with the highest
        for class_index, class_name in enumerate(class_vector):
            p = 1
            # for each column in the data set calculate the P(column|class)
            for index, name in enumerate(self.names):
                count_attr = 0
                if name == self.class_key:
                    continue
                # for each row count the how many of these attributes represent
                # the current class
                for vector in self.dataset:
                    if vector[index] == attribute_vector[index] and vector[self.class_index] == class_name:
                        count_attr += 1
                p *= (count_attr / class_count[class_index])
            # multiply with P(class)
            p *= (class_count[class_index] / len(self.dataset))
            # search maximum
            if not max_class or p > max_prob:
                max_class = class_name
                max_prob = p

        return max_class

    def benchmark(self):
        right = 0
        wrong = 0

        for c_data in self.dataset:
            res_class = self.classify(c_data)
            if res_class == c_data[self.class_index]:
                right += 1
            else:
                wrong += 1

        return (right * 100) / (right + wrong)
