# oxidizer.bzl
# PyOxidizer configuration file

python_binary(
    name = "generated_script",
    main_module = "generated_script",
    python_version = "3.1",
    sources = glob(["*generated_script.py"]),
    deps = [
        "@pip//:requests",
        # Add any other dependencies your application requires
    ],
)