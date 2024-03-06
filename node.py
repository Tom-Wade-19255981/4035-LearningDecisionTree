import main

class Node:
    def __init__(self, question_array, datapoints):
        self.question = -1 #Attribute to test NEXT, won't know at time of initialisation
        self.questions_left = question_array #Questions that haven't been asked yet, includes the next question to be asked
        self.children = {} #Each child will use their answer as their key
        self.leaf = False

        self.remaining_datapoints = datapoints

    def set_next_question(self, question_index):
        self.question = question_index

    def create_child(self, answer, datapoints):
        child_questions = self.questions_left #TODO: when done check that I don't need questions_left after question to ask is known
        child_questions.pop(self.question)

        self.children[answer] = Node(child_questions, datapoints)

    def grow_leaf(self):
        initial_entropy = main.calc_entropy(self.remaining_datapoints)
        highest_information_gain = -1
        best_outputs, best_question = None, None

        for question in self.questions_left:
            information_gain, outputs = main.calc_information_gain(self.remaining_datapoints, question, initial_entropy)

            if information_gain > highest_information_gain:
                print ("New best question: ", question)
                highest_information_gain = information_gain
                best_outputs = outputs
                best_question = question

        self.question = best_question

        for branch in best_outputs: #best_outputs = {"answer":[datapoints]}
            self.create_child(branch, best_outputs[branch])
            self.children[branch].grow_leaf()
