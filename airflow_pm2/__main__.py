import argparse
from . import pid, start, restart, stop, reload


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        help="command",
        default="",
        choices=("pid", "start", "restart", "stop", "reload"),
    )

    parser.add_argument("path", help="path")

    args = parser.parse_args()

    print(
        {
            "pid": pid,
            "start": start,
            "restart": restart,
            "stop": stop,
            "reload": reload,
        }
        .get(args.command)(args.path)
        .decode("ascii")
    )
