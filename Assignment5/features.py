import transition

def extract1(stack, queue, state, feature_names, sentence):
    extractions = {}
    extractions['stack0_pos'] = extractions['stack0_word'] = 'nil'
    extractions['queue0_pos'] = extractions['queue0_word'] = 'nil'

    if stack:
        extractions['stack0_pos'] = stack[0]['postag']
        extractions['stack0_word'] = stack[0]['form']

    if queue:
        extractions['queue0_pos'] = queue[0]['postag']
        extractions['queue0_word'] = queue[0]['form']

    extractions['canReduce'] = transition.can_reduce(stack, state)
    extractions['canLeftArc'] = transition.can_leftarc(stack, state)

    return extractions

def extract2(stack, queue, state, feature_names, sentence):
    extractions = {}
    extractions['stack0_pos'] = extractions['stack0_word'] = 'nil'
    extractions['stack1_pos'] = extractions['stack1_word'] = 'nil'
    extractions['queue0_pos'] = extractions['queue0_word'] = 'nil'
    extractions['queue1_pos'] = extractions['queue1_word'] = 'nil'

    if stack:
        extractions['stack0_pos'] = stack[0]['postag']
        extractions['stack0_word'] = stack[0]['form']
        if len(stack) > 1:
            extractions['stack1_pos'] = stack[1]['postag']
            extractions['stack1_word'] = stack[1]['form']
    if queue:
        extractions['queue0_pos'] = queue[0]['postag']
        extractions['queue0_word'] = queue[0]['form']
        if len(queue) > 1:
            extractions['queue1_pos'] = queue[1]['postag']
            extractions['queue1_word'] = queue[1]['form']

    extractions['canReduce'] = transition.can_reduce(stack, state)
    extractions['canLeftArc'] = transition.can_leftarc(stack, state)

    return extractions

def extract3(stack, queue, state, feature_names, sentence):
    extractions = {}
    extractions['stack0_pos'] = extractions['stack0_word'] = 'nil'
    extractions['stack1_pos'] = extractions['stack1_word'] = 'nil'
    extractions['stack2_pos'] = extractions['stack2_word'] = 'nil'
    extractions['queue0_pos'] = extractions['queue0_word'] = 'nil'
    extractions['queue1_pos'] = extractions['queue1_word'] = 'nil'
    extractions['queue2_pos'] = extractions['queue2_word'] = 'nil'

    if stack:
        extractions['stack0_pos'] = stack[0]['postag']
        extractions['stack0_word'] = stack[0]['form']
        if len(stack) > 1:
            extractions['stack1_pos'] = stack[1]['postag']
            extractions['stack1_word'] = stack[1]['form']
            if len(stack) > 2:
                extractions['stack2_pos'] = stack[2]['postag']
                extractions['stack2_word'] = stack[2]['form']
    if queue:
        extractions['queue0_pos'] = queue[0]['postag']
        extractions['queue0_word'] = queue[0]['form']
        if len(queue) > 1:
            extractions['queue1_pos'] = queue[1]['postag']
            extractions['queue1_word'] = queue[1]['form']
            if len(queue) > 2:
                extractions['queue2_pos'] = queue[2]['postag']
                extractions['queue2_word'] = queue[2]['form']

    extractions['canReduce'] = transition.can_reduce(stack, state)
    extractions['canLeftArc'] = transition.can_leftarc(stack, state)

    return extractions