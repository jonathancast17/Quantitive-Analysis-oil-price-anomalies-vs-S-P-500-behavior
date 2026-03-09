import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

print("Descargando datos...")

petroleo = yf.download("CL=F", start="2015-01-01")["Close"].squeeze()
sp500    = yf.download("^GSPC", start="2015-01-01")["Close"].squeeze()
bonos    = yf.download("^TNX",  start="2015-01-01")["Close"].squeeze()

cambio_petroleo = petroleo.pct_change() * 100
cambio_sp500    = sp500.pct_change() * 100

media  = cambio_petroleo.mean()
std    = cambio_petroleo.std()
zscore = (cambio_petroleo - media) / std

lunes_salto = cambio_petroleo[
    (cambio_petroleo.index.dayofweek == 0) &
    (cambio_petroleo > 7)
]

print(f"\n--- LUNES CON SALTO >7% EN PETRÓLEO (2015-hoy) ---")
print(f"Total encontrados: {len(lunes_salto)}")

resultados = []
for fecha in lunes_salto.index:
    fecha_fin = fecha + timedelta(days=3)
    sp_window = cambio_sp500[
        (cambio_sp500.index > fecha) &
        (cambio_sp500.index <= fecha_fin)
    ]
    rendimiento_48h = sp_window.sum()
    resultados.append({
        "fecha": fecha,
        "salto_petroleo": lunes_salto[fecha],
        "sp500_48h": rendimiento_48h,
        "zscore": zscore[fecha]
    })
    print(f"  {fecha.strftime('%d %b %Y')} | "
          f"Petróleo: +{lunes_salto[fecha]:.1f}% | "
          f"Z-Score: {zscore[fecha]:.1f}σ | "
          f"S&P 48h: {rendimiento_48h:.1f}%")

if resultados:
    sp_positivos = sum(1 for r in resultados if r["sp500_48h"] > 0)
    sp_negativos = sum(1 for r in resultados if r["sp500_48h"] < 0)
    prob_sube = (sp_positivos / len(resultados)) * 100
    prob_baja = (sp_negativos / len(resultados)) * 100
    promedio_movimiento = np.mean([r["sp500_48h"] for r in resultados])

    print(f"\n--- PROBABILIDAD HISTÓRICA ---")
    print(f"  S&P sube en 48h:  {prob_sube:.0f}%")
    print(f"  S&P baja en 48h:  {prob_baja:.0f}%")
    print(f"  Movimiento promedio: {promedio_movimiento:.2f}%")

    zscore_hoy = zscore.iloc[-1]
    print(f"\n--- ANOMALÍA DE HOY ---")
    print(f"  Z-Score actual del petróleo: {zscore_hoy:.2f}σ")
    if abs(zscore_hoy) > 3:
        print("  ⚠️  ANOMALÍA ESTADÍSTICA DETECTADA (>3σ)")
        print("  Potential Credit Crunch Signal identified")
    elif abs(zscore_hoy) > 2:
        print("  ⚡ Movimiento inusual (>2σ) — monitorear")
    else:
        print("  Movimiento dentro de rangos normales")


fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 12))

ax1b = ax1.twinx()
ax1.plot(petroleo.index, petroleo.to_numpy(), 
         color="orange", linewidth=1, label="Petróleo WTI")
ax1b.plot(sp500.index, sp500.to_numpy(), 
          color="steelblue", linewidth=1, label="S&P 500", alpha=0.7)
ax1.set_ylabel("Petróleo (USD)", color="orange")
ax1b.set_ylabel("S&P 500", color="steelblue")
ax1.set_title("Petróleo WTI vs S&P 500 — 10 años", fontweight="bold")
ax1.grid(True, alpha=0.2)

for fecha in lunes_salto.index:
    ax1.axvline(x=fecha, color="red", alpha=0.4, linewidth=1.5)


zscore_vals = zscore.to_numpy()
zscore_idx  = zscore.index.to_numpy()
ax2.plot(zscore_idx, zscore_vals, color="purple", linewidth=0.8)
ax2.axhline(y=3,  color="red",    linestyle="--", alpha=0.7, label="+3σ anomalía")
ax2.axhline(y=-3, color="red",    linestyle="--", alpha=0.7, label="-3σ anomalía")
ax2.axhline(y=0,  color="gray",   linestyle="-",  alpha=0.3)
ax2.fill_between(zscore_idx, zscore_vals, 3,
                 where=(zscore_vals > 3), color="red", alpha=0.3)
ax2.fill_between(zscore_idx, zscore_vals, -3,
                 where=(zscore_vals < -3), color="red", alpha=0.3)
ax2.set_title("Z-Score del Petróleo — Anomalías estadísticas", fontweight="bold")
ax2.set_ylabel("Desviaciones estándar (σ)")
ax2.legend(fontsize=8)
ax2.grid(True, alpha=0.2)


ax3b = ax3.twinx()
ax3.plot(petroleo.index, petroleo.to_numpy(),
         color="orange", linewidth=1, label="Petróleo")
ax3b.plot(bonos.index, bonos.to_numpy(),
          color="green", linewidth=1, label="US10Y Bonos", alpha=0.7)
ax3.set_ylabel("Petróleo (USD)", color="orange")
ax3b.set_ylabel("Rendimiento Bonos %", color="green")
ax3.set_title("Petróleo vs Bonos US10Y — Credit Crunch Signal", fontweight="bold")
ax3.grid(True, alpha=0.2)

plt.tight_layout()
plt.savefig("petroleo_analisis.png", dpi=150)
print("\nGráfica guardada como petroleo_analisis.png")