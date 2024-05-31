################################# IMPORT PACKAGES ################################

from dash import dcc, html

################################# MAIN CODE ################################

# Display utility functions
def _merge(a, b):
    """Merge two dictionaries, with values from 'b' overwriting those from 'a' if keys overlap."""
    return dict(a, **b)

# Utility function to return a new dictionary
def _omit(omitted_keys, d):
    """Return a new dictionary with certain keys omitted."""
    return {k: v for k, v in d.items() if k not in omitted_keys}

# Custom display components
def Card(children, **kwargs):
    """
    Create a styled style with children elements.

    Parameters:
        children: A list of Dash components.
        kwargs: Additional keyword arguments.

    Returns:
        A Dash html.Section element.
    """
    
    return html.Section(
        children,
        style=_merge(
            {
                "padding": 20,
                "margin": 5,
                "borderRadius": 5,
                "border": "thin lightgrey solid",
                "background-color": "white",
                # Remove possibility to select the text for better UX
                "user-select": "none",
                "-moz-user-select": "none",
                "-webkit-user-select": "none",
                "-ms-user-select": "none",
            },
            kwargs.get("style", {}),
        ),
        **_omit(["style"], kwargs),)

# Creates a title 
def SectionTitle(title, size, align="center", color="#222"):
    return html.Div(
        style={"text-align": align, "color": color},
        children=dcc.Markdown("#" * size + " " + title),)

# Creates a named card
def NamedCard(title, size, children, **kwargs):
    size = min(size, 6)
    size = max(size, 1)
    return html.Div(
        [Card([SectionTitle(title, size, align="left")] + children, **kwargs)])

# Creates a slider
def NamedSlider(name, **kwargs):
    return html.Div(
        style={"padding": "20px 10px 25px 4px"},
        children=[
            html.P(f"{name}:"),
            html.Div(style={"marginLeft": "6px"}, children=dcc.Slider(**kwargs)),],)

# Creates a dropdown
def NamedDropdown(name, **kwargs):
    return html.Div(
        style={"margin": "10px 0px"},
        children=[
            html.P(children=f"{name}:", style={"marginLeft": "3px"}),
            dcc.Dropdown(**kwargs),],)

# Creates radio items
def NamedRadioItems(name, **kwargs):
    return html.Div(
        style={"padding": "20px 10px 25px 4px"},
        children=[html.P(children=f"{name}:"), dcc.RadioItems(**kwargs)],)

# Creates a text input field
def NamedInput(name, **kwargs):
    return html.Div(children=[html.P(children=f"{name}:"), dcc.Input(**kwargs)])

# Utility to generate options for dropdown components
def DropdownOptionsList(*args):
    return [{"label": val.capitalize(), "value": val} for val in args]