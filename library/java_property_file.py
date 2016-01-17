DOCUMENTATION = '''
---
module: java_property_file 
author: U H u@h 
short_descripton:  Updates property files in java format
description:
    - Parsing logic by Kishan Thomas <kishan@hackorama.com> \
Given a route prefix, check to see if route exists. \
If the route exists, then do nothing. If route does not exist \
the module will exit with an error.
options:
    prefix:
        description:
            - route to check.
        required: true
    timeout:
        description:
            - timeout interval. if route is not found by the \
time timeout kicks in then exit module
'''

def fromStringWithChanges(data, changes):
    """Read the key, element pairs from a java properties file

    Follows the file format 'http://docs.oracle.com/javase/6/docs/api/
    java/util/Properties.html#load(java.io.Reader)' and tested against
    the Java 6 version of java.util.Properties

    Args:
       data: property file contents
       changes: dics containing key/value pair to change
    Returns:
       prop_dict: property parsed and updated
       raw_string: properyfile with updates
    Raises:
        UnicodeDecodeError: if the property file has malformed \uxxxx encoding,
            Corresponds to java IllegalArgumentException in Properties.load()
        AttributeError: if invalid object was provided for file object
            Corresponds to java NullPointerException

    Author: Kishan Thomas <kishan@hackorama.com>
    """
    LINE_BREAKS = '\n\r\f' #end-of-line, carriage-return, form-feed
    ESC_DELIM = r'\\' # '\'
    ESCAPED_ESC_DELIM = r'\\\\' # '\\'
    COMMENT_LINE = re.compile('\s*[#!].*') # starts with #|! ignore white space
    MULTI_LINE = re.compile(r'.*[\\]\s*$') # ending with '\' ignore white space
    # non escaped  =|:|' ', include surrounding non escaped white space
    SPLIT_DELIM = re.compile(r'(?<!\\)\s*(?<!\\)[=: ]\s*')
    # match escape characters '\', except escaped '\\' and unicode escape '\u'
    VALID_ESC_DELIM = r'(?<!\\)[\\](?!u)'
    DEFAULT_ELEMENT = ''

    result = dict()
    raw_string = ''
    buf = StringIO.StringIO(data)
    natural_line = buf.readline()
    while natural_line:
        # skip blank lines and comment lines, process only valid logical lines
        if natural_line.strip() and COMMENT_LINE.match(natural_line) is None:
          raw_line = natural_line 
          logical_line = natural_line.lstrip().rstrip(LINE_BREAKS)
          # remove multi line delim and append adjacent lines
          while MULTI_LINE.match(logical_line): 
            line = buf.readline()
            raw_line = raw_line + line 
            logical_line = logical_line.rstrip()[:-1] + line.lstrip().rstrip(LINE_BREAKS)

          pair = SPLIT_DELIM.split(logical_line, 1)
          if len(pair) == 1: pair.append(DEFAULT_ELEMENT)
          pair = [re.sub(VALID_ESC_DELIM, '', item) for item in pair]
          pair = [re.sub(ESCAPED_ESC_DELIM, ESC_DELIM, item) for item in pair]
          pair = [unicode(item, 'unicode_escape') for item in pair] 
          if pair[0] in changes:
            pair[1] = changes[pair[0]]
            raw_string = raw_string + pair[0] + "=" + pair[1] + '\n'
          else:
            raw_string = raw_string + raw_line
          result[pair[0]] = pair[1] # add key, element to result dict
        else:
          raw_string = raw_string + natural_line
        natural_line = buf.readline()
    return_value = collections.namedtuple('return_value', ['prop_dict', 'raw_string'])
    return return_value(result, raw_string)

def main():
    module = AnsibleModule(
        argument_spec=dict(
            dest=dict(required=True, type='str'),
            option=dict(required=True, type='str'),
            value=dict(required=True, type='str'),
        ),
    )

    # function runs a check.
    # If after timeout it will return false
    return_val = check_if_route_exists(module)
    if return_val is True:
        module.exit_json(changed=False, msg="Route Found")
    else:
        module.fail_json(msg="Route not Found. Check Routing Configuration")

import re
import collections
import StringIO


if __name__ == '__main__':
    main()
