py_library(
    name = "moneyflow",
    srcs = [
        "accounts_lib.py",
        "categories_lib.py",
        "storage_lib.py",
        "transactions_lib.py",
        "ui_utils.py",
    ],
    srcs_version = "PY2AND3",
    deps = [
        "@absl_git//absl/flags",
        "@tabulate_archive//:tabulate",
    ],
)

py_test(
    name = "storage_lib_test",
    srcs = ["storage_lib_test.py"],
    python_version = "PY2",
    deps = [
        ":moneyflow",
        "@absl_git//absl/flags",
        "@absl_git//absl/testing:absltest",
        "@mock_archive//:mock",
    ],
)
