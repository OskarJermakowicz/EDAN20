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

def parse_ml(stack, queue, state, trans):
    ## Right Arc ##
    if stack and trans[:2] == 'ra':
        stack, queue, state = transition.right_arc(stack, queue, state, trans[3:])
        return stack, queue, state, 'ra'
    ## Left Arc ##
    ## Reduce ##
    ## Shift ##
    return stack, queue, state, trans

if __name__ == '__main__':
    start_time = time.time()

    train_file = 'swedish_talbanken05_train.conll'
    test_file = 'swedish_talbanken05_test_blind.conll'
    column_names_2006 = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats', 'head', 'deprel', 'phead', 'pdeprel']
    column_names_2006_test = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats']

    sentences = conll.read_sentences(train_file)
    formatted_corpus = conll.split_rows(sentences, column_names_2006)

    # Read files, extract sentences from each file then go through each sentence in each model?
    model_6param = ''
    model_10param = ''
    model_14param = ''

    trans_vector = []
    for sentence in formatted_corpus:
       
        while queue:
            features.extract()
            trans_nr = classifier.predict()
            stack, queue, state, trans = parse_ml(stack, queue, state, trans)

    print("\n--- Execution time: %s seconds ---" % (time.time() - start_time))
