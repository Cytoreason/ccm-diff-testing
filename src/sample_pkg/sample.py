"""Module providing a sample function"""
import fire
import pycytocc
from loguru import logger
from sample_pkg.utils.util import get_date
from pycytocc.client import create_task, post_tasks, wait_wf


class Sample:
    """simple class for running something"""

    def do_something(self, input1, input2='stam'):
        """
        :param input1:
        :param input2:
        :return: True or False
        """
        logger.debug(f"input1={input1}, input2={input2}")
        logger.info(get_date())
        return pycytocc.client.is_capsule_env()

    @staticmethod
    def run_something_on_cyto_cc(input1, input2='stam'):
        """
        :param input1:
        :param input2:
        :return: wf status
        :rtype: str
        """
        logger.debug(f"input1={input1}, input2={input2}")
        logger.info("Running cyto-cc task")
        my_task = create_task(command='ls -lh')
        wf = post_tasks([my_task], wait=False, force_execution=True)
        wf = wait_wf(wf['workflow_id'], wait_for_descendants=True, interval=69)
        return wf['status']


def run():
    fire.Fire(Sample)
