from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Optional, Sequence, Tuple, Type, Union

import numpy as np

from dataclasses import field
from .autodiff import Context, Variable, backpropagate, central_difference
from .scalar_functions import (
    EQ,
    LT,
    Add,
    Exp,
    Inv,
    Log,
    Mul,
    Neg,
    ReLU,
    ScalarFunction,
    Sigmoid,
)

ScalarLike = Union[float, int, "Scalar"]


@dataclass
class ScalarHistory:
    """`ScalarHistory` stores the history of `Function` operations that was
    used to construct the current Variable.

    Attributes
    ----------
        last_fn : The last Function that was called.
        ctx : The context for that Function.
        inputs : The inputs that were given when `last_fn.forward` was called.

    """

    last_fn: Optional[Type[ScalarFunction]] = None
    ctx: Optional[Context] = None
    inputs: Sequence[Scalar] = ()


# ## Task 1.2 and 1.4
# Scalar Forward and Backward

_var_count = 0


@dataclass
class Scalar:
    """A reimplementation of scalar values for autodifferentiation
    tracking. Scalar Variables behave as close as possible to standard
    Python numbers while also tracking the operations that led to the
    number's creation. They can only be manipulated by
    `ScalarFunction`.
    """

    data: float
    history: Optional[ScalarHistory] = field(default_factory=ScalarHistory)
    derivative: Optional[float] = None
    name: str = field(default="")
    unique_id: int = field(default=0)

    def __post_init__(self):
        """Initialize the Scalar object after creation.

        This method sets the unique_id, name, and ensures data is a float.
        """
        global _var_count
        _var_count += 1
        object.__setattr__(self, "unique_id", _var_count)
        object.__setattr__(self, "name", str(self.unique_id))
        object.__setattr__(self, "data", float(self.data))

    def __repr__(self) -> str:
        """Return a string representation of the Scalar.

        Returns
        -------
            A string representation of the Scalar.

        """
        return f"Scalar({self.data})"

    def __mul__(self, b: ScalarLike) -> Scalar:
        """Multiply this Scalar with another Scalar or scalar-like object.

        Args:
        ----
            b: The value to multiply with.

        Returns:
        -------
            The result of the multiplication.

        """
        return Mul.apply(self, b)

    def __truediv__(self, b: ScalarLike) -> Scalar:
        """Divide this Scalar by another Scalar or scalar-like object.

        Args:
        ----
            b: The value to divide by.

        Returns:
        -------
            The result of the division.

        """
        return Mul.apply(self, Inv.apply(b))

    def __rtruediv__(self, b: ScalarLike) -> Scalar:
        """Divide a scalar-like object by this Scalar.

        Args:
        ----
            b: The value to be divided.

        Returns:
        -------
            The result of the division.

        """
        return Mul.apply(b, Inv.apply(self))

    def __bool__(self) -> bool:
        """Convert the Scalar to a boolean value.

        Returns
        -------
            The boolean representation of the Scalar's data.

        """
        return bool(self.data)

    def __radd__(self, b: ScalarLike) -> Scalar:
        """Add a scalar-like object to this Scalar (right-side addition).

        Args:
        ----
            b: The value to add.

        Returns:
        -------
            The result of the addition.

        """
        return self + b

    def __rmul__(self, b: ScalarLike) -> Scalar:
        """Multiply a scalar-like object with this Scalar (right-side multiplication).

        Args:
        ----
            b: The value to multiply with.

        Returns:
        -------
            The result of the multiplication.

        """
        return self * b
    
    # Variable elements for backprop

    def accumulate_derivative(self, x: Any) -> None:
        """Add `val` to the the derivative accumulated on this variable.
        Should only be called during autodifferentiation on leaf variables.

        Args:
        ----
            x: value to be accumulated

        """
        assert self.is_leaf(), "Only leaf variables can have derivatives."
        if self.derivative is None:
            self.__setattr__("derivative", 0.0)
        self.__setattr__("derivative", self.derivative + x)

    def is_leaf(self) -> bool:
        """Check if this variable was created by the user (no `last_fn`).

        Returns
        -------
            True if this is a leaf variable, False otherwise.

        """
        return self.history is not None and self.history.last_fn is None

    def is_constant(self) -> bool:
        """Check if this variable is a constant (has no history).

        Returns
        -------
            True if this is a constant, False otherwise.

        """
        return self.history is None
    
    @property
    def parents(self) -> Iterable[Variable]:
        """Get the parent variables of this Scalar.

        Returns
        -------
            The input variables that were used to create this Scalar.

        Raises
        ------
            AssertionError: If the Scalar has no history.

        """
        assert self.history is not None
        return self.history.inputs

    def chain_rule(self, d_output: Any) -> Iterable[Tuple[Variable, Any]]:
        """Apply the chain rule to compute gradients.

        Args:
        ----
            d_output: The gradient flowing back from the output.

        Returns:
        -------
            Pairs of (variable, gradient) for each input variable.

        Raises:
        ------
            AssertionError: If the Scalar has no history or last function.
            NotImplementedError: If the method is not implemented.

        """
        h = self.history
        assert h is not None
        assert h.last_fn is not None
        assert h.ctx is not None

        # Compute the derivative of the output with respect to each input
        derivatives = h.last_fn._backward(h.ctx, d_output)

        # Pair each derivative with its corresponding input variable
        # Filter out constants (inputs without history)
        return (
            (input_var, deriv)
            for input_var, deriv in zip(h.inputs, derivatives)
            if not input_var.is_constant()
        )

    def backward(self, d_output: Optional[float] = None) -> None:
        """Calls autodiff to fill in the derivatives for the history of this object.

        Args:
        ----
            d_output (number, opt): starting derivative to backpropagate through the model
                                   (typically left out, and assumed to be 1.0).

        """
        if d_output is None:
            d_output = 1.0
        backpropagate(self, d_output)

    # TODO: Implement for Task 1.2.
    def __add__(self, b: ScalarLike) -> Scalar:
        """Add this Scalar to another Scalar or scalar-like object.

        Args:
        ----
            b: The value to add.

        Returns:
        -------
            The result of the addition.

        """
        return Add.apply(self, b)
    
    def __lt__(self, b: ScalarLike) -> Scalar:
        """Compare if this Scalar is less than another Scalar or scalar-like object.

        Args:
        ----
            b: The value to compare with.

        Returns:
        -------
            A Scalar representing the result of the comparison.

        """
        return LT.apply(self, b)

    def __gt__(self, b: ScalarLike) -> Scalar:
        """Compare if this Scalar is greater than another Scalar or scalar-like object.

        Args:
        ----
            b: The value to compare with.

        Returns:
        -------
            A Scalar representing the result of the comparison.

        """
        return LT.apply(b, self)
    
    def __eq__(self, b: ScalarLike) -> Scalar:
        """Compare this Scalar for equality with another Scalar or scalar-like object.

        Args:
        ----
            b: The value to compare with.

        Returns:
        -------
            A Scalar representing the result of the comparison (1.0 if equal, 0.0 otherwise).

        """
        return EQ.apply(b, self)

    def __sub__(self, b: ScalarLike) -> Scalar:
        """Subtract another Scalar or scalar-like object from this Scalar.

        Args:
        ----
            b: The value to subtract.

        Returns:
        -------
            The result of the subtraction.

        """
        return Add.apply(self, -b)

    def __neg__(self) -> Scalar:
        """Negate this Scalar.

        Returns
        -------
            The negated Scalar.

        """
        return Neg.apply(self)


    def log(self) -> Scalar:
        """Compute the natural logarithm of this Scalar.

        Returns
        -------
            The result of the logarithm operation.

        """
        return Log.apply(self)

    def exp(self) -> Scalar:
        """Compute the exponential of this Scalar.

        Returns
        -------
            The result of the exponential operation.

        """
        return Exp.apply(self)

    def sigmoid(self) -> Scalar:
        """Compute the sigmoid of this Scalar.

        Returns
        -------
            The result of the sigmoid operation.

        """
        return Sigmoid.apply(self)

    def relu(self) -> Scalar:
        """Compute the ReLU (Rectified Linear Unit) of this Scalar.

        Returns
        -------
            The result of the ReLU operation.

        """
        return ReLU.apply(self)

    

    

    


# raise NotImplementedError("Need to implement for Task 1.2")


def derivative_check(f: Any, *scalars: Scalar) -> None:
    """Checks that autodiff works on a python function.
    Asserts False if derivative is incorrect.

    Args:
    ----
        f : function from n-scalars to 1-scalar.
        *scalars : n input scalar values.


    """
    out = f(*scalars)
    out.backward()

    err_msg = """
Derivative check at arguments f(%s) and received derivative f'=%f for argument %d,
but was expecting derivative f'=%f from central difference."""
    for i, x in enumerate(scalars):
        check = central_difference(f, *scalars, arg=i)
        print(str([x.data for x in scalars]), x.derivative, i, check)
        assert x.derivative is not None
        np.testing.assert_allclose(
            x.derivative,
            check.data,
            1e-2,
            1e-2,
            err_msg=err_msg
            % (str([x.data for x in scalars]), x.derivative, i, check.data),
        )
