# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-05-02

### Changed
- **BREAKING**: Migrated from Pydantic V1 to **Pydantic V2** for up to 10x faster response parsing (V2 core is written in Rust).
  - Replaced deprecated `parse_obj_as()` with `TypeAdapter().validate_python()` in `api.py`.
  - Replaced deprecated `.dict()` with `.model_dump()` in `utils.py`.
  - Replaced deprecated `.json()` with `.model_dump_json()` in `utils.py`.
  - Replaced `update_forward_refs()` with `model_rebuild()` in `node.py`.
  - Added default `= None` values to all `Optional` fields across all models as required by Pydantic V2.
  - Converted absolute model imports to relative imports in `page.py` and `uploaded_file.py`.
- Added Python 3.13 and 3.14 to the supported classifiers in `pyproject.toml` and `setup.py`.

## [1.1.4] - 2026-05-02

### Added

- **Native DPI Bypass**: `telegraph-next` now connects directly to the Telegram server IPs (`149.154.164.13`) to bypass DNS/SNI blocking by ISPs, enabling reliable Telegraph API usage without requiring a local proxy or Tor.
- **Catbox.moe Fallback Integration**: Because Telegraph's native `/upload` server is globally unstable and often rejects uploads with "Unknown error", the `upload_file()` method now natively uses the highly reliable `catbox.moe` API to upload files. It returns an `UploadedFile` with a full Catbox URL instead of a relative path.

### Changed

- **CRITICAL**: Renamed internal package from `telegraph` to `telegraph_next` to resolve naming conflicts with the official `telegraph` library. This ensures drop-in replacement without shadowing issues.
- Converted all internal absolute imports to relative imports to prevent `ModuleNotFoundError` during installation.

### Fixed

- Added `telegraph_next.models` to `packages` in `pyproject.toml` to ensure all submodules are correctly included in the build.
- Fixed `Unknown error` in `upload_file` by explicitly using `aiohttp.FormData` to enforce strict `multipart/form-data` formatting.
- Updated examples in `README.md` to use the correct `Abbasxan` author name.

## [1.1.3] - 2026-05-02

### Changed

- Updated metadata to reflect Abbasxan as the sole author and owner of the fork.

## [1.1.2] - 2026-05-02

### Added

- Created modern, premium `README.md` with complete usage examples.
- Added GitHub Actions workflow for PyPI publishing.
- Support for `bs4` alias in dependencies for backward compatibility.

### Fixed

- Fixed `AttributeError` caused by incorrect dictionary iteration during HTML attribute removal in middlewares.
- Fixed YouTube iframe parsing logic.
- Fixed memory leaks in `upload_file` by ensuring file streams are properly closed in a `finally` block.
- Restored missing `BeautifulSoup` imports.

### Changed

- Complete project rebranding to `telegraph-next`.
- Migrated core dependencies to `aiohttp` and `pydantic`.
