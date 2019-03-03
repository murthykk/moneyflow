# Bazel workspace file. Contains references to dependencies for this repo.
workspace(name = "moneyflow")

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository", "new_git_repository")

git_repository(
    name = "absl_git",
    remote = "https://github.com/abseil/abseil-py.git",
    tag = "pypi-v0.7.0",
)

http_archive(
    name = "tabulate_archive",
    urls = [
        "https://files.pythonhosted.org/packages/c2/fd/202954b3f0eb896c53b7b6f07390851b1fd2ca84aa95880d7ae4f434c4ac/tabulate-0.8.3.tar.gz",
    ],
    sha256 = "8af07a39377cee1103a5c8b3330a421c2d99b9141e9cc5ddd2e3263fea416943",
    strip_prefix = "tabulate-0.8.3",
    build_file = "@//third_party:tabulate.BUILD",
)

http_archive(
    name = "beautiful_soup_archive",
    urls = [
        "https://files.pythonhosted.org/packages/80/f2/f6aca7f1b209bb9a7ef069d68813b091c8c3620642b568dac4eb0e507748/beautifulsoup4-4.7.1.tar.gz"
    ],
    sha256 = "945065979fb8529dd2f37dbb58f00b661bdbcbebf954f93b32fdf5263ef35348",
    strip_prefix = "beautifulsoup4-4.7.1",
    build_file = "@//third_party:beautiful_soup.BUILD",
)

new_git_repository(
    name = "ofxparse_git",
    remote = "https://github.com/jseutter/ofxparse.git",
    tag = "0.20",
    build_file = "@//third_party:ofxparse.BUILD",
)

# The following are defined in absl-py's WORKSPACE file, but for some reason,
# Bazel doesn't fetch them. So, clone them here.
http_archive(
    name = "six_archive",
    urls = [
        "http://mirror.bazel.build/pypi.python.org/packages/source/s/six/six-1.10.0.tar.gz",
        "https://pypi.python.org/packages/source/s/six/six-1.10.0.tar.gz",
    ],
    sha256 = "105f8d68616f8248e24bf0e9372ef04d3cc10104f1980f54d57b2ce73a5ad56a",
    strip_prefix = "six-1.10.0",
    build_file = "@//third_party:six.BUILD",
)

http_archive(
    name = "mock_archive",
    urls = [
        "http://mirror.bazel.build/pypi.python.org/packages/a2/52/7edcd94f0afb721a2d559a5b9aae8af4f8f2c79bc63fdbe8a8a6c9b23bbe/mock-1.0.1.tar.gz",
        "https://pypi.python.org/packages/a2/52/7edcd94f0afb721a2d559a5b9aae8af4f8f2c79bc63fdbe8a8a6c9b23bbe/mock-1.0.1.tar.gz",
    ],
    sha256 = "b839dd2d9c117c701430c149956918a423a9863b48b09c90e30a6013e7d2f44f",
    strip_prefix = "mock-1.0.1",
    build_file = "@//third_party:mock.BUILD",
)

http_archive(
    # NOTE: The name here is used in _enum_module.py to find the sys.path entry.
    name = "enum34_archive",
    urls = [
        "https://mirror.bazel.build/pypi.python.org/packages/bf/3e/31d502c25302814a7c2f1d3959d2a3b3f78e509002ba91aea64993936876/enum34-1.1.6.tar.gz",
        "https://pypi.python.org/packages/bf/3e/31d502c25302814a7c2f1d3959d2a3b3f78e509002ba91aea64993936876/enum34-1.1.6.tar.gz"
        ],
    sha256 = "8ad8c4783bf61ded74527bffb48ed9b54166685e4230386a9ed9b1279e2df5b1",
    build_file = "@//third_party:enum34.BUILD"
)
