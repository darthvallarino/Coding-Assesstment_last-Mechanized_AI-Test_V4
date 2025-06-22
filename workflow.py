from flow import *
from tools import *
from graph import *

if __name__ == "__main__":
    events = graph.stream(
        {"messages": [("user", "How should we handle the climate crisis?")]},
        stream_mode="values",
    )
    for i, step in enumerate(events):
        print(f"Step {i}")
        step["messages"][-1].pretty_print()