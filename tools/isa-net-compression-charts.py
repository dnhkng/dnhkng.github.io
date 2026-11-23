"""Charts for the ISA-NET compression post. Data: Projects/results/results.jsonl + LTCB table."""
import json, zipfile
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch

OUT = Path(r"C:\Users\dnhkn\Documents\Projects\dnhkng.github.io\assets\img\isa-net-compression")
OUT.mkdir(parents=True, exist_ok=True)
RES = Path(r"C:\Users\dnhkn\Documents\Projects\results\results.jsonl")
KIT = Path(r"C:\Users\dnhkn\Documents\Overview\ternlog-compressor-bench-2026-11-22\ternlog_compressor_bench_kit_2026-11-22.zip")

SURF = "#fcfcfb"; INK = "#0b0b0b"; INK2 = "#52514e"; MUTED = "#8a8984"; GRID = "#e4e3df"
BLUE = "#2a78d6"; ORANGE = "#eb6834"; AQUA = "#1baf7a"; GRAY = "#b9b8b2"; GRAY_D = "#7d7c77"

fam = "Segoe UI" if any("Segoe UI" in f.name for f in font_manager.fontManager.ttflist) else "DejaVu Sans"
plt.rcParams.update({
    "font.family": fam, "font.size": 12, "text.color": INK, "axes.labelcolor": INK2,
    "xtick.color": INK2, "ytick.color": INK2, "axes.edgecolor": GRID, "figure.facecolor": SURF,
    "axes.facecolor": SURF, "savefig.facecolor": SURF, "axes.spines.top": False, "axes.spines.right": False,
    "axes.titleweight": "semibold", "axes.titlesize": 15, "axes.titlelocation": "left",
})

rows = [json.loads(l) for l in RES.read_text().splitlines() if l.strip()]
def get(file, tool):
    for r in rows:
        if r["file"] == file and r["tool"] == tool:
            return r
    raise KeyError((file, tool))

NAMES = {"jolt1": "ISA-NET Jolt", "jolt4": "Jolt, 4 workers", "cmix_dic": "cmix v21 + dict",
         "cmix_nodic": "cmix v21, no dict", "paq8px": "paq8px -11L", "ppmd": "PPMd (7-Zip)",
         "xz": "xz -9e", "zstd": "zstd -22", "bzip2": "bzip2 -9"}

def save(fig, name):
    fig.savefig(OUT / name, dpi=200, bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)
    print("wrote", name)

def footer(fig, text):
    fig.text(0.0, -0.02, text, ha="left", va="top", fontsize=9.5, color=MUTED, transform=fig.transFigure)

# ---------------------------------------------------------------- 1. speed vs size (the money chart)
fig, ax = plt.subplots(figsize=(10, 6.2))
tools = ["cmix_dic", "cmix_nodic", "paq8px", "jolt1", "ppmd", "bzip2", "xz", "zstd"]
offsets = {"cmix_dic": (0, 18), "cmix_nodic": (-10, 0), "paq8px": (10, 0), "jolt1": (14, 0),
           "ppmd": (0, 16), "bzip2": (10, 0), "xz": (-10, 0), "zstd": (10, 0)}
ha = {"ppmd": "center", "xz": "right", "cmix_nodic": "right", "cmix_dic": "center"}
for t in tools:
    r = get("dev1", t)
    x, y = r["encode"]["kB_per_s"], r["bpb"]
    hero = t == "jolt1"
    ax.scatter([x], [y], s=170 if hero else 70, color=BLUE if hero else GRAY, zorder=3,
               edgecolor=SURF, linewidth=2)
    ax.annotate(NAMES[t] + (f"\n{y:.3f} bpb, {x:.0f} kB/s" if hero else ""), (x, y),
                xytext=offsets[t], textcoords="offset points", ha=ha.get(t, "left"), va="center",
                fontsize=12.5 if hero else 11, color=INK if hero else INK2,
                fontweight="semibold" if hero else "normal")
ax.set_xscale("log")
ax.set_xlim(0.5, 60000)
ax.set_xticks([1, 10, 100, 1000, 10000], ["1", "10", "100", "1,000", "10,000"])
ax.set_ylim(1.26, 2.45)
ax.invert_yaxis()
ax.set_xlabel("Compression speed, kB/s, one core (log scale)")
ax.set_ylabel("Bits per byte (lower is better)")
ax.grid(True, which="major", color=GRID, linewidth=0.8)
ax.set_axisbelow(True)
cm = get("dev1", "cmix_dic"); jo = get("dev1", "jolt1")
ax.annotate("", xy=(jo["encode"]["kB_per_s"], jo["bpb"]), xytext=(cm["encode"]["kB_per_s"], cm["bpb"]),
            arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.6, shrinkA=9, shrinkB=12, mutation_scale=16))
ax.text(9.8, 1.395, "38x faster, 0.1 % larger", color=BLUE, ha="center", fontsize=11.5, fontweight="semibold")
ax.set_title("Same Mac, same megabyte: size against speed")
footer(fig, "Held-out 1 MB of enwik9 (bytes 909M-910M). Apple M4 Pro, single core, every round trip verified byte-exact.\n"
            "Encode speed shown; decode speeds are similar for the context mixers and Jolt, much faster for xz/zstd/bzip2.")
save(fig, "speed_vs_size.png")

# ---------------------------------------------------------------- 2. memory
fig, ax = plt.subplots(figsize=(10, 4.8))
mem = [  # (label, bytes, hero) peak footprint/RSS on dev1 encode
    ("cmix v21 + dict", 18.6 * 2**30, False),
    ("paq8px -11L", get("dev1", "paq8px")["encode"]["max_rss_bytes"], False),
    ("xz -9e", get("dev1", "xz")["encode"]["max_rss_bytes"], False),
    ("zstd -22", get("dev1", "zstd")["encode"]["max_rss_bytes"], False),
    ("PPMd (7-Zip)", get("dev1", "ppmd")["encode"]["max_rss_bytes"], False),
    ("ISA-NET Jolt", get("dev1", "jolt1")["encode"]["max_rss_bytes"], True),
    ("bzip2 -9", get("dev1", "bzip2")["encode"]["max_rss_bytes"], False),
]
labels = [m[0] for m in mem][::-1]; vals = [m[1] / 2**20 for m in mem][::-1]; hero = [m[2] for m in mem][::-1]
y = np.arange(len(vals))
ax.barh(y, vals, height=0.6, color=[BLUE if h else GRAY for h in hero], zorder=3)
for yi, v, h in zip(y, vals, hero):
    txt = f"{v/1024:.1f} GB" if v >= 1024 else f"{v:.0f} MB"
    ax.text(v * 1.15, yi, txt, va="center", fontsize=11, color=INK if h else INK2,
            fontweight="semibold" if h else "normal")
ax.set_yticks(y, labels)
for tl, h in zip(ax.get_yticklabels(), hero):
    if h: tl.set_fontweight("semibold"); tl.set_color(INK)
ax.set_xscale("log"); ax.set_xlim(3, 2e5)
ax.set_xticks([10, 100, 1000, 10000, 100000], ["10 MB", "100 MB", "1 GB", "10 GB", "100 GB"])
ax.set_xlabel("Peak memory while compressing 1 MB (log scale, MB)")
ax.grid(True, axis="x", color=GRID, linewidth=0.8); ax.set_axisbelow(True)
ax.spines["left"].set_visible(False); ax.tick_params(axis="y", length=0)
ax.set_title("Memory: the whole model fits in a performance-core L2")
footer(fig, "Peak resident set from /usr/bin/time -l; cmix shown as its 18.6 GB peak footprint (macOS compressed part of it,\n"
            "so its RSS read 7.9 GB). Jolt's 7.05 MB model is inside its 14 MB.")
save(fig, "memory.png")

# ---------------------------------------------------------------- 3. LTCB placement
ltcb = [  # (name, total bytes, kind)
    ("cmix v21", 108_244_767, "ref"), ("paq8px v206fix1 -12L", 125_099_359, "ref"),
    ("zpaq 6.42 max", 142_257_365, "ref"), ("PPMonstr var. J", 157_049_402, "ref"),
    ("nanozip 0.09 (rank 55)", 161_715_074, "ref"), ("ISA-NET Jolt (not submitted)", 161_855_306, "hero"),
    ("7-Zip PPMd", 178_965_454, "ref"), ("PPMd var. J", 183_976_014, "ref"),
    ("xz, 1 GiB dictionary", 197_368_568, "ref"), ("zstd -22", 215_744_357, "ref"),
    ("bzip2 -9", 254_007_875, "ref"),
]
fig, ax = plt.subplots(figsize=(10, 5.8))
y = np.arange(len(ltcb))[::-1]
ax.barh(y, [v / 1e6 for _, v, _ in ltcb], height=0.62,
        color=[BLUE if k == "hero" else GRAY for _, _, k in ltcb], zorder=3)
for yi, (n, v, k) in zip(y, ltcb):
    ax.text(v / 1e6 + 2, yi, f"{v/1e6:.1f} MB", va="center", fontsize=11,
            color=INK if k == "hero" else INK2, fontweight="semibold" if k == "hero" else "normal")
ax.set_yticks(y, [n for n, _, _ in ltcb])
for tl, (_, _, k) in zip(ax.get_yticklabels(), ltcb):
    if k == "hero": tl.set_fontweight("semibold"); tl.set_color(INK)
ax.set_xlim(0, 290); ax.set_xlabel("enwik9 compressed size + decompressor, MB")
ax.grid(True, axis="x", color=GRID, linewidth=0.8); ax.set_axisbelow(True)
ax.spines["left"].set_visible(False); ax.tick_params(axis="y", length=0)
ax.set_title("Where 161.9 MB lands on the Large Text Compression Benchmark")
footer(fig, "Totals from mattmahoney.net/dc/text.html (Nov 19, 2026); Jolt measured on the M4, about 56th of roughly 240 entries.\n"
            "Jolt's total includes its zipped 7 MB model. It was trained on the first 900 MB of enwik9.")
save(fig, "ltcb.png")

# ---------------------------------------------------------------- 4. bpb vs file: static vs online learners
fig, ax = plt.subplots(figsize=(10, 5.2))
files = [("dev1", "1 MB\n(909M)"), ("dev4", "4 MB\n(909M-913M)"), ("test1", "1 MB test\n(959M)")]
series = [("cmix_dic", "cmix v21 + dict", ORANGE), ("jolt1", "ISA-NET Jolt", BLUE), ("paq8px", "paq8px -11L", AQUA)]
x = np.arange(len(files))
for k, (t, name, c) in enumerate(series):
    ys = [get(f, t)["bpb"] for f, _ in files]
    xs = x + (k - 1) * 0.16
    ax.scatter(xs, ys, s=110, color=c, edgecolor=SURF, linewidth=2, label=name, zorder=3)
    for xi, yv in zip(xs, ys):
        ax.annotate(f"{yv:.3f}", (xi, yv), xytext=(0, -15), textcoords="offset points",
                    ha="center", fontsize=9.5, color=INK2)
ax.set_xticks(x, [l for _, l in files]); ax.set_xlim(-0.5, 2.5); ax.set_ylim(1.63, 1.24)
ax.set_ylabel("Bits per byte (lower is better)")
ax.grid(True, axis="y", color=GRID, linewidth=0.8); ax.set_axisbelow(True)
ax.legend(loc="lower left", frameon=False, ncols=3, bbox_to_anchor=(0, 1.0), fontsize=10.5, handletextpad=0.3)
ax.set_title("A frozen model against learners that keep learning", pad=30)
footer(fig, "All three files are held out from Jolt's training. cmix and paq8px adapt as they read, so they gain on longer inputs;\n"
            "Jolt's weights are fixed, so its rate barely moves with length.")
save(fig, "bpb_by_file.png")

# ---------------------------------------------------------------- 5. time to compress enwik9
times = [  # (label, hours, measured?)
    ("cmix v21", 1e9 / (get("dev4", "cmix_dic")["encode"]["kB_per_s"] * 1000) / 3600, False),
    ("paq8px -11L", 1e9 / (get("dev4", "paq8px")["encode"]["kB_per_s"] * 1000) / 3600, False),
    ("ISA-NET Jolt, 1 core", 1e9 / (get("dev4", "jolt1")["encode"]["kB_per_s"] * 1000) / 3600, False),
    ("ISA-NET Jolt, 4 cores", 4500.71 / 3600, True),
    ("xz -9e", get("enwik9", "xz")["encode"]["median_wall_s"] / 3600, True),
    ("PPMd (7-Zip)", get("enwik9", "ppmd")["encode"]["median_wall_s"] / 3600, True),
]
fig, ax = plt.subplots(figsize=(10, 4.6))
y = np.arange(len(times))[::-1]
for yi, (n, h, meas) in zip(y, times):
    hero = "Jolt" in n
    c = BLUE if hero else GRAY
    ax.barh(yi, h, height=0.6, color=c if meas else SURF, edgecolor=c, hatch=None if meas else "////",
            linewidth=1.5, zorder=3)
    if h >= 48: txt = f"{h/24:.1f} days"
    elif h >= 1: txt = f"{h:.1f} h"
    else: txt = f"{h*60:.0f} min"
    ax.text(h * 1.15, yi, txt + ("" if meas else "  (extrapolated)"), va="center", fontsize=11,
            color=INK if hero else INK2, fontweight="semibold" if hero else "normal")
ax.set_yticks(y, [n for n, _, _ in times])
ax.set_xscale("log"); ax.set_xlim(0.01, 3000)
ax.set_xticks([1/60, 0.1, 1, 10, 100, 1000], ["1 min", "6 min", "1 h", "10 h", "100 h", "1000 h"])
ax.set_xlabel("Time to compress all of enwik9 (1 GB) on the M4 Pro, log scale")
ax.grid(True, axis="x", color=GRID, linewidth=0.8); ax.set_axisbelow(True)
ax.spines["left"].set_visible(False); ax.tick_params(axis="y", length=0)
ax.set_title("A gigabyte of Wikipedia: minutes, an hour, or a week")
footer(fig, "Solid bars measured on this Mac. Hatched bars extrapolated from the measured 4 MB throughput; context mixers usually\n"
            "slow down as their models fill, so the cmix and paq8px figures are optimistic. Decompression takes about as long.")
save(fig, "enwik9_time.png")

# ---------------------------------------------------------------- 6. hero image: bits of held-out Wikipedia
z = zipfile.ZipFile(KIT)
data = z.read("kit/data/dev_909M_1MB.bin")
start = data.find(b"The Comet Orchid was first discovered by Darwin")  # held-out enwik9, byte 909,210,2xx
chunk = data[start:start + 96 * 4]  # 384 bytes -> 3072 bits
bits = np.unpackbits(np.frombuffer(chunk, dtype=np.uint8)).reshape(24, 128)
rng = np.random.default_rng(7)
fig = plt.figure(figsize=(12, 4.2))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 128); ax.set_ylim(0, 24); ax.axis("off")
fig.patch.set_facecolor("#0f1a2b")
for r in range(24):
    for c in range(128):
        fade = 0.25 + 0.75 * (c / 127) ** 1.4
        if bits[r, c]:
            col = (0.24, 0.55, 0.92, fade)
        else:
            col = (0.24, 0.55, 0.92, 0.06 + 0.06 * fade)
        ax.add_patch(FancyBboxPatch((c + 0.12, 23 - r + 0.12), 0.76, 0.76, boxstyle="round,pad=0,rounding_size=0.18",
                                    linewidth=0, facecolor=col))
grad = np.linspace(1, 0, 256)[None, :] ** 1.6
ax.imshow(np.dstack([np.full((1, 256, 3), (15/255, 26/255, 43/255)), (0.88 * grad)[..., None]]),
          extent=(0, 128, 0, 24), aspect="auto", zorder=2, interpolation="bicubic")
text = "Every bit you can predict is a bit you don't have to store."
ax.text(2, 16.2, "1,000,000,000 bytes of Wikipedia → 155,874,783", color="white", fontsize=30, fontweight="semibold", family=fam, zorder=5)
ax.text(2, 12.6, "Predicted byte by byte by a 7 MB network of XORs, popcounts and SDOTs", color="#cfe0f7", fontsize=17, family=fam, zorder=5)
ax.text(2, 2.4, text, color="#9fb8da", fontsize=15, family=fam, style="italic", zorder=5)
fig.savefig(OUT / "hero.png", dpi=160, facecolor=fig.get_facecolor())
plt.close(fig)
print("wrote hero.png")

# ---------------------------------------------------------------- 7. Pareto frontier, before and after Jolt
def frontier(points):
    """points: list of (speed, bpb). Returns Pareto-optimal points sorted by speed (faster AND smaller wins)."""
    pts = sorted(points, key=lambda p: (-p[0], p[1]))
    out, best = [], float("inf")
    for s_, b_ in pts:                      # fastest first; keep a point only if it beats every faster one on size
        if b_ < best:
            out.append((s_, b_)); best = b_
    return sorted(out)

def steps(front, xmin):
    xs = [xmin] + [s_ for s_, _ in front]
    ys = [front[0][1]] + [b_ for _, b_ in front]
    return xs, ys

base_tools = ["cmix_dic", "cmix_nodic", "paq8px", "ppmd", "bzip2", "xz", "zstd"]
fig, axes = plt.subplots(1, 2, figsize=(13, 5.8), sharey=True)
for ax, key, title in [(axes[0], "encode", "Compress"), (axes[1], "decode", "Decompress")]:
    pts = {t: (get("dev1", t)[key]["kB_per_s"], get("dev1", t)["bpb"]) for t in base_tools + ["jolt1"]}
    old = frontier([pts[t] for t in base_tools])
    new = frontier(list(pts.values()))
    xmin, xmax = 0.5, 2e5
    def line(front, x):
        # straight segments between frontier points (linear in log-speed), undefined outside them
        fx = np.log10([s_ for s_, _ in front]); fy = [b_ for _, b_ in front]
        return np.where((np.log10(x) >= fx[0]) & (np.log10(x) <= fx[-1]), np.interp(np.log10(x), fx, fy), np.nan)
    def f(front, x):
        # best bpb among compressors at least this fast (used for the annotation)
        c = [b_ for s_, b_ in front if s_ >= x]
        return min(c) if c else np.nan
    grid_x = np.logspace(np.log10(min(p_[0] for p_ in old + new)), np.log10(max(p_[0] for p_ in old + new)), 2000)
    fo = line(old, grid_x); fn = line(new, grid_x)
    ax.fill_between(grid_x, fn, fo, where=fn < fo - 1e-9, color=BLUE, alpha=0.13, lw=0, zorder=1)
    ax.plot([s_ for s_, _ in old], [b_ for _, b_ in old], color=GRAY_D, lw=1.6, ls=(0, (4, 3)), zorder=2,
            label="Pareto frontier without Jolt")
    ax.plot([s_ for s_, _ in new], [b_ for _, b_ in new], color=BLUE, lw=2, zorder=2, label="Pareto frontier with Jolt")
    for t, (s_, b_) in pts.items():
        hero = t == "jolt1"
        on_old = (s_, b_) in old
        ax.scatter([s_], [b_], s=150 if hero else 60, color=BLUE if hero else (GRAY_D if on_old else GRAY),
                   edgecolor=SURF, linewidth=2, zorder=4)
    lab = {"cmix_dic": ("cmix + dict", (8, -14), "left"), "paq8px": ("paq8px", (8, 12), "left"),
           "jolt1": ("Jolt", (12, 12), "left"), "ppmd": ("PPMd", (8, 12), "left"),
           "cmix_nodic": ("cmix, no dict", (-8, 0), "right")}
    if key == "encode":
        lab.update({"bzip2": ("bzip2", (10, 0), "left"), "xz": ("xz", (-10, 0), "right"), "zstd": ("zstd", (-10, 0), "right")})
    else:
        lab.update({"bzip2": ("bzip2", (-10, 0), "right"), "xz": ("xz", (14, 2), "left"), "zstd": ("zstd", (0, -16), "center")})
    for t, (txt, off, h) in lab.items():
        s_, b_ = pts[t]
        ax.annotate(txt, (s_, b_), xytext=off, textcoords="offset points", ha=h, va="center",
                    fontsize=12 if t == "jolt1" else 10, color=INK if t == "jolt1" else INK2,
                    fontweight="semibold" if t == "jolt1" else "normal")
    ax.set_xscale("log"); ax.set_xlim(xmin, xmax)
    ax.set_xticks([1, 10, 100, 1000, 10000, 100000], ["1", "10", "100", "1k", "10k", "100k"])
    ax.set_ylim(2.45, 1.27)
    ax.set_xlabel(f"{title} speed, kB/s, one core (log scale)")
    ax.grid(True, color=GRID, linewidth=0.8); ax.set_axisbelow(True)
    ax.set_title(title, fontsize=13)
    gained = [(s_, b_) for s_, b_ in new if (s_, b_) not in old]
    # how much smaller at Jolt's speed than the best old option at least that fast
    sj, bj = pts["jolt1"]
    old_at = f(old, sj)
    note = (f"At Jolt's {sj:.0f} kB/s, the best\n"
            "file before was PPMd's.\n"
            f"Jolt's is {(1 - bj / old_at) * 100:.0f} % smaller.")
    ax.text(0.7, 1.80, note,
            va="center", ha="left", fontsize=10.5, color=BLUE)
axes[0].set_ylabel("Bits per byte (lower is better)")
axes[0].legend(loc="lower left", frameon=False, fontsize=10)
fig.suptitle("Jolt moves the speed/size Pareto frontier", x=0.06, ha="left", fontsize=15, fontweight="semibold")
footer(fig, "Held-out 1 MB of enwik9 (bytes 909M-910M), Apple M4 Pro, single core, all round trips byte-exact. A point is on the frontier if no other\n"
            "compressor is both faster and smaller. Shaded: the area the frontier gains with Jolt.")
save(fig, "pareto.png")
