import random
import math
import os

random.seed(1337)

WIDTH = 1000
HEIGHT = 220

# Create nodes:
# 1. Very top edge sparse accents (y <= 25, well above any text)
nodes = [
    (35, 22), (130, 18), (250, 16), (370, 20), (460, 22)
]

# 2. Dense, beautiful neural / constellation cluster on the RIGHT (x: 520 to 975)
for _ in range(32):
    x = random.uniform(530, 975)
    y = random.uniform(18, HEIGHT - 18)
    nodes.append((x, y))

# Connect nodes based on distance
edges = []
for i in range(len(nodes)):
    dists = []
    for j in range(len(nodes)):
        if i == j: continue
        dx = nodes[i][0] - nodes[j][0]
        dy = nodes[i][1] - nodes[j][1]
        d = math.sqrt(dx*dx + dy*dy)
        # Connect nearby nodes
        if 35 < d < 135:
            dists.append((d, j))
    dists.sort()
    for d, j in dists[:4]:
        edge = (min(i, j), max(i, j))
        if edge not in edges:
            edges.append(edge)

print(f"Nodes: {len(nodes)}, Edges: {len(edges)}")

def build_svg(theme='dark'):
    if theme == 'dark':
        bg = "#0D1117"
        text_primary = "#FFFFFF"
        text_accent = "#00D9FF"
        text_secondary = "#8B949E"
        text_muted = "#58A6FF"
        # Soft starry white/silver graphic so it never clashes with cyan text!
        node_fill = "#FFFFFF"
        node_glow = "#FFFFFF"
        line_stroke = "#FFFFFF"
        line_base_opacity = 0.18
    else:
        bg = "#FFFFFF"
        text_primary = "#1F2328"
        text_accent = "#0969DA"
        text_secondary = "#656D76"
        text_muted = "#0969DA"
        node_fill = "#4B5563"
        node_glow = "#6B7280"
        line_stroke = "#6B7280"
        line_base_opacity = 0.22

    edges_lines = []
    for a, b in edges:
        x1, y1 = nodes[a]
        x2, y2 = nodes[b]
        edges_lines.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{line_stroke}" stroke-opacity="{line_base_opacity:.2f}" stroke-width="1.1"/>')

    nodes_circles = []
    for i, (x, y) in enumerate(nodes):
        r = random.uniform(2.4, 3.8)
        dur = random.uniform(2.4, 4.2)
        delay = (i * 0.18) % 3.0
        op = 0.45 if x < 500 else 0.75
        nodes_circles.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{node_fill}" opacity="{op}">'
            f'<animate attributeName="r" values="{r:.1f};{r+1.6:.1f};{r:.1f}" dur="{dur:.1f}s" repeatCount="indefinite" begin="{delay:.1f}s"/>'
            f'<animate attributeName="opacity" values="{op*0.6:.2f};{min(1.0, op*1.3):.2f};{op*0.6:.2f}" dur="{dur:.1f}s" repeatCount="indefinite" begin="{delay:.1f}s"/>'
            f'</circle>'
        )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="100%" height="{HEIGHT}">
  <defs>
    <style>
      .font-mono {{
        font-family: 'Fira Code', Consolas, 'Courier New', monospace;
      }}
      .emoji-font {{
        font-family: 'Apple Color Emoji', 'Segoe UI Emoji', 'Noto Color Emoji', sans-serif;
      }}
    </style>
    <filter id="glow-{theme}" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="1.8" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>

    <!-- Clip 1: reveals full sentence 1 smoothly, then erases -->
    <clipPath id="clip1-{theme}">
      <rect x="95" y="30" width="0" height="60">
        <animate attributeName="width" dur="11s" repeatCount="indefinite"
          values="0; 560; 560; 0; 0; 0"
          keyTimes="0; 0.18; 0.45; 0.49; 0.50; 1" />
      </rect>
    </clipPath>

    <!-- Clip 2: reveals full sentence 2 smoothly, then erases -->
    <clipPath id="clip2-{theme}">
      <rect x="95" y="30" width="0" height="60">
        <animate attributeName="width" dur="11s" repeatCount="indefinite"
          values="0; 0; 450; 450; 0; 0"
          keyTimes="0; 0.50; 0.66; 0.94; 0.98; 1" />
      </rect>
    </clipPath>
  </defs>

  <!-- Background -->
  <rect width="{WIDTH}" height="{HEIGHT}" fill="{bg}" rx="8"/>

  <!-- Neural / Constellation Mesh: Positioned on the right & top edge, clean starry white -->
  <g id="edges">
    {''.join(edges_lines)}
  </g>
  <g id="nodes" filter="url(#glow-{theme})">
    {''.join(nodes_circles)}
  </g>

  <!-- Header Content -->
  <!-- Top Row: Waving Hand aligned at y=72 -->
  <g transform="translate(50, 72)">
    <text x="0" y="0" font-size="34" class="emoji-font">
      👋
      <animateTransform
        attributeName="transform"
        type="rotate"
        values="0 17 -6; 14 17 -6; -10 17 -6; 14 17 -6; -4 17 -6; 10 17 -6; 0 17 -6"
        dur="2.5s"
        repeatCount="indefinite"
      />
    </text>
  </g>

  <!-- Sentence 1: Continuous single text element with crisp contrast -->
  <g clip-path="url(#clip1-{theme})">
    <text x="100" y="72" class="font-mono" font-size="31" font-weight="700">
      <tspan fill="{text_primary}">Hi there! I'm </tspan><tspan fill="{text_accent}">Nayan Utkarsh</tspan> <tspan fill="{text_accent}">|<animate attributeName="opacity" values="1;0;1" dur="0.8s" repeatCount="indefinite"/></tspan>
    </text>
  </g>

  <!-- Sentence 2: Continuous single text element with crisp contrast -->
  <g clip-path="url(#clip2-{theme})">
    <text x="100" y="72" class="font-mono" font-size="31" font-weight="700">
      <tspan fill="{text_primary}">Hi there! I'm </tspan><tspan fill="{text_accent}">Gigaberg</tspan> <tspan fill="{text_accent}">|<animate attributeName="opacity" values="1;0;1" dur="0.8s" repeatCount="indefinite"/></tspan>
    </text>
  </g>

  <!-- Role / Subtitle -->
  <text x="100" y="108" class="font-mono" font-size="14.5" font-weight="600" fill="{text_secondary}">
    AI/ML Engineer <tspan fill="{text_accent}">·</tspan> Full-Stack <tspan fill="{text_accent}">·</tspan> Systems Builder
  </text>

  <!-- Detail Subtitle -->
  <text x="100" y="134" class="font-mono" font-size="12.5" fill="{text_secondary}">
    Bengaluru, India <tspan fill="{text_accent}">·</tspan> B.Tech CSE (AI &amp; ML) <tspan fill="{text_accent}">·</tspan> Class of 2028
  </text>

  <!-- Divider -->
  <line x1="100" y1="152" x2="420" y2="152" stroke="{text_accent}" stroke-width="1.5" stroke-opacity="0.5"/>

  <!-- Live prompt / terminal line -->
  <text x="100" y="174" class="font-mono" font-size="12" fill="{text_muted}">
    <tspan fill="{text_accent}">&gt;</tspan> LLMs · RAG · Explainable AI · Hardware Systems
  </text>
  <text x="100" y="196" class="font-mono" font-size="12" fill="{text_accent}" opacity="0.9">
    <animate attributeName="opacity" values="0.9;0.4;0.9" dur="2.2s" repeatCount="indefinite"/>
    <tspan fill="{text_accent}">&gt;</tspan> building practical AI systems_
  </text>
</svg>"""
    return svg

os.makedirs('assets', exist_ok=True)

with open('assets/header-dark.svg', 'w', encoding='utf-8') as f:
    f.write(build_svg('dark'))

with open('assets/header-light.svg', 'w', encoding='utf-8') as f:
    f.write(build_svg('light'))

print("Generated repositioned white graphic SVGs successfully!")
