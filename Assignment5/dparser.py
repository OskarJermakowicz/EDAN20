"""
Gold standard parser
"""
__author__ = "Pierre Nugues"

import transition, conll, features
import time, codecs
import pickle
from sklearn import metrics
from sklearn import linear_model
from sklearn.feature_extraction import DictVectorizer

def reference(stack, queue, state):
    """
    Gold standard parsing
    Produces a sequence of transitions from a manually-annotated corpus:
    sh, re, ra.deprel, la.deprel
    :param stack: The stack
    :param queue: The input list
    :param state: The set of relations already parsed
    :return: the transition and the grammatical function (deprel) in the
    form of transition.deprel
    """
    # Right arc
    if stack and stack[0]['id'] == queue[0]['head']:
        # print('ra', queue[0]['deprel'], stack[0]['cpostag'], queue[0]['cpostag'])
        deprel = '.' + queue[0]['deprel']
        stack, queue, state = transition.right_arc(stack, queue, state)
        return stack, queue, state, 'ra' + deprel
    # Left arc
    if stack and queue[0]['id'] == stack[0]['head']:
        # print('la', stack[0]['deprel'], stack[0]['cpostag'], queue[0]['cpostag'])
        deprel = '.' + stack[0]['deprel']
        stack, queue, state = transition.left_arc(stack, queue, state)
        return stack, queue, state, 'la' + deprel
    # Reduce
    if stack and transition.can_reduce(stack, state):
        for word in stack:
            if (word['id'] == queue[0]['head'] or
                        word['head'] == queue[0]['id']):
                # print('re', stack[0]['cpostag'], queue[0]['cpostag'])
                stack, queue, state = transition.reduce(stack, queue, state)
                return stack, queue, state, 're'
    # Shift
    # print('sh', [], queue[0]['cpostag'])
    stack, queue, state = transition.shift(stack, queue, state)
    return stack, queue, state, 'sh'

def encode_classes(y_symbols):
    """
    Encode the classes as numbers
    :param y_symbols:
    :return: the y vector and the lookup dictionaries
    """
    # We extract the chunk names
    classes = sorted(list(set(y_symbols)))
    """
    Results in:
    ['B-ADJP', 'B-ADVP', 'B-CONJP', 'B-INTJ', 'B-LST', 'B-NP', 'B-PP',
    'B-PRT', 'B-SBAR', 'B-UCP', 'B-VP', 'I-ADJP', 'I-ADVP', 'I-CONJP',
    'I-INTJ', 'I-NP', 'I-PP', 'I-PRT', 'I-SBAR', 'I-UCP', 'I-VP', 'O']
    """
    # We assign each name a number
    dict_classes = dict(enumerate(classes))
    """
    Results in:
    {0: 'B-ADJP', 1: 'B-ADVP', 2: 'B-CONJP', 3: 'B-INTJ', 4: 'B-LST',
    5: 'B-NP', 6: 'B-PP', 7: 'B-PRT', 8: 'B-SBAR', 9: 'B-UCP', 10: 'B-VP',
    11: 'I-ADJP', 12: 'I-ADVP', 13: 'I-CONJP', 14: 'I-INTJ',
    15: 'I-NP', 16: 'I-PP', 17: 'I-PRT', 18: 'I-SBAR',
    19: 'I-UCP', 20: 'I-VP', 21: 'O'}
    """

    # We build an inverted dictionary
    inv_dict_classes = {v: k for k, v in dict_classes.items()}
    """
    Results in:
    {'B-SBAR': 8, 'I-NP': 15, 'B-PP': 6, 'I-SBAR': 18, 'I-PP': 16, 'I-ADVP': 12,
    'I-INTJ': 14, 'I-PRT': 17, 'I-CONJP': 13, 'B-ADJP': 0, 'O': 21,
    'B-VP': 10, 'B-PRT': 7, 'B-ADVP': 1, 'B-LST': 4, 'I-UCP': 19,
    'I-VP': 20, 'B-NP': 5, 'I-ADJP': 11, 'B-CONJP': 2, 'B-INTJ': 3, 'B-UCP': 9}
    """

    # We convert y_symbols into a numerical vector
    y = [inv_dict_classes[i] for i in y_symbols]
    return y, dict_classes, inv_dict_classes

def dict_to_matrix(dict, column_names):
    mx = []
    for entry in dict:
        en = []
        for col in column_names:
            if col in entry:
                en.append(entry[col])
        mx.append(en)
    return mx

def save(file, features_matrix, trans_vector):
    with codecs.open(file, 'w', 'utf-8') as f_out:
        for index, entry in enumerate(features_matrix):
            f_out.write(str(entry) + ' ' + str(trans_vector[index]) + '\n')

if __name__ == '__main__':
    start_time = time.time()

    train_file = 'swedish_talbanken05_train.conll'
    test_file = 'swedish_talbanken05_test_blind.conll'
    column_names_2006 = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats', 'head', 'deprel', 'phead', 'pdeprel']
    column_names_2006_test = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats']

    column_names_features= ['stack0_pos', 'stack1_pos', 'stack2_pos', 'stack0_word', 'stack1_word', 'stack2_word', 'queue0_pos', 'queue1_pos', 'queue2_pos', 'queue0_word', 'queue1_word', 'queue2_word', 'canReduce', 'canLeftArc']

    sentences = conll.read_sentences(train_file)
    formatted_corpus = conll.split_rows(sentences, column_names_2006)

    features_mx1 = []
    features_mx2 = []
    features_mx3 = []
    trans_vector = []
    for sentence in formatted_corpus:
        stack = []
        queue = list(sentence)
        state = {}
        state['heads'] = {}
        state['heads']['0'] = '0'
        state['deprels'] = {}
        state['deprels']['0'] = 'ROOT'
        transitions = []

        while queue:
            features_mx1.append(features.extract1(stack, queue, state, column_names_2006, sentence))
            features_mx2.append(features.extract2(stack, queue, state, column_names_2006, sentence))
            features_mx3.append(features.extract3(stack, queue, state, column_names_2006, sentence))
            stack, queue, state, trans = reference(stack, queue, state)
            trans_vector.append(trans)
            transitions.append(trans)

        stack, state = transition.empty_stack(stack, state)

        for word in sentence:
            word['head'] = state['heads'][word['id']]


    ### Print features ###

    print("--- Features: 6 param features")
    for index, features in enumerate(dict_to_matrix(features_mx1[:9], column_names_features)):
        print(features, trans_vector[index])

    print("\n--- Features: 10 param features")
    for index, features in enumerate(dict_to_matrix(features_mx2[:9], column_names_features)):
        print(features, trans_vector[index])

    print("\n--- Features: 14 param features")
    for index, features in enumerate(dict_to_matrix(features_mx3[:9], column_names_features)):
        print(features, trans_vector[index])


    ### Generation classification reports for the three models ###

    vec = DictVectorizer(sparse=True)
    X = vec.fit_transform(features_mx1[:50000])
    y, dict_classes, inv_dict_classes = encode_classes(trans_vector[:50000])

    #classifier = linear_model.Perceptron(penalty='l2')
    classifier = linear_model.LogisticRegression(penalty='l2', dual=True, solver='liblinear')
    model = classifier.fit(X, y)

    y_test = [inv_dict_classes[i] if i in trans_vector[:50000] else 0 for i in trans_vector[:50000]]
    y_test_predicted = classifier.predict(X)
    print("Classification report for classifier %s:\n%s\n"
          % (classifier, metrics.classification_report(y_test, y_test_predicted)))


    ### Save the models to output files ###

    pickle.dump(model, open("model1.conll", "w"))

    #save('model1.conll', dict_to_matrix(features_mx1, column_names_features), trans_vector)
    #save('model2.conll', dict_to_matrix(features_mx2, column_names_features), trans_vector)
    #save('model3.conll', dict_to_matrix(features_mx3, column_names_features), trans_vector)

    print("\n--- Execution time: %s seconds ---" % (time.time() - start_time))