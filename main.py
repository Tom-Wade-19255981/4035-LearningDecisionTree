#Learning Decision Tree

import math


def read_data(attribute_count):
    data_set = []

    with open ("car.data", "r") as car_data:
        for data_point in car_data:
            data_arr = split_row(data_point)

            data_set.append(data_arr)

            attribute_count = tally_attribute(data_arr, attribute_count)


    return data_set, attribute_count

def split_row(row): #Formats each row of the data set
    data = row.split(",")
    data[-1] = data[-1][:-1] #Remove "\n" from final attribute
    return data

def tally_attribute(data_arr, attribute_count):
    for i in range (0,6):
        attribute_count[i][data_arr[i]] += 1
    return attribute_count

def calc_entropy(data_set):
    """
    Calculates the entropy of a given data set.

    :param data_set: A 2D array where each data point is an array. Each data point stores its class as the final item in the list: preceding items are attributes.
    :type data_set: list
    :return: The entropy of the data set (always +ve)
    :rtype: int
    """

    classes = {}
    length = len(data_set)
    for item in data_set:
        try:
            classes[item[-1]] += 1
        except KeyError:
            classes[item[-1]] = 1

    for output in classes: #Obtain the probability of each output
        classes[output] = classes[output]/length

    sum = 0
    for output in classes:
        try:
            sum += classes[output] * math.log2(classes[output])
        except ValueError:
            #Can't log 0
            pass
    return -sum

def calc_information_gain(data_set, index):
    """
    Calculates the information gain given a decision.

    :param data_set: A 2D array where each data point is an array. Each data point stores its class as the final item in the list: preceding items are attributes.
    :type data_set: list
    :param index: Index of the attribute the decision tree uses for the decision.
    :return: A tuple containing: information_gain (float) - Information gain of the choice, test_output (dictionary)- A dictionary where the key is the result of the choice and the value is the smaller dataset.
    :rtype: tuple
    """


    inital_entropy = calc_entropy(data_set)
    initial_length = len(data_set)

    test_outputs = {}
    new_entropy = 0

    #Split into 3/4 arrays
    for item in data_set:
        try:
            test_outputs[item[index]].append(item) #Add to the array of outputs
        except KeyError:
            test_outputs[item[index]] = [item] #Create an array of outputs

    # testing_output_counts = []
    # for output in test_outputs:
    #     this_output = test_outputs[output]
    #
    #
    #
    #     attribute_count = {  # Might be redundant
    #         0: {"vhigh": 0, "high": 0, "med": 0, "low": 0},  # Buying price: low good high bad
    #         1: {"vhigh": 0, "high": 0, "med": 0, "low": 0},  # Maintenance: low good high bad
    #         2: {"2": 0, "3": 0, "4": 0, "5more": 0},  # Number of doors
    #         3: {"2": 0, "4": 0, "more": 0},  # Number of passengers
    #         4: {"small": 0, "med": 0, "big": 0},  # Size of boot
    #         5: {"high": 0, "med": 0, "low": 0},  # Safety
    #         6: {"vgood":0, "good":0, "acc":0, "unacc":0}
    #     }
    #
    #     for data_point in this_output:
    #
    #         for i in range(0, 7):
    #             try:
    #                 attribute_count[i][data_point[index]] += 1
    #             except KeyError:
    #                 attribute_count[i][data_point[index]] = 1
    #
    #     testing_output_counts.append(attribute_count)
    #
    # for _ in testing_output_counts:
    #     print (_)
    #     print ("\n")

    #Calculate entropy of each array
    for output in test_outputs:
        probability_of_case = len(test_outputs[output])/initial_length
        entropy_of_case = calc_entropy(test_outputs[output])

        new_entropy += probability_of_case * entropy_of_case



    #Calculate information gain
    information_gain = inital_entropy - new_entropy

    # print ("New entropy: ", new_entropy)
    # print ("IG: ", information_gain)
    #
    # for _class in test_outputs:
    #     print ("\nOutput: ")
    #     for data_point in test_outputs[_class]:
    #         print (data_point)
    #print (test_outputs)

    return information_gain, test_outputs


if __name__ == "__main__":
    attribute_count = { #Might be redundant
        0: {"vhigh":0,"high":0,"med":0,"low":0}, #Buying price: low good high bad
        1: {"vhigh": 0, "high": 0, "med": 0, "low": 0}, #Maintenance: low good high bad
        2: {"2":0,"3":0,"4":0,"5more":0}, #Number of doors
        3: {"2":0,"4":0,"more":0}, #Number of passengers
        4: {"small":0,"med":0,"big":0}, #Size of boot
        5: {"high": 0, "med": 0, "low": 0} #Safety
    }
    data_set, attribute_count = read_data(attribute_count)

    print (attribute_count)

    print ("Initial entropy: ",calc_entropy(data_set))

    information_gain, test_outputs = calc_information_gain(data_set, 5)
    print ("Information gain: ", information_gain)