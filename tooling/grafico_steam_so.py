#!/usr/bin/env python3
"""Grafica la Steam Survey por SO (docs/steam-historic-hardware-survey-os.tsv, compilacion de panke) -> docs/figuras/steam-linux.png y steam-so.png.
Celdas vacias = dato faltante (hueco, sin interpolar). Parseo por posicion; se verifica Windows+OSX+Linux ~ 100 % por mes."""
import csv
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
R = list(csv.reader(open('docs/steam-historic-hardware-survey-os.tsv', encoding='utf-8'), delimiter='\t'))
H = R[0][1:]; D = {r[0]: r[1:] for r in R[1:]}
nan = float('nan')
def col(n): return [float(x) if x.strip() else nan for x in D[n]]
def tot(prefix):  # suma de versiones visibles; hueco si ninguna version tiene dato
    ks = [k for k in D if k.startswith(prefix)]
    out = []
    for i in range(len(H)):
        v = [float(D[k][i]) for k in ks if D[k][i].strip()]
        out.append(sum(v) if v else nan)
    return out
W, O, L = col('Windows'), col('OSX'), col('Linux')
bad = [(H[i], W[i] + O[i] + L[i]) for i in range(len(H)) if H[i].strip() and abs(W[i] + O[i] + L[i] - 100) > .3]
print('meses con suma fuera de 100+-0.3:', bad)
ok = [i for i in range(len(H)) if L[i] == L[i]]
print('Linux: con dato', len(ok), 'primero', H[ok[0]], L[ok[0]], 'ultimo', H[ok[-1]], L[ok[-1]])
mx = max(ok, key=lambda i: L[i]); mn = min(ok, key=lambda i: L[i]); print('max', H[mx], L[mx], 'min', H[mn], L[mn])
print('meses de la tabla', sum(1 for h in H if h.strip()), 'sin dato Linux', [H[i] for i in range(len(H)) if H[i].strip() and L[i] != L[i]])
x = list(range(len(H))); yrs = [i for i, h in enumerate(H) if h.endswith('January')]
def fmt(ax):
    ax.set_xticks(yrs); ax.set_xticklabels([H[i][:4] for i in yrs]); ax.grid(alpha=.3)
fig, ax = plt.subplots(figsize=(8, 3.6)); ax.plot(x, L, lw=1.6, label='Linux (compilación de panke)')
ax.set_ylabel('Participación (%)'); ax.legend(fontsize=8); fmt(ax); fig.tight_layout(); fig.savefig('docs/figuras/steam-linux.png', dpi=200)
fig, (a, b) = plt.subplots(1, 2, figsize=(9, 3.6))
for n, v in (('Windows', W),): a.plot(x, v, label=n)
a.set_ylim(90, 100); a.set_ylabel('Participación (%)'); a.legend(fontsize=8); fmt(a)
for n, v in (('Linux', L), ('macOS (OSX)', O), ('Arch Linux', col('Arch Linux 64 bit')), ('Manjaro', col('Manjaro Linux 64 bit')),
             ('Ubuntu (suma de versiones visibles)', tot('Ubuntu')), ('Linux Mint (suma de versiones visibles)', tot('Linux Mint'))):
    b.plot(x, v, label=n, lw=1.2)
b.legend(fontsize=6); fmt(b); fig.tight_layout(); fig.savefig('docs/figuras/steam-so.png', dpi=200)
for n in ('Arch Linux 64 bit', 'Manjaro Linux 64 bit'):
    v = col(n); k = [i for i in range(len(H)) if v[i] == v[i]]; print(n, H[k[0]], v[k[0]], H[k[-1]], v[k[-1]], len(k))
