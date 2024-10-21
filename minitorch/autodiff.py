from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Tuple, Protocol


# ## Task 1.1
# Central Difference calculation


def central_difference(f: Any, *vals: Any, arg: int = 0, epsilon: float = 1e-6) -> Any:
    r"""Computes an approximation to the derivative of `f` with respect to one arg.

    See :doc:`derivative` or https://en.wikipedia.org/wiki/Finite_difference for more details.

    Args:
    ----
        f : arbitrary function from n-scalar args to one value
        *vals : n-float values $x_0 \ldots x_{n-1}$
        arg : the number $i$ of the arg to compute the derivative
        epsilon : a small constant

    Returns:
    -------
        An approximation of $f'_i(x_0, \ldots, x_{n-1})$

    """
    # Create a list from the input values
    vals_list = list(vals)

    # Compute f(x + epsilon)
    vals_list[arg] += epsilon
    f_plus = f(*vals_list)

    # Compute f(x - epsilon)
    vals_list[arg] -= 2 * epsilon  # Subtract 2*epsilon since we added epsilon before
    f_minus = f(*vals_list)

    # Compute the central difference
    return (f_plus - f_minus) / (2 * epsilon)


variable_count = 1


class Variable(Protocol):
    def accumulate_derivative(self, x: Any) -> None:
        """Accumulates the derivative of the variable.

        Args:
        ----
            x (Any): The value to be accumulated to the derivative.

        """
        ...

    @property
    def unique_id(self) -> int:
        """Returns a unique identifier for the variable.

        Returns
        -------
            int: A unique integer identifier.

        """
        ...

    def is_leaf(self) -> bool:
        """Checks if the variable is a leaf node in the computation graph.

        Returns
        -------
            bool: True if the variable is a leaf node, False otherwise.

        """
        ...

    def is_constant(self) -> bool:
        """Checks if the variable is a constant.

        Returns
        -------
            bool: True if the variable is a constant, False otherwise.

        """
        ...

    @property
    def parents(self) -> Iterable["Variable"]:
        """Returns the parent variables in the computation graph.

        Returns
        -------
            Iterable["Variable"]: An iterable of parent variables.

        """
        ...

    def chain_rule(self, d_output: Any) -> Iterable[Tuple[Variable, Any]]:
        """Applies the chain rule to compute gradients.

        Args:
        ----
            d_output (Any): The gradient flowing back from the output.

        Returns:
        -------
            Iterable[Tuple[Variable, Any]]: An iterable of tuples containing
            parent variables and their corresponding gradients.

        """
        ...


def topological_sort(variable: Variable) -> Iterable[Variable]:
    """Computes the topological order of the computation graph.

    Args:
    ----
        variable: The right-most variable

    Returns:
    -------
        Non-constant Variables in topological order starting from the right.

    """
    visited = set()
    top_order = []

    def dfs(var: Variable) -> None:
        if var.unique_id in visited or var.is_constant():
            return
        visited.add(var.unique_id)
        for parent in var.parents:
            dfs(parent)
        top_order.append(var)

    dfs(variable)
    return reversed(top_order)


def backpropagate(variable: Variable, deriv: Any) -> None:
    """Runs backpropagation on the computation graph in order to compute derivatives for the leave nodes.

    Args:
    ----
        variable: The right-most variable.
        deriv: The derivative of the right-most variable that we want to propagate backward to the leaves.

    Returns:
    -------
    No return. Should write to its results to the derivative values of each leaf through `accumulate_derivative`.

    """
    top_order = topological_sort(variable)

    derivatives = {variable.unique_id: deriv}
    for var in top_order:
        if var.unique_id in derivatives:
            curr_var_deriv = derivatives[var.unique_id]
            if var.is_leaf():
                var.accumulate_derivative(derivatives[var.unique_id])
            else:
                for parent, parent_deriv in var.chain_rule(curr_var_deriv):
                    if parent.unique_id not in derivatives:
                        derivatives[parent.unique_id] = parent_deriv
                    else:
                        derivatives[parent.unique_id] += parent_deriv


@dataclass
class Context:
    """Context class is used by `Function` to store information during the forward pass."""

    no_grad: bool = False
    saved_values: Tuple[Any, ...] = ()

    def save_for_backward(self, *values: Any) -> None:
        """Store the given `values` if they need to be used during backpropagation."""
        if self.no_grad:
            return
        self.saved_values = values

    @property
    def saved_tensors(self) -> Tuple[Any, ...]:
        """Returns the values stored for backward computation"""
        return self.saved_values
