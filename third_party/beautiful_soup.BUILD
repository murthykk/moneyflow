# Beautiful soup.

licenses(["notice"])  # MIT

exports_files(["LICENSE"])

py_library(
    name = "bs4",
    srcs = glob(["bs4/*.py", "bs4/builder/*.py"]),
    srcs_version = "PY2AND3",
    visibility = ["//visibility:public"],
    deps = [
        "@soupsieve_archive//:soupsieve",
    ],
)
