#!/usr/bin/env bash
echo "########################################################"
echo "# AUDIT REPORT — $(date)"
echo "########################################################"

echo ""
echo "===== 1. ENVIRONMENT ====="
echo "PWD: $(pwd)"
echo "OS : $(uname -a)"

echo ""
echo "===== 2. STRUKTUR FOLDER (depth 3) ====="
find . -maxdepth 3 -type d \
  -not -path '*/node_modules*' \
  -not -path '*/.git*' \
  -not -path '*/venv*' \
  -not -path '*/.venv*' \
  -not -path '*/__pycache__*' \
  -not -path '*/.cache*' | sort

echo ""
echo "===== 3. DAFTAR FILE + UKURAN ====="
find . -maxdepth 4 -type f \
  -not -path '*/node_modules/*' \
  -not -path '*/.git/*' \
  -not -path '*/venv/*' \
  -not -path '*/.venv/*' \
  -not -path '*/__pycache__/*' \
  -not -path '*/.cache/*' \
  2>/dev/null | sort | while read f; do
  sz=$(wc -c < "$f" 2>/dev/null)
  printf "%8s B  %s\n" "$sz" "$f"
done

echo ""
echo "===== 4. LINE COUNT per FILE ====="
find . -type f \( \
    -name "*.py" -o -name "*.js" -o -name "*.ts" -o \
    -name "*.jsx" -o -name "*.tsx" -o -name "*.mjs" -o \
    -name "*.sh" -o -name "*.json" -o -name "*.md" -o \
    -name "*.yml" -o -name "*.yaml" -o -name "*.txt" -o \
    -name "*.toml" -o -name "*.ini" -o -name "*.env*" \
  \) \
  -not -path '*/node_modules/*' \
  -not -path '*/.git/*' \
  -not -path '*/venv/*' \
  -not -path '*/.venv/*' \
  -not -path '*/__pycache__/*' \
  -exec wc -l {} \; 2>/dev/null | sort -n

echo ""
echo "===== 5. ROOT LISTING (termasuk hidden) ====="
ls -la

echo ""
echo "===== 6. PACKAGE / DEPENDENCY FILES ====="
for f in package.json requirements.txt pyproject.toml Pipfile setup.py setup.cfg composer.json Gemfile go.mod Cargo.toml; do
  [ -f "$f" ] && { echo "--- $f ---"; cat "$f"; echo; }
done

echo ""
echo "===== 7. README / DOCS ====="
for f in README.md README.txt readme.md README; do
  [ -f "$f" ] && { echo "--- $f (100 baris pertama) ---"; head -100 "$f"; echo; break; }
done
echo "--- docs/ ---"
ls -la docs/ 2>/dev/null || echo "(tidak ada folder docs)"

echo ""
echo "===== 8. GIT INFO ====="
if [ -d .git ]; then
  echo "--- branch ---"; git branch -a 2>/dev/null
  echo "--- recent commits ---"; git log --oneline -15 2>/dev/null
  echo "--- status ---"; git status -s 2>/dev/null
else
  echo "(bukan git repo)"
fi

echo ""
echo "===== 9. TOTAL ====="
echo -n "Total file (exclude vendor): "
find . -type f -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/venv/*' -not -path '*/.venv/*' -not -path '*/__pycache__/*' 2>/dev/null | wc -l
echo -n "Total baris kode (source): "
find . -type f \( -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.jsx" -o -name "*.tsx" \) -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/venv/*' -not -path '*/.venv/*' -not -path '*/__pycache__/*' -exec cat {} \; 2>/dev/null | wc -l

echo ""
echo "===== SELESAI ====="
