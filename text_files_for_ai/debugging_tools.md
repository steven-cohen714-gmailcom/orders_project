# 🛠 Debugging & Dependency Analysis Toolkit

This document lists tools you can use to debug, trace, and analyze your JavaScript and Python project dependencies, performance, and dead code.

---

## 🧠 1. Import/Dependency Tracing

| Tool | Language | Description |
|------|----------|-------------|
| `trace_js_imports.py` | JS | Traces internal module imports for frontend logic (used in `new_order_main.js`) |
| [madge](https://github.com/pahen/madge) | JS | Visual dependency graph, detects circular deps |
| [pydeps](https://github.com/thebjorn/pydeps) | Python | Import tree visualizer for Python modules |
| [modulefinder](https://docs.python.org/3/library/modulefinder.html) | Python | Standard tool to detect module usage |
| [pipdeptree](https://github.com/naiquevin/pipdeptree) | Python | Dependency tree of pip-installed packages |

---

## 🔄 2. Circular Dependency & Unused Code Detection

| Tool | Language | Description |
|------|----------|-------------|
| `madge --circular` | JS | Detects circular module imports |
| [depcheck](https://www.npmjs.com/package/depcheck) | JS | Finds unused npm packages and file-level imports |
| [vulture](https://github.com/jendrikseipp/vulture) | Python | Finds unused functions, variables, imports |
| [coverage.py](https://coverage.readthedocs.io/) | Python | Measures test coverage and flags untested code |

---

## 🔥 3. Runtime Debugging / Profiling

| Tool | Language | Description |
|------|----------|-------------|
| Chrome DevTools | JS | Inspect live JS behavior, network, console, call stack |
| [py-spy](https://github.com/benfred/py-spy) | Python | Profiling without modifying code (flame graphs) |
| [loguru](https://github.com/Delgan/loguru) | Python | Simpler, more powerful logging than `logging` |
| [trace](https://docs.python.org/3/library/trace.html) | Python | Traces program line-by-line during execution |

---

## 🧪 4. Testing & Linting

| Tool | Language | Description |
|------|----------|-------------|
| `pytest` | Python | Popular test runner, plugin-rich |
| `flake8`, `black`, `ruff` | Python | Linting, formatting, code cleanup |
| `eslint`, `prettier` | JS | JS linting and formatting |
| `jest` | JS | Unit and integration testing for frontend |

---

## 🌐 5. Static Analysis & Graphing

| Tool | Language | Description |
|------|----------|-------------|
| [SourceTrail](https://github.com/CoatiSoftware/Sourcetrail) | Python/JS | Graphical dependency viewer, function & class mapping |
| `graphviz` | All | Used by many tools to render .png/.svg import graphs |
| `pylint --generate-rcfile` | Python | Deep static code inspection and rule generation |

---

## 📦 6. Asset/Bundling & Browser Dependency Analysis

| Tool | Language | Description |
|------|----------|-------------|
| `webpack-bundle-analyzer` | JS | Inspect final browser bundle contents |
| Chrome DevTools → Sources tab | JS | View JS/CSS file load dependencies |
| Chrome DevTools → Network tab | JS | Shows all static assets loaded at runtime |

---

> 📝 Last updated by ChatGPT on request from Steven. Tailored to Universal Recycling's order system debugging needs.
