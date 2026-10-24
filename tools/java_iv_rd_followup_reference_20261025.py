#!/usr/bin/env python3
"""Authored exact witnesses; no upstream package is imported or executed."""
from fractions import Fraction as F
import json

def calculate():
    matrix=[[100*i+j for j in range(3)] for i in range(5)]
    intended=[row[1] for row in matrix]
    swapped_prefix=[matrix[1][i] for i in range(3)]
    invalid_columns=[i for i in range(5) if i>=3]
    assert intended==[1,101,201,301,401]
    assert swapped_prefix==[100,101,102] and invalid_columns==[3,4]
    coefficient=F(2);coordinate_scale=F(4)
    rescaled=coefficient/coordinate_scale
    assert rescaled==F(1,2)
    determinant=F(1)*4-F(2)*2
    assert determinant==0
    numerator=[F(2),F(4)];denominator=[F(1),F(4)]
    mean_ratio=sum(n/d for n,d in zip(numerator,denominator))/2
    ratio_mean=sum(numerator)/sum(denominator)
    assert mean_ratio==F(3,2) and ratio_mean==F(6,5)
    costs={str(n):str(F(12000,n)) for n in [400,300,200]}
    return dict(intended_column=intended,swapped_valid_prefix=swapped_prefix,
                invalid_column_indices=invalid_columns,rows=5,columns=3,
                original_coefficient=str(coefficient),rescaled_coefficient=str(rescaled),
                coordinate_scale=str(coordinate_scale),singular_determinant=str(determinant),
                mean_of_local_ratios=str(mean_ratio),ratio_of_sums=str(ratio_mean),
                hypothetical_costs_usd=costs,native_execution=False,calibration_claim=False)

if __name__=='__main__':print(json.dumps(calculate(),indent=2))
