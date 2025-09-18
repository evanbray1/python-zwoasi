---
description: When working with Python packages that need to discover and load
  bundled native libraries
alwaysApply: false
---

When creating library discovery mechanisms for Python packages that bundle native libraries (.dll/.so/.dylib), always search the package directory first before falling back to system-wide search. Use platform-specific library naming conventions and check multiple common locations in this order: 1) Package lib/ directory, 2) System-wide search via find_library(), 3) Environment variables as fallback.