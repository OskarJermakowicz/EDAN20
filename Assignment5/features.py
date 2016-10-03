import transition

def extract_1(stack, queue, state, feature_names, sentence):
    stack0_pos = stack0_word = 'nil'
    queue0_pos = queue0_word = 'nil'

    if (stack):
        stack0_pos = stack[0]['postag']
        stack0_word = stack[0]['form']

    if (queue):
        queue0_pos = queue[0]['postag']
        queue0_word = queue[0]['form']

    return [stack0_pos, stack0_word, queue0_pos, queue0_word, transition.can_reduce(stack, state), transition.can_leftarc(stack, state)]

def extract_2(stack, queue, state, feature_names, sentence):
    stack0_pos = stack0_word = stack1_pos = stack1_word = 'nil'
    queue0_pos = queue0_word = queue1_pos = queue1_word = 'nil'

    if (stack):
        stack0_pos = stack[0]['postag']
        stack0_word = stack[0]['form']
        if (len(stack) > 1):
            stack1_pos = stack[1]['postag']
            stack1_word = stack[1]['form']

    if (queue):
        queue0_pos = queue[0]['postag']
        queue0_word = queue[0]['form']
        if (len(queue) > 1):
            queue1_pos = queue[1]['postag']
            queue1_word = queue[1]['form']

    return [stack0_pos, stack1_pos, stack0_word, stack1_word, queue0_pos, queue1_pos, queue0_word, queue1_word, transition.can_reduce(stack, state), transition.can_leftarc(stack, state)]

def extract_3(stack, queue, state, feature_names, sentence):
    stack0_pos = stack0_word = stack1_pos = stack1_word = stack2_pos = stack2_word = 'nil'
    queue0_pos = queue0_word = queue1_pos = queue1_word = queue2_pos = queue2_word = 'nil'

    if (stack):
        stack0_pos = stack[0]['postag']
        stack0_word = stack[0]['form']
        if (len(stack) > 1):
            stack1_pos = stack[1]['postag']
            stack1_word = stack[1]['form']
            if (len(stack) > 2):
                stack2_pos = stack[2]['postag']
                stack2_word = stack[2]['form']

    if (queue):
        queue0_pos = queue[0]['postag']
        queue0_word = queue[0]['form']
        if (len(queue) > 1):
            queue1_pos = queue[1]['postag']
            queue1_word = queue[1]['form']
            if (len(queue) > 2):
                queue2_pos = queue[2]['postag']
                queue2_word = queue[2]['form']

    return [stack0_pos, stack1_pos, stack2_pos, stack0_word, stack1_word, stack2_word, queue0_pos, queue1_pos, queue2_pos, queue0_word, queue1_word, queue2_word, transition.can_reduce(stack, state), transition.can_leftarc(stack, state)]