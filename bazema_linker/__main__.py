"""Entry point"""
import sys
from datetime import datetime

from bazema_linker.process import Process
from bazema_linker.utils.logging import get_logger
from bazema_linker.utils.parser import parse_args


def main():
    """Run main"""

    logger = get_logger(__name__)
    logger.info('Bazema_linker start...')
    start_time = datetime.now()

    args = parse_args(args=sys.argv[1:])
    Process(data_folder=args.input_dir, output_folder=args.output_dir).run_process()

    # End
    now = datetime.now()
    time_run = (now - start_time).total_seconds()
    logger.info('Processing time: {} seconds'.format(time_run))
    logger.info('Bazema_linker end.')


if __name__ == '__main__':
    main()
