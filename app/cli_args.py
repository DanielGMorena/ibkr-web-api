import argparse


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments and return an argparse.Namespace object.
    The config attribute (args.config) will be a str or None.
    """
    parser = argparse.ArgumentParser(description="Start the IBKR Web API server")
    parser.add_argument(
        "--config",
        type=str,
        help="Path to the config.yml file",
        default=None,
    )

    args = parser.parse_args()

    if args.config is not None and not isinstance(args.config, str):
        raise TypeError(f"Expected --config to be a string, got {type(args.config)}")

    return args
