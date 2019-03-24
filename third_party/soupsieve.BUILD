# Beautiful soup.

licenses(["notice"])  # MIT

exports_files(["LICENSE"])

py_library(
    name = "soupsieve",
    srcs = glob(["soupsieve/**/*.py"]),
    srcs_version = "PY2AND3",
    visibility = ["//visibility:public"],
    deps = [
        "@lru_cache_archive//:lru_cache",
    ],
)
