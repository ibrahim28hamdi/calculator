import streamlit as st
import math
import re

st.set_page_config(
    page_title="Python Calculator",
    page_icon="🧮",
    layout="centered"
)

# -------------------------
# Session state
# -------------------------
if "expression" not in st.session_state:
    st.session_state.expression = ""

if "result" not in st.session_state:
    st.session_state.result = ""

# -------------------------
# Safe calculator function
# -------------------------
def safe_calculate(expression: str):
    """
    Evaluate only calculator-style mathematical expressions.
    Supports:
    + - * / % ** ( )
    decimal numbers
    sqrt, sin, cos, tan, log
    """
    if not expression.strip():
        return ""

    # Replace display symbols with Python operators
    expr = (
        expression
        .replace("×", "*")
        .replace("÷", "/")
        .replace("^", "**")
        .replace("π", "pi")
    )

    # Only allow expected characters/words
    allowed_pattern = r"^[0-9+\-*/().%\sA-Za-z_]*$"
    if not re.match(allowed_pattern, expr):
        raise ValueError("Invalid characters")

    allowed_names = {
        "sqrt": math.sqrt,
        "sin": lambda x: math.sin(math.radians(x)),
        "cos": lambda x: math.cos(math.radians(x)),
        "tan": lambda x: math.tan(math.radians(x)),
        "log": math.log10,
        "ln": math.log,
        "pi": math.pi,
        "e": math.e,
        "abs": abs,
        "round": round,
    }

    return eval(expr, {"__builtins__": {}}, allowed_names)


def add_value(value):
    st.session_state.expression += value


def clear_all():
    st.session_state.expression = ""
    st.session_state.result = ""


def delete_last():
    st.session_state.expression = st.session_state.expression[:-1]


def calculate():
    try:
        answer = safe_calculate(st.session_state.expression)

        if isinstance(answer, float):
            # Avoid ugly floating-point output when possible
            answer = round(answer, 12)
            if answer.is_integer():
                answer = int(answer)

        st.session_state.result = str(answer)
    except ZeroDivisionError:
        st.session_state.result = "Cannot divide by zero"
    except Exception:
        st.session_state.result = "Error"


# -------------------------
# Styling
# -------------------------
st.markdown(
    """
    <style>
        .stApp {
            max-width: 520px;
            margin: auto;
        }

        .calculator-title {
            text-align: center;
            font-size: 38px;
            font-weight: 800;
            margin-bottom: 10px;
        }

        .calculator-box {
            background: #151515;
            padding: 20px;
            border-radius: 24px;
            margin-bottom: 18px;
            box-shadow: 0 12px 30px rgba(0,0,0,0.25);
        }

        .expression {
            color: #b8b8b8;
            font-size: 22px;
            min-height: 35px;
            text-align: right;
            word-wrap: break-word;
        }

        .result {
            color: white;
            font-size: 42px;
            font-weight: 700;
            min-height: 55px;
            text-align: right;
            word-wrap: break-word;
        }

        div.stButton > button {
            height: 62px;
            font-size: 22px;
            font-weight: 700;
            border-radius: 18px;
            width: 100%;
        }

        .small-note {
            text-align: center;
            color: #777;
            margin-top: 18px;
            font-size: 14px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------
# UI
# -------------------------
st.markdown('<div class="calculator-title">🧮 Python Calculator</div>', unsafe_allow_html=True)

expression_text = st.session_state.expression if st.session_state.expression else "0"
result_text = st.session_state.result if st.session_state.result else ""

st.markdown(
    f"""
    <div class="calculator-box">
        <div class="expression">{expression_text}</div>
        <div class="result">{result_text}</div>
    </div>
    """,
    unsafe_allow_html=True
)

# Scientific buttons
scientific_rows = [
    [("√", "sqrt("), ("sin", "sin("), ("cos", "cos("), ("tan", "tan(")],
    [("log", "log("), ("ln", "ln("), ("π", "π"), ("x²", "^2")],
]

with st.expander("Scientific buttons"):
    for row in scientific_rows:
        cols = st.columns(4)
        for col, (label, value) in zip(cols, row):
            with col:
                st.button(
                    label,
                    use_container_width=True,
                    key=f"sci_{label}",
                    on_click=add_value,
                    args=(value,)
                )

# Main calculator layout
rows = [
    [("AC", "clear"), ("⌫", "delete"), ("(", "("), (")", ")")],
    [("7", "7"), ("8", "8"), ("9", "9"), ("÷", "÷")],
    [("4", "4"), ("5", "5"), ("6", "6"), ("×", "×")],
    [("1", "1"), ("2", "2"), ("3", "3"), ("−", "-")],
    [("0", "0"), (".", "."), ("%", "%"), ("+", "+")],
]

for row in rows:
    cols = st.columns(4)

    for col, (label, value) in zip(cols, row):
        with col:
            if value == "clear":
                st.button(
                    label,
                    use_container_width=True,
                    key=f"btn_{label}",
                    on_click=clear_all
                )
            elif value == "delete":
                st.button(
                    label,
                    use_container_width=True,
                    key=f"btn_{label}",
                    on_click=delete_last
                )
            else:
                st.button(
                    label,
                    use_container_width=True,
                    key=f"btn_{label}",
                    on_click=add_value,
                    args=(value,)
                )

st.button(
    "=",
    use_container_width=True,
    type="primary",
    on_click=calculate
)

# Optional keyboard input
st.divider()

typed_expression = st.text_input(
    "Or type an expression",
    placeholder="Example: (25 + 5) * 3"
)

if st.button("Calculate typed expression", use_container_width=True):
    st.session_state.expression = typed_expression
    calculate()
    st.rerun()

st.markdown(
    """
    <div class="small-note">
        Built with Python + Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
