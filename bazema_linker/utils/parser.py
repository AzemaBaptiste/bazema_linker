"""
Argument parser
"""
import argparse


def create_parser():
    """
    Parser
    :return: argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input_dir',
        help='Folder of file reception',
        required=True
    )
    parser.add_argument(
        '-o', '--output_dir',
        help='Path to output directory',
        required=True
    )
    return parser


def parse_args(args):
    """
    Parse arguments
    :param args: raw args
    :return: Parsed arguments
    """
    parser = create_parser()
    return parser.parse_args(args=args)
