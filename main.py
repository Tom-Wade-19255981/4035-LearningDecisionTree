#Learning Decision Tree

import math

class Node:
    def __init__(self, datapoints):
        self.question = -1 #Attribute to test NEXT, won't know at time of initialisation
        self.questions_asked = []
        self.children = {} #Each child will use their answer as their key
        self.leaf = False

        self.remaining_datapoints = datapoints

    def set_next_question(self, question_index):
        self.question = question_index

    def create_child(self, answer, datapoints):
        child_questions = self.questions_asked #TODO: when done check that I don't need questions_left after question to ask is known

        child_questions.append(self.question)

        self.children[answer] = Node(datapoints)

    def grow_leaf(self):
        """
        A method which recursively splits the dataset of the given node into a branches using the classes of the datapoints.

        :return: Returns the number of leaves created from this "branch"
        :rtype: int
        """

        number_leaves = 0
        initial_entropy = calc_entropy(self.remaining_datapoints)
        highest_information_gain = -1
        best_outputs, best_question = None, None

        #print (f"Questions asked: ", self.questions_asked)
        for question in range (0,6):
            if question not in self.questions_asked:
                information_gain, outputs = calc_information_gain(self.remaining_datapoints, question, initial_entropy)

                if information_gain > highest_information_gain:
                    #print ("New best question: ", question)
                    highest_information_gain = information_gain
                    best_outputs = outputs
                    best_question = question

        self.question = best_question

        for branch in best_outputs: #best_outputs = {"answer":[datapoints]}
            check_array = []
            for _ in best_outputs:
                check_array.append(_)

            self.create_child(branch, best_outputs[branch])

            check_value,solved = None,True
            for datapoint in best_outputs[branch]:
                if check_value is None:
                    check_value = datapoint[-1]
                elif check_value != datapoint[-1]:
                    solved = False


            if len(self.children[branch].questions_asked) < 6 and not solved:
                number_leaves += self.children[branch].grow_leaf()
            elif not solved:
                self.children[branch].leaf = True
                self.children[branch].result = "ambiguous"
                print ("unsolved")
                print (self.questions_asked)
                number_leaves += 1
            else: #Is a leaf not a node
                self.children[branch].leaf = True
                self.children[branch].result = check_value
                number_leaves += 1
        return number_leaves

    def display_children(self, depth):

        if not self.leaf:
            print (" "*depth + "Attribute: ", self.question)

            for branch in self.children:
                print (" "*(depth+1) + "Branch: ", branch)
                self.children[branch].display_children(depth+2)
        else:
            print (" "*depth, self.result)



def read_data():
    """
    Retrieves data from the .data file
    NOTE: ensure the file address is correct it is hard coded.
    :return:
    """

    data_set = []
    filename = "car.data"

    with open (filename, "r") as car_data:
        for data_point in car_data:
            data_arr = split_row(data_point)

            data_set.append(data_arr)


    return data_set

def split_row(row): #Formats each row of the data set
    data = row.split(",")
    data[-1] = data[-1][:-1] #Remove "\n" from class of datapoint
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

def calc_information_gain(data_set, index, initial_entropy):
    """
    Calculates the information gain given a decision.

    :param data_set: A 2D array where each data point is an array. Each data point stores its class as the final item in the list: preceding items are attributes.
    :type data_set: list
    :param index: Index of the attribute the decision tree uses for the decision.
    :type index: int
    :param initial_entropy: The initial entropy of the previous dataset
    :type initial_entropy: int
    :return: A tuple containing: information_gain (float) - Information gain of the choice, test_output (dictionary)- A dictionary where the key is the result of the choice and the value is the smaller dataset.
    :rtype: tuple
    """

    initial_length = len(data_set)

    test_outputs = {} #Holds the outputs for this question
    new_entropy = 0 #New entropy is calculated using a sum

    #Finding the outputs for the question
    for item in data_set:
        try:
            test_outputs[item[index]].append(item) #Add to the array of outputs

        except KeyError: #KeyError means output hasn't been found before
            test_outputs[item[index]] = [item] #Create an array of outputs

    #Calculate entropy of each array
    for output in test_outputs:
        probability_of_case = len(test_outputs[output])/initial_length
        entropy_of_case = calc_entropy(test_outputs[output])

        #Using the entropy equation shown on the slides in week 3
        new_entropy += probability_of_case * entropy_of_case

    #Calculate information gain
    information_gain = initial_entropy - new_entropy

    return information_gain, test_outputs


if __name__ == "__main__":
    data_set = read_data()

    root_node = Node(data_set)
    print (f"Number of leaves: {root_node.grow_leaf()}")

    print (root_node.display_children(0))
