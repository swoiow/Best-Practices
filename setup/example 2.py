import os
import sys
from pathlib import Path

from Cython.Build import cythonize
from setuptools import Extension, find_packages, setup
from setuptools.command.build_ext import build_ext as _build_ext

from pytrade.tdx import __NAME__, __VERSION__


BASE_DIR = Path(__file__).resolve().parent
SKIP_FILES = {"__init__.py", "__main__.py", "setup.py"}

# 仅用于是否进入发布模式（此处不删除源码，由 CI 中的“strip 源码”步骤处理）
IS_RELEASE = "--release" in sys.argv
if IS_RELEASE:
    sys.argv.remove("--release")

# 收集需要 Cython 的 .py（跳过 __init__.py / __main__.py）
pkg_root = BASE_DIR / "pytrade"
py_sources = [
    p for p in pkg_root.rglob("*.py")
    if p.name not in SKIP_FILES
]


# =========================
# 自定义 build_ext
# =========================
class ReleaseBuild(_build_ext):
    def run(self):
        super().run()
        if IS_RELEASE:
            removed = 0
            for ext in ("*.py", "*.c"):
                for src_file in BASE_DIR.rglob(ext):
                    if any(part in {".venv", "venv"} for part in src_file.parts):  # 跳过虚拟环境目录
                        continue
                    if src_file.name not in SKIP_FILES:
                        src_file.unlink()
                        removed += 1
            print(f"[CLEAN] 已删除源码（发布模式），共 {removed} 个文件（保留 __init__.py/__main__.py/setup.py）")


# =========================
# 构建扩展模块列表
# =========================
extensions = []
for src in py_sources:
    rel = src.relative_to(BASE_DIR)  # 相对 setup.py
    mod_name = str(rel.with_suffix("")).replace(os.sep, ".")  # pytrade.xxx.yyy
    extensions.append(Extension(mod_name, [str(rel)]))  # 传相对路径，避免绝对路径报错

setup(
    name=__NAME__,
    version=".".join(map(str, __VERSION__)),
    description="ETL pipeline for TDX daily data (Cython protected)",
    author="HarmonSir",
    author_email="git@pylab.me",
    packages=find_packages(include=["pytrade", "pytrade.*"]),
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.10",
    install_requires=[
        "pandas",
        "polars",
        "requests",
        "tqdm",
    ],
    entry_points={
        "console_scripts": [
            "tdx-etl=pytrade.tdx.__main__:main",
        ],
    },
    ext_modules=cythonize(
        extensions,
        compiler_directives={"language_level": "3"},
        annotate=False,
    ),
    cmdclass={"build_ext": ReleaseBuild},
)
