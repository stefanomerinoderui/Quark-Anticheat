#!/usr/bin/env python3
"""Grafica el reparto de la Steam Survey por idioma (docs/steam-historic-hardware-survey.tsv) -> docs/figuras/steam-idiomas.png.
Meses sin dato quedan como huecos. Series empalmadas: 'Spanish' (hasta 2018-09) + 'Spain'+'Latin America' (desde 2018-10); idem portugues de Brasil."""
import csv, sys
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
R = list(csv.reader(open('docs/steam-historic-hardware-survey.tsv', encoding='utf-8'), delimiter='\t'))
H = R[0]; D = {r[0]: r[1:] for r in R[1:]}
def num(x):
    try: return float(x)
    except ValueError: return None
def col(n): return [num(x) for x in D[n]] + [None] * (len(H) - 1 - len(D[n]))
def add(a, b): return [x + y if x is not None and y is not None else None for x, y in zip(a, b)]
def splice(old, new): return [n if n is not None else o for o, n in zip(old, new)]
S = {'Inglés': col('English'), 'Chino simplificado': col('Simplified Chinese'), 'Ruso': col('Russian'),
     'Español (España + LatAm)': splice(col('Spanish'), add(col('Spanish - Spain'), col('Spanish - Latin America'))),
     'Portugués (Brasil)': splice(col('Brazilian Portuguese'), col('Portuguese-Brazil'))}
x = list(range(len(H) - 1))
fig, ax = plt.subplots(figsize=(8, 4.2))
for n, v in S.items():
    ax.plot(x, [float('nan') if a is None else a for a in v], label=n, lw=1.5)
    f = [(i, a) for i, a in enumerate(v) if a is not None]
    print(n, 'primero', H[1 + f[0][0]], f[0][1], 'ultimo', H[1 + f[-1][0]], f[-1][1], 'con dato', len(f), 'de', len(x))
yrs = [i for i, h in enumerate(H[1:]) if h.endswith('January')]
ax.set_xticks(yrs); ax.set_xticklabels([H[1 + i][:4] for i in yrs])
ax.set_ylabel('Participación (%)'); ax.grid(alpha=.3); ax.legend(fontsize=8)
fig.tight_layout(); fig.savefig('docs/figuras/steam-idiomas.png', dpi=200)
