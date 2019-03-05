# Tool to import data into budget data storage.

py_binary(
    name = "import_tool",
    srcs = glob(["*.py"]),
    deps = [
        "//moneyflow",
        "//third_party:appcommands",
        "@absl_git//absl/flags",
        "@tabulate_archive//:tabulate",
    ]
)
