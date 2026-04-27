import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Week 01 worker smoke entrypoint."
    )
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Run the worker smoke check.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if args.smoke:
        print("worker smoke pass")
        return 0

    print("Please run: python main.py --smoke")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
