import json

from src.model_checker import State, Event


class function_wrapper:

    def __init__(self, code, variables):
        self.code = code
        self.variables = variables

    def __call__(self, *args, **kwargs):
        exec(self.code, {'variable': self.variables})


def type_cast(t: str, value):
    if t == "str":
        return str(value)
    elif t == "int":
        return int(value)
    elif t == "list":
        return list(t)
    elif t == "bool":
        return bool(t)
    elif t == "dict":
        return json.loads(t)


def parse_variable(variables) -> dict:
    return {
        i: type_cast(variables[i]['type'], variables[i]['default_value'])
        for i in variables
    }


def parse_state(state: dict, variables: dict) -> State:
    name = state.get("state_name", None)

    on_enter_state = state.get("on_enter_state", None)
    on_leave_state = state.get("on_leave_state", None)
    if on_enter_state:
        on_enter_state = function_wrapper(on_enter_state, variables)

    if on_leave_state:
        on_leave_state = function_wrapper(on_leave_state, variables)

    initial = state.get('is_initial', False)
    final = state.get('is_final', False)
    return State(name, on_enter_state, on_leave_state, is_initial=initial, is_final=final)


def parse_event(event: dict, variables: dict) -> Event:
    name = event.get('event_name', None)
    src = event.get('src', None)
    des = event.get('des', None)
    on_event = event.get("on_event", None)
    if on_event:
        on_event = function_wrapper(on_event, variables)

    return Event(name, src, des, on_event, variables)


def parse_validator(code: str, variable: dict):
    return function_wrapper(code, variable)
