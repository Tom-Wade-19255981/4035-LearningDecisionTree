#Learning Decision Tree

import math
import time

class Node:
    def __init__(self, datapoints):
        self.question = -1 #Attribute to test NEXT, won't know at time of initialisation
        self.questions_asked = []
        self.children = {} #Each child will use their answer as their key
        self.leaf = False

        self.remaining_datapoints = datapoints

    def create_child(self, answer, datapoints):
        self.children[answer] = Node(datapoints)

    def grow_leaf(self):
        """
        A method which recursively splits the dataset of the given node into a branches using the classes of the datapoints.

        :return: Returns the number of leaves created from this "branch"
        :rtype: int
        """

        number_leaves = 0
        initial_entropy = calc_entropy(self.remaining_datapoints)
        highest_information_gain = -1 #calc_entropy ALWAYS returns a +ve number so any question will give a higher information gain than this
        best_outputs, best_question = None, None


        for question in range (0,6):
            if question not in self.questions_asked:
                information_gain, outputs = calc_information_gain(self.remaining_datapoints, question, initial_entropy)

                if information_gain > highest_information_gain:
                    highest_information_gain = information_gain
                    best_outputs = outputs
                    best_question = question

        self.question = best_question

        #For loop will never be run in a leaf as "best_outputs" will be empty
        for branch in best_outputs: #Format for best_outputs: {"answer":[datapoints]}
            self.create_child(branch, best_outputs[branch])

            check_value,solved = None,True
            for datapoint in best_outputs[branch]: #check if all outputs are equal
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

    def display_children(self, depth=0):
        """
        Traverses the tree and outputs the branches and leaves of the tree
        :param depth: Automatically set to 0, does not need changing.
        :return:
        """
        if not self.leaf: #Higher the depth, further to the right.
            print (" "*depth + "Attribute: ",self.question) #The attribute being tested

            for branch in self.children:
                print (" "*(depth+1) + "Branch: ",branch) #Result of the question
                #print(" "*(depth+1) +"Distribution: ", calc_distribution(self.remaining_datapoints)) #Used for testing the tree
                self.children[branch].display_children(depth+2)
        else:
            print (" "*depth, self.result)

    def find_outcome(self, data_point):
        """
        Traverses the data set using the provided data point to find the output.
        :param data_point: An array of 6 attributes. Assumed to contain valid attributes.
        :type data_point: list
        :return: The output for the data point.
        :rtype: string
        """

        if not self.leaf:
            return self.children[data_point[self.question]].find_outcome(data_point)
        else:
            return self.result


def read_data():
    """
    Retrieves data from the .data file
    NOTE: ensure the file address is correct it is hard coded.
    :return: The array of all data points, stored as arrays
    :rtype list:
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
    start_time = time.time()
    leaves = root_node.grow_leaf()
    time_taken = (time.time() - start_time) * 1000
    print (f"Number of leaves: {leaves}, grown in {time_taken} milliseconds")

    using = True
    while using:
        print ("\nPlease choose an option:")
        print ("1. Display tree")
        print ("2. Test data point")
        print ("3. Exit")
        choice = int(input("(1/2/3): "))
        if choice == 1: root_node.display_children(0)
        elif choice == 2:
            buying = input("Please enter the cost of the car: ")
            maintenance = input("Please enter the maintenance cost of the car: ")
            doors = input("Please enter the number of doors the car has: ")
            passengers = input("Please enter the number of people the car can hold: ")
            boot_size = input("Please enter the size of the boot: ")
            safety = input("Please enter the safety level of the car: ")
            outcome = root_node.find_outcome([buying, maintenance, doors, passengers, boot_size, safety])
            print ("The outcome is: ", outcome)
        else: using = False


# Functions used to test data about the tree, not used within actual use of the tree
def calc_distribution(dataset):
    distribution = {"unacc": 0, "acc": 0, "good": 0, "vgood": 0}
    total = len(dataset)

    for datapoint in dataset:
        distribution[datapoint[-1]] += 1

    for output in distribution:
        distribution[output] = round(distribution[output] / total, 3)

    return distribution

def generate_data_point():
    buying = ["vhigh", "high", "med", "low"]
    maintenance = ["vhigh", "high", "med", "low"]
    doors = ["2", "3", "4", "5more"]
    passengers = ["2", "4", "more"]
    boot_size = ["small", "med", "big"]
    safety = ["low","med","high"]

    return [
        random.choice(buying),
        random.choice(maintenance),
        random.choice(doors),random.choice(passengers),
        random.choice(boot_size),random.choice(safety)]

def test_tree():
    total_time = 0
    for i in range(0,50):
        data_point = generate_data_point()
        outcome = root_node.find_outcome(data_point)

        formatted_data_point = ""
        for attribute in data_point:
            formatted_data_point += attribute + ","
        formatted_data_point += outcome + "\n"

        exists = False
        with open("car.data","r") as test_file:
            for line in test_file:
                if formatted_data_point == line:
                    exists = True

        if exists is False: return "ERROR"
    print ("Average time to retrieve an outcome: ", total_time/50, "nanoseconds.")
    return "No errors found"