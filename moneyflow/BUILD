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
        "@ofxparse_git//:ofxparse",
    ],
)

py_library(
    name = "test_utils",
    srcs = ["test_utils.py"],
)

py_test(
    name = "storage_lib_test",
    srcs = ["storage_lib_test.py"],
    # This should be PY3 compatible, but absl throws an error: no module named
    # enum.
    python_version = "PY2",
    data = ["testdata/test_read.csv"],
    deps = [
        ":moneyflow",
        "@absl_git//absl/flags",
        "@absl_git//absl/testing:absltest",
        "@mock_archive//:mock",
    ],
)

py_test(
    name = "accounts_lib_test",
    srcs = ["accounts_lib_test.py"],
    # This should be PY3 compatible, but absl throws an error: no module named
    # enum.
    python_version = "PY2",
    deps = [
        ":moneyflow",
        "@absl_git//absl/testing:absltest",
        "@mock_archive//:mock",
    ],
)

py_test(
    name = "transactions_lib_test",
    srcs = ["transactions_lib_test.py"],
    # This should be PY3 compatible, but absl throws an error: no module named
    # enum.
    python_version = "PY2",
    data = ["testdata/test_import.ofx"],
    deps = [
        ":moneyflow",
        ":test_utils",
        "@absl_git//absl/testing:absltest",
        "@mock_archive//:mock",
    ],
)

py_test(
    name = "categories_lib_test",
    srcs = ["categories_lib_test.py"],
    # This should be PY3 compatible, but absl throws an error: no module named
    # enum.
    python_version = "PY2",
    deps = [
        ":moneyflow",
        "@absl_git//absl/testing:absltest",
        "@mock_archive//:mock",
    ],
)

py_test(
    name = "ui_utils_test",
    srcs = ["ui_utils_test.py"],
    # This should be PY3 compatible, but absl throws an error: no module named
    # enum.
    python_version = "PY2",
    deps = [
        ":moneyflow",
        "@absl_git//absl/testing:absltest",
        "@mock_archive//:mock",
    ],
)
