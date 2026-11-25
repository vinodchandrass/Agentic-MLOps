from pathlib import Path
from html import escape
from reproduce_contrasts import reproduce

def main():
    rows = reproduce()
    out = Path(__file__).resolve().parents[1] / "generated"
    out.mkdir(exist_ok=True)
    for unit in ("pp","relative_percent","absolute"):
        subset = [r for r in rows if r["unit"] == unit]
        scale = 220/max(abs(r["difference"]) for r in subset)
        height = 85+42*len(subset)
        parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="960" height="{height}" viewBox="0 0 960 {height}">','<rect width="100%" height="100%" fill="white"/>',f'<text x="20" y="25" font-size="16">Descriptive contrasts: {unit} (provisional)</text>',f'<line x1="650" x2="650" y1="45" y2="{height-20}" stroke="black"/>']
        for i,r in enumerate(subset):
            y=55+42*i
            d=r["difference"]
            label=escape(r["study"]+" "+r["metric"]+" / "+r["comparator"])
            parts.append(f'<text x="20" y="{y+14}" font-size="12">{label}</text>')
            parts.append(f'<rect x="{650+min(0,d*scale)}" y="{y}" width="{abs(d*scale)}" height="18" fill="#446688"/>')
            parts.append(f'<text x="890" y="{y+14}" font-size="12">{d:+.4f}</text>')
        parts.append("</svg>")
        (out/f"contrasts_{unit}.svg").write_text("\n".join(parts),encoding="utf-8")

if __name__ == "__main__":
    main()
