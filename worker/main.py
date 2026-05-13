import argparse
import json

try:
    from .image_layout_pipeline import process_image_layout_job
    from .layout_validator import configure_output_encoding
except ImportError:
    from image_layout_pipeline import process_image_layout_job
    from layout_validator import configure_output_encoding


def str_to_bool(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"true", "1", "yes", "y"}:
        return True
    if normalized in {"false", "0", "no", "n"}:
        return False
    raise argparse.ArgumentTypeError("fallback must be true or false")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Worker entrypoint for smoke checks and real image layout jobs."
    )
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Run the worker smoke check.",
    )
    parser.add_argument("--job-id", help="Worker job id for real image processing.")
    parser.add_argument("--image-path", help="Path to the real image file.")
    parser.add_argument(
        "--mode",
        choices=["real-ai", "fallback-only"],
        help="Worker execution mode.",
    )
    parser.add_argument(
        "--fallback",
        type=str_to_bool,
        default=True,
        help="Whether fallback is allowed when real-ai mode fails. Use true or false.",
    )
    args = parser.parse_args()

    if args.smoke:
        return args

    missing = [
        flag
        for flag, value in {
            "--job-id": args.job_id,
            "--image-path": args.image_path,
            "--mode": args.mode,
        }.items()
        if not value
    ]
    if missing:
        parser.error("missing required arguments for real worker mode: " + ", ".join(missing))
    return args


def main():
    configure_output_encoding()
    args = parse_args()

    if args.smoke:
        print("worker smoke pass")
        return 0

    result, exit_code = process_image_layout_job(
        job_id=args.job_id,
        image_path=args.image_path,
        mode=args.mode,
        fallback=args.fallback,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
