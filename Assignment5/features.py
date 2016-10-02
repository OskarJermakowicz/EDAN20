import transition

def extract(stack, queue, state, feature_names, sentence):
    extracted_features = []

    stack0_pos = stack0_word = stack1_pos = stack1_word = 'nil'
    queue0_pos = queue0_word = queue1_pos = queue1_word = 'nil'

    if (len(stack) > 0):
        stack0_pos = stack[0]['postag']
        stack0_word = stack[0]['form']
        if (len(stack) > 1):
            stack1_pos = stack[1]['postag']
            stack1_word = stack[1]['form']

    if (len(queue) > 0):
        queue0_pos = queue[0]['postag']
        queue0_word = queue[0]['form']
        if (len(queue) > 1):
            queue1_pos = queue[1]['postag']
            queue1_word = queue[1]['form']

    return [stack0_pos, stack0_word, stack1_pos, stack1_word, queue0_pos, queue0_word, queue1_pos, queue1_word, transition.can_reduce(stack, state), transition.can_leftarc(stack, state)]