# -*- coding: utf-8 -*-
"""
Bertsimas–Sim (BS) budget uncertainty robust counterpart builder.

This module contains a minimal, auditable implementation of the robust
counterpart for linear constraints under the BS budget set. It is
intended for appendix reproducibility: the code focuses on clarity and
traceability rather than performance or solver-specific features.

Modeling summary
----------------
For a nominal linear constraint a0·x <= b with uncertain coefficients in
index set J, the BS budget model bounds the total deviation via a budget
parameter Gamma >= 0. The robust counterpart becomes

    a0·x + sum_{j in J} d_j s_j + Gamma * theta <= b,
    0 <= s_j <= theta  for all j in J,

where theta and {s_j} are additional variables. This is the template we
instantiate below for each constraint to be robustified.

Reproducibility notes
---------------------
- Keep a consistent naming scheme for added variables/constraints.
- Record counts of new variables and inequalities to build an audit log.
- When scanning multiple Gamma values on a grid, reuse the nominal model
  and rebuild only the robust parts.
"""
from typing import Dict, Any


def robustify_constraint(
    model: Any,
    a0: Dict[Any, float],
    d: Dict[Any, float],
    x: Dict[Any, Any],
    b: float,
    Gamma: float,
    name: str = "rc",
):
    """Build BS robust counterpart.

    Template:
        a0·x + sum_j d_j s_j + Gamma * theta <= b,
        0 <= s_j <= theta.

    Parameters
    ----------
    model : Any
        Abstract MIP model exposing add_var(), add_constr().
    a0 : Dict[Any, float]
        Nominal coefficients for the left-hand side.
    d : Dict[Any, float]
        Deviation magnitudes for indices j in J.
    x : Dict[Any, Any]
        Decision variables indexed compatibly with a0.
    b : float
        Right-hand side.
    Gamma : float
        BS budget parameter >= 0.
    name : str
        Name prefix for created entities.

    Returns
    -------
    theta : Any
        The budget scaling variable.
    s : Dict[Any, Any]
        Selection variables for each j in J.
    """
    theta = model.add_var(name=f"{name}_theta", lb=0)
    s = {j: model.add_var(name=f"{name}_s_{j}", lb=0) for j in d}
    lhs = sum(a0.get(j, 0.0) * x[j] for j in x) \
          + sum(d[j] * s[j] for j in d) \
          + Gamma * theta
    model.add_constr(lhs <= b, name=f"{name}_main")
    for j in d:
        model.add_constr(s[j] <= theta, name=f"{name}_ub_{j}")
    return theta, s


def robustify_constraints_bulk(
    model: Any,
    specs: Dict[str, Dict[str, Dict[Any, float]]],
    vars_by_name: Dict[str, Dict[Any, Any]],
    rhs: Dict[str, float],
    Gamma: float,
) -> Dict[str, int]:
    """Robustify multiple nominal constraints specified by name.

    This helper loops over a set of constraint specs and applies the BS
    robust counterpart template to each, returning aggregate counts that
    are handy for scalability and audit reporting.

    Parameters
    ----------
    model : Any
        Abstract MIP model.
    specs : Dict[str, Dict[str, Dict[Any, float]]]
        Mapping constraint name -> {"a0": {...}, "d": {...}}.
    vars_by_name : Dict[str, Dict[Any, Any]]
        Mapping constraint name -> variable dict x for that constraint.
    rhs : Dict[str, float]
        Mapping constraint name -> right-hand side b.
    Gamma : float
        BS budget parameter.

    Returns
    -------
    Dict[str, int]
        {"constraints": added_inequalities, "variables": added_variables}.
    """
    added_vars = 0
    added_cons = 0
    for cname, data in specs.items():
        a0 = data.get("a0", {})
        d = data.get("d", {})
        x = vars_by_name[cname]
        b = rhs[cname]
        theta, s = robustify_constraint(
            model, a0=a0, d=d, x=x, b=b, Gamma=Gamma, name=f"rc_{cname}"
        )
        # Tally variables: 1 for theta + |J| for s_j
        added_vars += 1 + len(d)
        # Tally inequalities: 1 main + |J| upper bounds
        added_cons += 1 + len(d)
    return {"constraints": added_cons, "variables": added_vars}
