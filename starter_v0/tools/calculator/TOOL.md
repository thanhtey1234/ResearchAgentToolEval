---
name: calculator
track: core
kind: local_computation
requires_env: []
inputs: [a, b, operation]
outputs: [a, b, operation, result]
side_effect: false
---
# calculator

Performs a basic arithmetic operation locally without calling an external API.
Pass numeric operands `a` and `b`, and set `operation` to `add`, `subtract`,
`multiply`, or `divide`. Returns both operands, the operation, and the numeric
result. Invalid operands, unsupported operations, and division by zero return
an error object.
