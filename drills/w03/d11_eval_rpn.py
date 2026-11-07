"""d11 Evaluate reverse Polish notation with + - * / (division truncates toward zero).
eval_rpn(["2","1","+","3","*"]) == 9"""


def eval_rpn(tokens: list) -> int:
    st = []
    for tok in tokens:
        if tok in "+-*/" and len(tok) == 1:
            b, a = st.pop(), st.pop()
            if tok == "+":
                st.append(a + b)
            elif tok == "-":
                st.append(a - b)
            elif tok == "*":
                st.append(a * b)
            else:
                st.append(int(a / b))
        else:
            st.append(int(tok))
    return st[0]
