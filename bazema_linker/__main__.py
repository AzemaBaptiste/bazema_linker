"""Entry point"""
import sys

from bazema_linker.linker import Linker
from bazema_linker.utils.parser import parse_args


def main():
    """main"""
    args = parse_args(args=sys.argv[1:])
    Linker(data_folder=args.input_dir, output_folder=args.output_dir).main()


if __name__ == '__main__':
    main()
