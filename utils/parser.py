import argparse

def default_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, required=True)
    return parser