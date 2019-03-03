# ofxparse deserializes Open Financial Exchange files.

licenses(["notice"])  # BSD

exports_files(["LICENSE"])

py_library(
    name = "ofxparse",
    srcs = glob(["ofxparse/*.py", "utils/*.py"]),
    srcs_version = "PY2AND3",
    visibility = ["//visibility:public"],
    deps = [
        "@beautiful_soup_archive//:bs4",
    ],
)
