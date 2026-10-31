#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p docs/_build/html
# docs/index.md -> /index.html
sphinx-build -b html docs docs/_build/root -D master_doc=index
cp docs/_build/root/index.html docs/_build/html/index.html
# 各言語の独立したSphinxソースをビルド
for lang in en ja; do
  sphinx-build -b html -D language="$lang" docs/$lang docs/_build/html/$lang
done
touch docs/_build/html/.nojekyll
