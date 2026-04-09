import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(12, 8))
ax.set_xlim(0, 12)
ax.set_ylim(0, 8)
ax.axis("off")
fig.patch.set_facecolor("#1e1e2e")

def box(ax, x, y, w, h, label, sublabel="", color="#4a90d9"):
    rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                          facecolor=color, edgecolor="white", linewidth=1.5)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2 + (0.15 if sublabel else 0), label,
            ha="center", va="center", fontsize=10, fontweight="bold", color="white")
    if sublabel:
        ax.text(x + w/2, y + h/2 - 0.25, sublabel,
                ha="center", va="center", fontsize=7.5, color="#cccccc")

def arrow(ax, x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color="white", lw=1.5))

# title
ax.text(6, 7.5, "Game Glitch Investigator — System Architecture",
        ha="center", va="center", fontsize=13, fontweight="bold", color="white")

# user
box(ax, 0.5, 5.5, 2, 0.9, "👤 User", "Bug description / query", "#6c8ebf")

# streamlit ui
box(ax, 0.5, 3.5, 2, 1.2, "🖥️ Streamlit UI", "3 tabs: Game /\nLookup / Evaluator", "#5a9e6f")

# retriever
box(ax, 4, 5.0, 2.5, 1.0, "🔍 retriever.py", "Keyword scoring\n(set intersection)", "#d97b4a")

# knowledge base
box(ax, 4, 3.0, 2.5, 1.5, "📚 Knowledge Base", "bug_patterns/\nerror_types/\n6 markdown files", "#9b59b6")

# reliability evaluator
box(ax, 8, 5.0, 2.8, 1.0, "🧪 Reliability Evaluator", "7 automated tests\ngame logic + retriever", "#c0392b")

# game logic
box(ax, 8, 3.0, 2.8, 1.5, "🎮 logic_utils.py", "check_guess()\nparse_guess()\nupdate_score()", "#2980b9")

# output
box(ax, 3.5, 0.8, 5, 0.9, "📄 Results Displayed to User", "Matched docs / Test results / Game feedback", "#5a9e6f")

# arrows
arrow(ax, 2.5, 6.0, 4.0, 5.5)       # user -> retriever
arrow(ax, 1.5, 5.5, 1.5, 4.7)       # user -> streamlit
arrow(ax, 2.5, 4.1, 4.0, 4.5)       # streamlit -> knowledge base
arrow(ax, 4.0, 5.5, 2.5, 4.5)       # retriever -> streamlit
arrow(ax, 5.0, 5.0, 5.0, 4.5)       # retriever -> knowledge base
arrow(ax, 2.5, 3.8, 8.0, 5.2)       # streamlit -> evaluator
arrow(ax, 2.5, 3.6, 8.0, 3.8)       # streamlit -> logic_utils
arrow(ax, 6.5, 4.0, 8.0, 4.0)       # knowledge base -> logic_utils (eval uses both)
arrow(ax, 6.0, 3.5, 6.0, 1.7)       # knowledge base -> output
arrow(ax, 9.4, 3.0, 7.5, 1.7)       # logic_utils -> output
arrow(ax, 9.4, 5.0, 7.5, 1.7)       # evaluator -> output

plt.tight_layout()
plt.savefig("assets/architecture.png", dpi=150, bbox_inches="tight",
            facecolor=fig.get_facecolor())
print("saved to assets/architecture.png")
