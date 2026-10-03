"""Generate light and dark hero SVGs for the GitHub profile README."""

import math
import sys
from pathlib import Path

THEMES = {
    "light": dict(
        bg="#ffffff", dots="#d8dee4", border="#d0d7de", text="#1f2328",
        muted="#656d76", faint="#d0d7de", node="#ffffff", stroke="#8c959f",
        teal="#0d9488", amber="#d97706", glow="0.10",
    ),
    "dark": dict(
        bg="#0d1117", dots="#21262d", border="#30363d", text="#e6edf3",
        muted="#8b949e", faint="#30363d", node="#0d1117", stroke="#6e7681",
        teal="#2dd4bf", amber="#fbbf24", glow="0.16",
    ),
}

W, H = 1200, 470
DY = 26  # vertical offset of the diagram below the title block
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

SOURCES = ["telemetry", "documents", "databases", "APIs", "SaaS"]
SRC_Y = [204 + DY + 40 * i for i in range(5)]
MID = 280 + DY

ONT_NODES = [(380, 262), (440, 240), (505, 258), (575, 240),
             (410, 315), (480, 300), (550, 318), (600, 290)]
ONT_NODES = [(x, y + DY) for x, y in ONT_NODES]
ONT_EDGES = [(0, 1), (1, 2), (2, 3), (0, 4), (1, 5), (4, 5),
             (5, 2), (5, 6), (6, 7), (3, 7), (2, 6)]

AGENT = (730, MID)
OUTCOMES = ["insight", "recommendation", "action"]
OUT_Y = [MID - 66, MID, MID + 66]
PILL_X, PILL_W, PILL_H = 860, 200, 36
LOOP_Y = 436
PULSE_PX = 22  # visible length of a travelling pulse, in pixels


def cubic_len(p0, p1, p2, p3, n=64):
    pts = [tuple((1-u)**3*a + 3*(1-u)**2*u*b + 3*(1-u)*u**2*c + u**3*d
                 for a, b, c, d in zip(p0, p1, p2, p3)) for u in (i / n for i in range(n + 1))]
    return sum(math.dist(pts[i], pts[i + 1]) for i in range(n))


def dash(length):
    """Dash size in pathLength=100 units so every pulse looks PULSE_PX long."""
    return f"--d:{100 * PULSE_PX / length:.2f}"


def icon(name, y, c):
    """Small glyph for each data source, centred on x=92."""
    s = f'stroke="{c}" stroke-width="1.6" fill="none" stroke-linejoin="round" stroke-linecap="round"'
    if name == "telemetry":
        return f'<polyline {s} points="82,{y+4} 86,{y-1} 90,{y+3} 95,{y-7} 98,{y-1} 102,{y-3}"/>'
    if name == "documents":
        return (f'<path {s} d="M85,{y-9} h9 l5,5 v13 h-14 z"/>'
                f'<path {s} d="M94,{y-9} v5 h5"/>')
    if name == "databases":
        return (f'<ellipse {s} cx="92" cy="{y-6}" rx="7" ry="2.6"/>'
                f'<path {s} d="M85,{y-6} v11 a7,2.6 0 0 0 14,0 v-11"/>'
                f'<path {s} d="M85,{y-0.5} a7,2.6 0 0 0 14,0"/>')
    if name == "APIs":
        return (f'<text x="92" y="{y+4.5}" text-anchor="middle" font-family="{MONO}" '
                f'font-size="13" font-weight="600" fill="{c}">{{ }}</text>')
    return "".join(f'<rect {s} x="{x}" y="{yy}" width="6.5" height="6.5" rx="1.6"/>'
                    for x in (84.5, 93) for yy in (y - 7.5, y + 1))


def hexagon(cx, cy, r):
    pts = [(cx + r * math.cos(math.radians(60 * i - 90)),
            cy + r * math.sin(math.radians(60 * i - 90))) for i in range(6)]
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)


def build(t):
    o = []
    a = o.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
      f'role="img" aria-labelledby="title desc">')
    a('<title id="title">Zeyu Chen: building the enterprise context layer</title>')
    a('<desc id="desc">Data sources such as telemetry, documents, databases, APIs and SaaS flow into '
      'an ontology-based context layer. AI agents reason over it to produce insights, recommendations '
      'and actions, and actions are written back to the source systems under governance.</desc>')

    a(f"""<style>
.pulse{{fill:none;stroke-linecap:round;stroke-dasharray:var(--d) 200;stroke-dashoffset:var(--d);opacity:0}}
.in{{animation:in 10s linear infinite both}}
.to-agent{{animation:toagent 10s linear infinite both}}
.out{{animation:out 10s linear infinite both}}
.back{{animation:back 10s linear infinite both}}
.lit{{opacity:0;animation:lit 10s ease-in-out infinite both}}
.agent-lit{{opacity:0;animation:agentlit 10s ease-in-out infinite both}}
.ring{{opacity:0;transform-box:fill-box;transform-origin:center;animation:ring 10s ease-out infinite both}}
.pill-lit{{opacity:0;animation:pill 10s ease-in-out infinite both}}
.src-lit{{opacity:0;animation:src 10s ease-in-out infinite both}}
.ants{{stroke-dasharray:5 7;animation:ants 1.4s linear infinite}}
.cursor{{animation:blink 1.1s steps(1) infinite}}
@keyframes in{{0%{{stroke-dashoffset:var(--d);opacity:0}}1%{{opacity:1}}20%{{stroke-dashoffset:-100;opacity:1}}21%,100%{{stroke-dashoffset:-100;opacity:0}}}}
@keyframes toagent{{0%,37%{{stroke-dashoffset:var(--d);opacity:0}}38%{{opacity:1}}45%{{stroke-dashoffset:-100;opacity:1}}46%,100%{{stroke-dashoffset:-100;opacity:0}}}}
@keyframes out{{0%,48%{{stroke-dashoffset:var(--d);opacity:0}}49%{{opacity:1}}58%{{stroke-dashoffset:-100;opacity:1}}59%,100%{{stroke-dashoffset:-100;opacity:0}}}}
@keyframes back{{0%,66%{{stroke-dashoffset:var(--d);opacity:0}}67%{{opacity:1}}86%{{stroke-dashoffset:-100;opacity:1}}87%,100%{{stroke-dashoffset:-100;opacity:0}}}}
@keyframes lit{{0%,19%{{opacity:0}}25%{{opacity:1}}82%{{opacity:1}}92%,100%{{opacity:0}}}}
@keyframes agentlit{{0%,44%{{opacity:0}}48%{{opacity:1}}84%{{opacity:1}}93%,100%{{opacity:0}}}}
@keyframes ring{{0%,45%{{opacity:0;transform:scale(1)}}47%{{opacity:.9;transform:scale(1)}}60%{{opacity:0;transform:scale(1.9)}}100%{{opacity:0}}}}
@keyframes pill{{0%,56%{{opacity:0}}60%{{opacity:1}}86%{{opacity:1}}94%,100%{{opacity:0}}}}
@keyframes src{{0%,84%{{opacity:0}}87%{{opacity:1}}95%,100%{{opacity:0}}}}
@keyframes ants{{to{{stroke-dashoffset:-24}}}}
@keyframes blink{{0%{{opacity:1}}50%{{opacity:0}}}}
@media (prefers-reduced-motion:reduce){{
  *{{animation:none!important}}
  .pulse{{opacity:0}}
  .lit,.agent-lit,.pill-lit{{opacity:1}}
}}
</style>""")

    a(f"""<defs>
<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="{t['dots']}"/></pattern>
<radialGradient id="halo" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{t['teal']}" stop-opacity="{t['glow']}"/><stop offset="1" stop-color="{t['teal']}" stop-opacity="0"/></radialGradient>
<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t['bg']}" stop-opacity="1"/><stop offset=".45" stop-color="{t['bg']}" stop-opacity="0"/></linearGradient>
<filter id="glow" filterUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="{t['amber']}"/></marker>
<clipPath id="card"><rect x="4" y="4" width="{W-8}" height="{H-8}" rx="18"/></clipPath>
</defs>""")

    # Card, dot grid, fade over the title area, glow behind the context layer
    a(f'<rect x="4" y="4" width="{W-8}" height="{H-8}" rx="18" fill="{t["bg"]}"/>')
    a('<g clip-path="url(#card)">')
    a(f'<rect width="{W}" height="{H}" fill="url(#dots)"/>')
    a(f'<rect width="{W}" height="{H}" fill="url(#fade)"/>')
    a(f'<ellipse cx="485" cy="{MID}" rx="300" ry="170" fill="url(#halo)"/>')
    a("</g>")
    a(f'<rect x="4" y="4" width="{W-8}" height="{H-8}" rx="18" fill="none" stroke="{t["border"]}"/>')

    # Title block
    a(f'<text x="56" y="98" font-family="{SANS}" font-size="56" font-weight="700" '
      f'letter-spacing="-1.5" fill="{t["text"]}">Zeyu Chen</text>')
    a(f'<text x="{W-56}" y="62" text-anchor="end" font-family="{MONO}" font-size="12" '
      f'letter-spacing="2" fill="{t["muted"]}">AI &amp; DATA ENGINEER · SYDNEY</text>')
    a(f'<text x="56" y="140" font-family="{SANS}" font-size="22" fill="{t["text"]}">'
      f'Building the enterprise context layer,</text>')
    a(f'<text x="56" y="172" font-family="{SANS}" font-size="22" fill="{t["muted"]}">'
      f'where AI goes from answers to <tspan fill="{t["amber"]}" font-weight="600">governed action.</tspan>'
      f'<tspan class="cursor" fill="{t["amber"]}" font-family="{MONO}"> ▍</tspan></text>')

    # Column captions
    cap = f'font-family="{MONO}" font-size="10.5" letter-spacing="2" fill="{t["muted"]}"'
    a(f'<text x="80" y="{SRC_Y[0]-26}" {cap}>SOURCES</text>')
    a(f'<text x="{AGENT[0]}" y="{SRC_Y[0]-26}" text-anchor="middle" {cap}>REASON</text>')
    a(f'<text x="{PILL_X}" y="{SRC_Y[0]-26}" {cap}>ACT</text>')

    # Sources: icon, label, base edge, pulse, write-back highlight
    for i, (name, y) in enumerate(zip(SOURCES, SRC_Y)):
        ty = MID + (y - MID) * 0.35
        d = f"M200,{y} C265,{y} 275,{ty:.1f} 330,{ty:.1f}"
        a(f'<path d="{d}" fill="none" stroke="{t["faint"]}" stroke-width="1.5"/>')
        a(f'<path class="pulse in" d="{d}" pathLength="100" stroke="{t["teal"]}" stroke-width="3" '
          f'filter="url(#glow)" style="{dash(cubic_len((200, y), (265, y), (275, ty), (330, ty)))}"/>')
        a(icon(name, y, t["muted"]))
        a(f'<circle class="src-lit" cx="92" cy="{y}" r="14" fill="none" stroke="{t["amber"]}" '
          f'stroke-width="1.5" style="animation-delay:{0.12*(4-i):.2f}s"/>')
        a(f'<text x="112" y="{y+4.5}" font-family="{MONO}" font-size="13" fill="{t["text"]}">{name}</text>')

    # Context layer box with ontology graph
    bx, by, bw, bh = 330, 192 + DY, 310, 176
    a(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="14" fill="{t["bg"]}" fill-opacity="0.6" '
      f'stroke="{t["teal"]}" stroke-opacity="0.55" stroke-width="1.5"/>')
    a(f'<text x="{bx+20}" y="{by+24}" {cap}>CONTEXT LAYER</text>')
    a(f'<text x="{bx+bw-20}" y="{by+24}" text-anchor="end" font-family="{MONO}" font-size="10.5" '
      f'fill="{t["teal"]}">ontology</text>')
    for i, j in ONT_EDGES:
        (x1, y1), (x2, y2) = ONT_NODES[i], ONT_NODES[j]
        a(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{t["stroke"]}" stroke-opacity="0.5" stroke-width="1.2"/>')
        a(f'<line class="lit" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{t["teal"]}" stroke-width="1.6" '
          f'style="animation-delay:{0.09*max(i, j):.2f}s"/>')
    for k, (x, y) in enumerate(ONT_NODES):
        a(f'<circle cx="{x}" cy="{y}" r="5.5" fill="{t["node"]}" stroke="{t["stroke"]}" stroke-width="1.5"/>')
        a(f'<g class="lit" style="animation-delay:{0.09*k:.2f}s">'
          f'<circle cx="{x}" cy="{y}" r="11" fill="{t["teal"]}" fill-opacity="0.18"/>'
          f'<circle cx="{x}" cy="{y}" r="5.5" fill="{t["teal"]}"/></g>')
    a(f'<text x="{bx+20}" y="{by+bh-16}" font-family="{MONO}" font-size="11" fill="{t["muted"]}">'
      f'entities · relations · rules · actions</text>')

    # Context layer -> agent
    d = f"M{bx+bw},{MID} H{AGENT[0]-26}"
    a(f'<path d="{d}" fill="none" stroke="{t["faint"]}" stroke-width="1.5"/>')
    a(f'<path class="pulse to-agent" d="{d}" pathLength="100" stroke="{t["teal"]}" stroke-width="3.5" '
      f'filter="url(#glow)" style="{dash(AGENT[0] - 26 - bx - bw)}"/>')

    # Agent
    ax, ay = AGENT
    a(f'<polygon class="ring" points="{hexagon(ax, ay, 24)}" fill="none" stroke="{t["teal"]}" stroke-width="1.5"/>')
    a(f'<polygon points="{hexagon(ax, ay, 24)}" fill="{t["node"]}" stroke="{t["text"]}" stroke-width="1.8"/>')
    a(f'<polygon class="agent-lit" points="{hexagon(ax, ay, 24)}" fill="{t["teal"]}" fill-opacity="0.16" '
      f'stroke="{t["teal"]}" stroke-width="1.8"/>')
    a(f'<text x="{ax}" y="{ay+4.5}" text-anchor="middle" font-family="{MONO}" font-size="13" '
      f'font-weight="700" fill="{t["text"]}">AI</text>')
    a(f'<text x="{ax}" y="{ay+46}" text-anchor="middle" font-family="{MONO}" font-size="12" '
      f'fill="{t["muted"]}">agents</text>')

    # Agent -> outcomes
    for i, (name, y) in enumerate(zip(OUTCOMES, OUT_Y)):
        is_action = name == "action"
        c = t["amber"] if is_action else t["teal"]
        d = f"M{ax+26},{ay} C{ax+75},{ay} {ax+80},{y} {PILL_X},{y}"
        a(f'<path d="{d}" fill="none" stroke="{t["faint"]}" stroke-width="1.5"/>')
        a(f'<path class="pulse out" d="{d}" pathLength="100" stroke="{c}" stroke-width="3" '
          f'filter="url(#glow)" style="{dash(cubic_len((ax+26, ay), (ax+75, ay), (ax+80, y), (PILL_X, y)))}"/>')
        px, py = PILL_X, y - PILL_H / 2
        a(f'<rect x="{px}" y="{py}" width="{PILL_W}" height="{PILL_H}" rx="18" fill="{t["node"]}" '
          f'stroke="{c if is_action else t["stroke"]}" stroke-width="1.4"/>')
        a(f'<rect class="pill-lit" x="{px}" y="{py}" width="{PILL_W}" height="{PILL_H}" rx="18" '
          f'fill="{c}" fill-opacity="0.14" stroke="{c}" stroke-width="1.6"/>')
        a(f'<circle cx="{px+20}" cy="{y}" r="4" fill="{c}"/>')
        a(f'<text x="{px+34}" y="{y+4.5}" font-family="{MONO}" font-size="13" '
          f'fill="{t["amber"] if is_action else t["text"]}" font-weight="{600 if is_action else 400}">{name}</text>')

    # Governed write-back loop: action -> back to the sources
    ry = OUT_Y[2]
    d = (f"M{PILL_X+PILL_W},{ry} C{PILL_X+PILL_W+50},{ry} {PILL_X+PILL_W+50},{LOOP_Y} {PILL_X+PILL_W},{LOOP_Y} "
         f"H120 C92,{LOOP_Y} 92,{LOOP_Y} 92,{SRC_Y[-1]+18}")
    a(f'<path class="ants" d="{d}" fill="none" stroke="{t["amber"]}" stroke-opacity="0.55" stroke-width="1.4" '
      f'marker-end="url(#arrow)"/>')
    back_len = (cubic_len((PILL_X+PILL_W, ry), (PILL_X+PILL_W+50, ry), (PILL_X+PILL_W+50, LOOP_Y), (PILL_X+PILL_W, LOOP_Y))
                + PILL_X + PILL_W - 120 + cubic_len((120, LOOP_Y), (92, LOOP_Y), (92, LOOP_Y), (92, SRC_Y[-1]+18)))
    a(f'<path class="pulse back" d="{d}" pathLength="100" stroke="{t["amber"]}" stroke-width="3" '
      f'filter="url(#glow)" style="{dash(back_len)}"/>')
    lx = 600
    a(f'<text x="{lx}" y="{LOOP_Y-8}" text-anchor="middle" font-family="{MONO}" font-size="11.5" '
      f'letter-spacing="1" fill="{t["amber"]}">governed write-back · audited</text>')

    a("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent
    out.mkdir(parents=True, exist_ok=True)
    for name, theme in THEMES.items():
        (out / f"hero-{name}.svg").write_text(build(theme) + "\n")
