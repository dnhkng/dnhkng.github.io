# David Noel Ng

Source for [dnhkng.github.io](https://dnhkng.github.io), my personal site and long-form technical notebook.

This is where I write about systems that are interesting because they are hard to optimize: LLM internals, homebrew AI hardware, inference memory paths, biotech, game theory, coordination problems, and the occasional piece of high-effort nonsense that turns into a real experiment.

The site runs on [Jekyll](https://jekyllrb.com/) using the [Chirpy](https://github.com/cotes2020/jekyll-theme-chirpy) theme, which is objectively a good choice because it gives me tags, categories, archives, dark mode, syntax highlighting, math, and a clean reading experience without requiring me to become a frontend framework person. Cool AF, frankly.

## What Is Here

A few representative threads:

- **LLM Neuroanatomy**: experiments around transformer layer structure, RYS layer duplication, and the idea that middle layers act like a language-agnostic reasoning region.
- **Local AI hardware**: GH200 memory-path benchmarking, Jetson Orin NX Hermes Agent tuning, vLLM deployment notes, and the practical ugliness of making large models actually serve tokens.
- **Model behavior and representation**: multilingual semantic spaces, Sapir-Whorf-ish questions in transformers, leaderboard experiments, and why benchmark gains sometimes come from weird places.
- **Systems thinking**: game theory, coordination, economics, automation, and attempts to reason about very large systems without pretending they are simple.

The writing style is part lab notebook, part build log, part argument. The goal is to show the work: measurements, failed assumptions, hardware constraints, and the reasoning that led to the final shape.

## Repo Layout

```text
_posts/       Published posts
_drafts/      Draft posts and working notes
_tabs/        Chirpy sidebar pages
_data/        Site metadata and social/share config
assets/       Images, widgets, and interactive assets
tools/        Local build and test helper scripts
```

Important config lives in [_config.yml](_config.yml). The site title, tagline, author metadata, Chirpy settings, pagination, permalinks, and PWA behavior are all there.

## Local Development

Install Ruby dependencies:

```bash
bundle install
```

Run the site locally:

```bash
bash tools/run.sh
```

By default this serves on `127.0.0.1` with live reload. To bind another host:

```bash
bash tools/run.sh --host 0.0.0.0
```

Build and run the local HTML checks:

```bash
bash tools/test.sh
```

The test script builds the site in production mode and runs `html-proofer` with external links disabled.

## Writing Notes

Posts are Markdown files in `_posts/` using standard Jekyll front matter. Most technical posts use some mix of:

- tables for benchmark results
- fenced code blocks for commands
- local images under `assets/img/`
- math rendering where needed
- embedded HTML widgets for interactive explanations

Chirpy handles the reading furniture: table of contents, tags, categories, archives, post metadata, and the general blog shell. The content is the point; the theme stays out of the way.

## License

The site scaffolding is based on Chirpy and Jekyll. Original writing, images, diagrams, benchmark results, and project notes in this repository are mine unless otherwise stated.

See [LICENSE](LICENSE) for the repository license.
