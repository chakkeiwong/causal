"""
Implementation of DiscreteFator.

API inspired by pgmpy (https://github.com/pgmpy)
"""
import copy
import math

import numpy as np
import sympy as sp


class BaseDiscreteFactor:
    """
    The `inplace=False` argument is to maintain API compatibility with
    `pgmpy.factors.discrete.DiscreteFactor`.

    """

    def __init__(self, variables, cardinality, values):
        pass

    def get_cards_dict(self):
        return {k: v for k, v in zip(self.variables, self.cardinality)}

    def marginalize(self, other, inplace=False):
        raise NotImplementedError

    def product(self, other, inplace=False):
        raise NotImplementedError

    def reduce(self, values, inplace=False):
        raise NotImplementedError

    def divide(self, other, inplace=False):
        raise NotImplementedError


class SymDiscreteFactor(BaseDiscreteFactor):
    def __init__(self, variables, cardinality, values):
        """
        Initializes a symbolic `DiscreteFactor`, which is backed by sympy arrays.



        :param variables: Scope of the factor
        :type variables: list
        :param cardinality: Cardinality of each variable of the factor, in order supplied by
        `variables`
        :type cardinality: list
        :param values: A sympy.Array of variables representing the factor, or sympy.One
        :type values: sympy.Array, int

        """
        self.variables = list(variables)
        self.cardinality = cardinality
        if hasattr(values, "reshape"):
            self.values = values.reshape(*tuple(self.cardinality))
        else:
            self.values = values

    def marginalize(self, variables, inplace=False):
        if not variables:
            return copy.deepcopy(self)

        var_indexes = [self.variables.index(var) for var in variables]
        index_to_keep = sorted(
            set(range(len(self.variables))) - set(var_indexes)
        )

        new_values = sp.tensorcontraction(self.values, tuple(var_indexes))

        return SymDiscreteFactor(
            variables=[self.variables[i] for i in index_to_keep],
            cardinality=[self.cardinality[i] for i in index_to_keep],
            values=new_values,
        )

    def product(self, other, inplace=False):
        common_vars = sorted(set(self.variables) & set(other.variables))
        result = sp.tensorproduct(self.values, other.values)
        named_indexes = list(self.variables) + list(other.variables)
        if common_vars:
            for c in common_vars:
                active_indices = [
                    i for i, x in enumerate(named_indexes) if x == c
                ]
                result = sp.tensordiagonal(result, active_indices)
                named_indexes = [i for i in named_indexes if i != c] + [c]
        cards = dict(
            zip(
                self.variables + other.variables,
                self.cardinality + other.cardinality,
            )
        )
        final_cardinality = [cards[x] for x in named_indexes]

        return SymDiscreteFactor(
            variables=named_indexes,
            cardinality=final_cardinality,
            values=result.reshape(math.prod(final_cardinality)),
        )

    def reduce(self, evidence, inplace=False):
        slice_ = [slice(None)] * len(self.variables)
        var_index_to_del = list()
        for v, s in evidence:
            var_index = self.variables.index(v)
            slice_[var_index] = s
            var_index_to_del.append(var_index)
        var_index_to_keep = sorted(
            set(range(len(self.variables))) - set(var_index_to_del)
        )
        new_variables = [self.variables[i] for i in var_index_to_keep]
        new_cardinality = [self.cardinality[i] for i in var_index_to_keep]
        new_values = self.values[tuple(slice_)]

        return SymDiscreteFactor(
            variables=new_variables,
            cardinality=new_cardinality,
            values=new_values,
        )

    def divide(self, other, inplace=False):
        inverted_other = SymDiscreteFactor(
            variables=other.variables,
            cardinality=other.cardinality,
            values=sp.Array(1 / np.array(other.values)),
        )

        return self.product(inverted_other)

    def get_value(self, **kwargs):
        assert set(kwargs.keys()) == set(
            self.variables
        ), "Factor variables do not match specified variables"

        ix = [kwargs[var] for var in self.variables]
        return self.values[tuple(ix)]

    def __eq__(self, other):
        if not (
            isinstance(self, SymDiscreteFactor)
            and isinstance(other, SymDiscreteFactor)
        ):
            return False
        elif set(self.variables) != set(other.variables):
            return False
        else:
            if self.variables != other.variables:

                other_indexes = [
                    other.variables.index(var) for var in self.variables
                ]
                other_values = sp.permutedims(other.values, other_indexes)
                phi = SymDiscreteFactor(
                    variables=[other.variables[i] for i in other_indexes],
                    cardinality=[other.cardinality[i] for i in other_indexes],
                    values=other_values,
                )
            else:
                phi = copy.deepcopy(other)
            if hasattr(self.values, "shape") and hasattr(phi.values, "shape"):
                if self.values.shape != phi.values.shape:
                    return False
            else:
                if self.values != phi.values:
                    return False

            if self.cardinality != phi.cardinality:
                return False

            return True

    def subs(self, vals):
        new_values = self.values.subs(vals)
        return SymDiscreteFactor(
            variables=self.variables,
            cardinality=self.cardinality,
            values=new_values,
        )

    def to_pgmpy(self):
        import pgmpy

        try:
            factor = pgmpy.factors.discrete.DiscreteFactor(
                variables=self.variables,
                cardinality=self.cardinality,
                values=np.array(self.values).astype(float64),
            )
        except TypeError:
            raise ValueError(
                "There are unsubstituted Sympy variables - cannot convert to pgmpy"
            )
        return factor


class SymCPD(SymDiscreteFactor):
    def __init__(
        self,
        variable: str,
        variable_card: int,
        values: sp.Array,
        evidence=None,
        evidence_card=None,
    ):

        variables = [variable]
        cardinality = [variable_card]
        if evidence is not None:
            variables.extend(evidence)
            cardinality.extend(evidence_card)
        self.variable = variable
        self.variable_card = variable_card
        super().__init__(variables, cardinality, values)

    def get_values(self):
        if len(self.variables) > 1:
            return self.values.reshape(
                self.variable_card, math.prod(self.cardinality[1:])
            )
        else:
            return self.values.reshape(self.variable_card, 1)

    def to_factor(self):
        return SymDiscreteFactor(
            self.variables.copy(),
            self.cardinality.copy(),
            copy.deepcopy(self.values),
        )

    def to_pgmpy(self):
        from pgmpy.factors.discrete import TabularCPD

        values = self.get_values()

        np_values = np.array(values.tolist()).astype(float)

        try:
            if len(self.variables) == 1:
                factor = TabularCPD(
                    variable=self.variables[0],
                    variable_card=self.cardinality[0],
                    values=np_values,
                )
            else:
                factor = TabularCPD(
                    variable=self.variables[0],
                    variable_card=self.cardinality[0],
                    values=np_values,
                    evidence=self.variables[1:],
                    evidence_card=self.cardinality[1:],
                )
        except TypeError as e:
            raise ValueError(
                f"There are unsubstituted Sympy variables - cannot convert to pgmpy: {self.values}, {e}"
            )
        return factor
