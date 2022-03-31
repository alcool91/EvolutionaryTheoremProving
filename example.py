from parser import parse_proof

to_prove = """
(p => (q => r)) => (q => (p => r))
"""

ast = parse_proof(to_prove)
print(ast)