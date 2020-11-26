x = 15.00
y: int = x

# pyright issue https://github.com/microsoft/pyright/issues/1078
# Error message
# Expression of type "Literal[15]" cannot be assigned to declared type "int"
#  "Literal[15]" is incompatible with "int"
