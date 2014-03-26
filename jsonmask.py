class util:
    @classmethod
    def isEmpty(obj):
        return not obj
    @classmethod
    def isArray(cls, obj):
        return isinstance(obj, list)
    @classmethod
    def has(obj, key):
        return key in obj

TERMINALS = {',': 1, '/': 2, '(': 3, ')': 4}

def compile(text):
    if not text:
        return None
    return parse(scan(text))

def scan(text):
    tokens = []
    name = [""]
    def maybePushName():
        if not name[0]:
            return
        tokens.append({"tag": "_n", "value": name[0]})
        name[0] = ''

    for ch in text:
        if TERMINALS.get(ch):
            maybePushName()
            tokens.append({"tag": ch})
        else:
            name[0] += ch
    maybePushName()
    return tokens

def parse(tokens):
    return _buildTree(tokens, {}, [])

def _buildTree(tokens, parent, stack):
    props = {}
    while tokens:
        token = tokens.pop(0)
        if '_n' == token["tag"]:
            token['type'] = 'object'
            token['properties'] = _buildTree(tokens, token, stack)
            # exit if in object stack
            #peek = stack[-1]
            if stack and stack[-1]['tag'] == '/':
                stack.pop()
                _addToken(token, props)
                return props
        elif token['tag'] == ',':
            return props
        elif token['tag'] == '(':
            stack.append(token)
            parent['type'] = 'array'
            continue
        elif token['tag'] == ')':
            #openTag = stack.pop(token)
            openTag = stack.pop()
            return props
        elif token['tag'] == '/':
            stack.append(token)
            continue
        _addToken(token, props)
    return props

def _addToken(token, props):
    props[token['value']] = {"type": token['type']}
    if token['properties']:
        props[token['value']]['properties'] = token['properties']

######
# filter.js
#####
def filter(obj, compiledMask):
    if util.isArray(obj):
        return _arrayProperties(obj, compiledMask)
    else:
        return _properties(obj, compiledMask)

# wrap array & mask in a temp object;
# extract results from temp at the end
def _arrayProperties(arr, mask):
    obj = _properties({"_": arr}, {"_": {
        "type": 'array',
        "properties": mask
    }})
    return obj and obj["_"]

def _properties(obj, mask):
    maskedObj = {}
    if not obj or not mask:
        return obj
    for key in mask:
        value = mask[key]
        ret = None
        if value['type'] == 'object':
            if key == '*':
                ret = _objectAll(obj, value.get('properties', None))
                for retKey in ret:
                    maskedObj[retKey] = ret[retKey]
                ret = None
            else:
                ret = _object(obj, key, value.get('properties', None))
        elif value['type'] == 'array':
            ret = _array(obj, key, value.get('properties', None))
        
        if ret is not None:
            maskedObj[key] = ret
    return maskedObj or None

def _objectAll(obj, mask):
    ret = {}
    for key in obj:
        value = _object(obj, key, mask)
        if value:
            ret[key] = value
    return ret

def _object(obj, key, mask):
    try:
        value = obj.get(key, None)
    except AttributeError: # obj is an int
        value = None
    if util.isArray(value):
        return _array(obj, key, mask)
    if mask:
        return _properties(value, mask)
    else:
        return value

def _array(obj, key, mask):
    ret = []
    arr = obj[key]
    maskedObj = None
    if not arr:
        return arr
    if not util.isArray(arr):
        return _properties(arr, mask)
    for item in arr:
        maskedObj = _properties(item, mask)
        if maskedObj:
            ret.append(maskedObj)
    return ret or None
