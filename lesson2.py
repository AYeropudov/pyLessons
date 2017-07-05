M = [[1, 2, 3],
     [4, 5, 6],
     [7, 8, 9]]
print M
print M[1]
print M[1][2]

col3 = [row[1] for row in M]
print col3

[row[1] + 1 for row in M]

diag = [M[i][i] for i in [1, 0, 2]]
print  diag

doubless = [c + "f" for c in 'spamm']
print doubless

G = (sum(row) for row in M)
print next(G)
