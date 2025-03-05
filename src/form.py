form1 = (
    "Logical and Arithmetic Operator Variations:\n"
    "- Modify logical and arithmetic operators (e.g., AND → OR, + → *, division → modulo).\n"
    "- Swap between equivalence and implication operators (e.g., <=> ↔ →).\n"
    "- Change operator precedence and grouping (e.g., (A AND B) → A AND (B OR C)).\n"
    "- Use bitwise operators in arithmetic expressions or mix bitwise and logical operators."
)

form2 = (
    "Data Type and Value Variations:\n"
    "- Introduce type conflicts, such as mixing integers with bit-vectors or arrays with sets.\n"
    "- Adjust numeric constants and bit-vector widths (e.g., change a 32-bit vector to a 16-bit vector or vice versa).\n"
    "- Randomize constant values in assertions (e.g., change 10 to a random integer or floating-point value).\n"
    "- Force type coercion errors by assigning mismatched types.\n"
    "- Introduce floating-point operations or irrational constants if the solver supports them."
)

form3 = (
    "Quantifier and Variable Variations:\n"
    "- Interfere with quantifier scopes (e.g., change the scope of existential or universal quantifiers).\n"
    "- Rename variables or introduce new variables of different types.\n"
    "- Add or remove variables in complex quantifier statements (e.g., introduce new bound variables).\n"
    "- Modify variable domains to conflict with the rest of the formula."
)

form4 = (
    "Function and Term Variations:\n"
    "- Swap function argument order or introduce new function definitions.\n"
    "- Replace custom functions with inline expressions or add undefined functions that could cause errors.\n"
    "- Introduce new theories or axioms via custom functions, then modify them randomly.\n"
    "- Swap built-in functions with custom or undefined ones, and test Z3’s reaction."
)

form5 = (
    "Solver Command and Meta-command Variations:\n"
    "- Disrupt command order or insert non-standard commands (e.g., randomize solver options).\n"
    "- Set conflicting solver options, such as enabling multiple conflicting theories.\n"
    "- Introduce meta-comments or unsupported options in the file to test error handling.\n"
    "- Experiment with different solver behaviors (e.g., optimization commands vs. satisfiability checks)."
)

form6 = (
    "Array and Set Operations Variations:\n"
    "- Modify array dimensions and types randomly, introducing unexpected dimensions or mixed types.\n"
    "- Perform redundant stores, and confusing operations on arrays (e.g., array indexing with expressions instead of constants).\n"
    "- Use set operations in unexpected ways (e.g., union of arrays, intersection of sets and arrays).\n"
    "- Insert inconsistent or conflicting array bounds or indices."
)

form7 = (
    "Syntax and Format Variations:\n"
    "- Introduce redundant symbols or disrupt structure with excessive comments or extra parentheses.\n"
    "- Modify spacing and line breaks to obscure the structure of the SMT2 file (e.g., space around operators, inconsistent indentations).\n"
    "- Add non-printing characters (e.g., tabs, newlines, extra spaces) randomly into the file.\n"
    "- Randomize bracket/parenthesis placements and nesting, while keeping logical consistency."
)

form8 = (
    "Theory Mixing and Conflicts:\n"
    "- Mix operations from different theories (e.g., arithmetic theory with array or bit-vector theory).\n"
    "- Introduce theory conflicts by using incompatible functions (e.g., mixing integer and real operations).\n"
    "- Force unsupported theory options, such as combining floating-point and fixed-point theories.\n"
    "- Introduce extraneous or unsupported theories to test Z3's error handling."
)

form9 = (
    "Combination and Iteration Variations:\n"
    "- Apply multiple variations sequentially, starting with minor changes and gradually increasing intensity.\n"
    "- Apply transformations in random orders and track the solver’s performance on the resulting SMT2 files.\n"
    "- Iteratively combine changes to test interactions between different modification types."
)

form10 = (
    "Theory-Specific Variations:\n"
    "- Modify theory-specific operations (e.g., modify bitwise operations under the bit-vector theory, adjust array operations in the theory of arrays).\n"
    "- Randomly switch to and from theory-specific commands to test theory-switching robustness in the solver.\n"
    "- Add or remove theory constraints to challenge the solver’s handling of mixed or unsupported theories."
)

form11 = (
    "Advanced Temporal and Non-standard Operations:\n"
    "- Introduce temporal logic operators or non-standard logics if supported.\n"
    "- Test the solver with multi-stage or time-based assertions, if supported.\n"
    "- Create complex nested assertions involving time or future/past constraints, if supported."
)