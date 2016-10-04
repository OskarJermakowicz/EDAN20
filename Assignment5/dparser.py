"""
Gold standard parser
"""
__author__ = "Pierre Nugues"

import transition, conll, features
import time
from sklearn import metrics
from sklearn import linear_model

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

if __name__ == '__main__':
    start_time = time.time()

    train_file = 'swedish_talbanken05_train.conll'
    test_file = 'swedish_talbanken05_test_blind.conll'
    column_names_2006 = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats', 'head', 'deprel', 'phead', 'pdeprel']
    column_names_2006_test = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats']

    sentences = conll.read_sentences(train_file)
    formatted_corpus = conll.split_rows(sentences, column_names_2006)

    feature_matrix_1 = []
    feature_matrix_2 = []
    feature_matrix_3 = []
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
            feature_matrix_1.append(features.extract_1(stack, queue, state, column_names_2006, sentence))
            feature_matrix_2.append(features.extract_2(stack, queue, state, column_names_2006, sentence))
            feature_matrix_3.append(features.extract_3(stack, queue, state, column_names_2006, sentence))
            stack, queue, state, trans = reference(stack, queue, state)
            trans_vector.append(trans)
            transitions.append(trans)

        stack, state = transition.empty_stack(stack, state)

        for word in sentence:
            word['head'] = state['heads'][word['id']]


    ### Print features to see if they are correct ###

    print("--- Features: 6 param features")
    for features, transition in zip(feature_matrix_1[:9], trans_vector[:9]):
        print(features, transition)

    print("\n--- Features: 10 param features")
    for features, transition in zip(feature_matrix_2[:9], trans_vector[:9]):
        print(features, transition)

    print("\n--- Features: 14 param features")
    for features, transition in zip(feature_matrix_3[:9], trans_vector[:9]):
        print(features, transition)


    ### Generation classification reports for the three models ###

    classifier = linear_model.LogisticRegression(penalty='l2', dual=True, solver='liblinear')
    feature_m1_predicted = classifier.predict(feature_matrix_1)
    feature_m2_predicted = classifier.predict(feature_matrix_2)
    feature_m3_predicted = classifier.predict(feature_matrix_3)

    print("\n--- Classification report for classifier %s:\n%s\n"
          % (classifier, metrics.classification_report(trans_vector, feature_m1_predicted))) 

    print("\n--- Classification report for classifier %s:\n%s\n"
          % (classifier, metrics.classification_report(trans_vector, feature_m2_predicted))) 

    print("\n--- Classification report for classifier %s:\n%s\n"
          % (classifier, metrics.classification_report(trans_vector, feature_m3_predicted))) 


    ### Save the three models to files ###

    conll.save('model1.conll', zip(feature_matrix_1, trans_vector), [])
    conll.save('model2.conll', zip(feature_matrix_2, trans_vector), [])
    conll.save('model3.conll', zip(feature_matrix_3, trans_vector), [])

    print("\n--- Execution time: %s seconds ---" % (time.time() - start_time))
