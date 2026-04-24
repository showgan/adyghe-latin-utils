# How to Publish adyghe-latin-utils to PyPI

## 1. Update the Version Number

Bump the version in **both** files:

- `pyproject.toml` → `version = "X.Y.Z"`
- `src/adyghe_latin_utils/__init__.py` → `__version__ = "X.Y.Z"`

Follow [semantic versioning](https://semver.org/):
- **Patch** (0.1.0 → 0.1.1): bug fixes, documentation changes
- **Minor** (0.1.0 → 0.2.0): new features, backward-compatible
- **Major** (0.1.0 → 1.0.0): breaking changes

## 2. Delete Old Build Artifacts

```bash
rm dist/*
```

This removes previously built `.tar.gz` and `.whl` files. If you skip this,
`uv publish` will try to upload all files in `dist/`, including old versions
that may already exist on PyPI (causing a 400 error).

## 3. Build the Package

```bash
uv build
```

This creates two files in `dist/`:
- `adyghe_latin_utils-X.Y.Z.tar.gz` (source distribution)
- `adyghe_latin_utils-X.Y.Z-py3-none-any.whl` (wheel)

## 4. Run Tests Before Publishing

```bash
uv run pytest tests/ -v
```

Make sure all tests pass before publishing.

## 5. Commit and Push

```bash
git add -A
git commit -m "Bump version to X.Y.Z"
git push
```

## 6. Publish to TestPyPI (Recommended First)

```bash
uv publish --publish-url https://test.pypi.org/legacy/
```

When prompted:
- **Username**: `__token__`
- **Password**: your TestPyPI API token (starts with `pypi-`)

To create a TestPyPI token: https://test.pypi.org/manage/account/#api-tokens

### Verify on TestPyPI

Visit: https://test.pypi.org/project/adyghe-latin-utils/

### Test-install from TestPyPI

Create a temporary venv to test the package in isolation:

```bash
uv venv /tmp/test-adyghe --python 3.10
source /tmp/test-adyghe/bin/activate        # bash/zsh
# source /tmp/test-adyghe/bin/activate.csh  # tcsh
uv pip install --index-url https://test.pypi.org/simple/ adyghe-latin-utils
```

Then verify it works:

```bash
python -c "from adyghe_latin_utils import AdigaCharacterUtils, AdigaNumberUtils; print('OK')"
adyghe-char-convert --help
adyghe-num-convert --help
```

Uninstall after testing:

```bash
deactivate
rm -rf /tmp/test-adyghe
```

## 7. Publish to PyPI (Production)

```bash
uv publish
```

When prompted:
- **Username**: `__token__`
- **Password**: your PyPI API token (starts with `pypi-`)

To create a PyPI token: https://pypi.org/manage/account/#api-tokens

### Verify on PyPI

Visit: https://pypi.org/project/adyghe-latin-utils/

### Test-install from PyPI

Create a temporary venv to test the package in isolation:

```bash
uv venv /tmp/test-adyghe --python 3.10
source /tmp/test-adyghe/bin/activate        # bash/zsh
# source /tmp/test-adyghe/bin/activate.csh  # tcsh
uv pip install adyghe-latin-utils
```

Then verify:

```bash
python -c "from adyghe_latin_utils import AdigaCharacterUtils, AdigaNumberUtils; print('OK')"
adyghe-char-convert --help
adyghe-num-convert -t "42"
```

Clean up:

```bash
deactivate
rm -rf /tmp/test-adyghe
```

## 8. Tag the Release on GitHub

Once the package is live on PyPI, tag the release commit and push the tag so
GitHub has a permanent marker for the published version. Use an annotated tag
with a `vX.Y.Z` name matching `pyproject.toml` / `__version__`:

```bash
git tag -a vX.Y.Z -m "Release X.Y.Z"
git push origin vX.Y.Z
```

If you ever need to remove a tag that was pushed by mistake:

```bash
git tag -d vX.Y.Z                      # delete locally
git push origin :refs/tags/vX.Y.Z      # delete on GitHub
```

## Quick Reference (Copy-Paste)

Full publish workflow in one block:

```bash
# 1. Edit version in pyproject.toml and src/adyghe_latin_utils/__init__.py
# 2. Then run:
rm dist/*
uv build
uv run pytest tests/ -v
git add -A && git commit -m "Bump version to X.Y.Z" && git push
uv publish --publish-url https://test.pypi.org/legacy/   # TestPyPI
uv publish                                                 # PyPI
git tag -a vX.Y.Z -m "Release X.Y.Z" && git push origin vX.Y.Z
```
