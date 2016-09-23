#!/usr/bin/env python3

from collections import deque, namedtuple
import logging
import operator as op
import random
import re
import sys

logger = logging.getLogger()

def d(a, b):
    return sum(random.randrange(b) + 1 for _ in range(a))

Op = namedtuple("Op", "prec func")
ops = {
    "d": Op(4, d),
    "^": Op(3, op.pow), # Allow "**"?
    "*": Op(2, op.mul),
    "/": Op(2, op.truediv),
    "%": Op(2, op.mod), # Conflicts with "d%"
    "+": Op(1, op.add),
    "-": Op(1, op.sub),
    ">": Op(0, op.gt),
    ">=": Op(0, op.ge),
    "<": Op(0, op.lt),
    "<=": Op(0, op.le),
    "=": Op(0, op.eq), # Allow "=="?
    # Keep/drop requires more advanced behavior for `d` and figuring out precedence
    # "kh": Op(4, kh),
    # "kl": Op(4, kl),
    # "dh": Op(4, dh),
    # "dl": Op(4, dl),
}

def conv_to_op(s):
    try:
        return int(s)
    except:
        try:
            return float(s)
        except:
            return ops[s]

if __name__ == "__main__":
    logging.basicConfig(level = logging.DEBUG)
    expr = re.sub(r"\s+", "", sys.argv[1], flags = re.UNICODE)
    logger.debug(expr)
    expr = re.findall(r"[\d.]+|[^\d.]+", expr)
    logger.debug(expr)
    expr = deque(conv_to_op(elem) for elem in expr)
    logger.debug(expr)

    op_stack = []
    num_stack = []

    # Use shunting yard algorithm, adapted to evaluate in place instead of converting to postfix notation.
    while expr:
        curr = expr.popleft()
        if type(curr) in (int, float):
            num_stack.append(curr)
        else:
            while op_stack and op_stack[-1].prec >= curr.prec:
                b = num_stack.pop()
                a = num_stack.pop()
                num_stack.append(op_stack.pop().func(a, b))
            op_stack.append(curr)
    while op_stack:
        b = num_stack.pop()
        a = num_stack.pop()
        num_stack.append(op_stack.pop().func(a, b))
    print(num_stack[0])
