

def calc_probability_attr_to_class(db_table, class_name, class_count, c_data, sum_data):
    probability = 1
    sum_attributes = db_table.calc_sum_attributes(c_data, class_name)
    for sum_attribute in sum_attributes:
        probability *= (sum_attribute / class_count)
    return probability * (class_count / sum_data)


def classify(db_table, c_data):
    sum_data = db_table.calc_sum_data()
    sum_class = db_table.calc_sum_class()

    result_class = None
    max_probabty = None

    for class_name, class_count in sum_class.items():
        probability = calc_probability_attr_to_class(db_table, class_name, class_count, c_data, sum_data)

        if not max_probabty or probability > max_probabty:
            result_class = class_name
            max_probabty = probability

    return result_class
