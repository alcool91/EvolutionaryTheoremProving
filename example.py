from parser import parse_proof

to_prove = """
{} |=H ((p => (q => r)) => (q => (p => r)))
p => (q => r)
"""

ast = parse_proof(to_prove)
print()
print(ast)