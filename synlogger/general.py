#!/usr/bin/env python

####################
# Required Modules #
####################

# Generic/Built-in
import logging
import signal
import sys
import time
from multiprocessing import Process
from typing import Dict, List

# Lib


# Custom
from .base import RootLogger
from .config import (
    DIRECTOR_NAME_TEMPLATE, 
    TTP_NAME_TEMPLATE, 
    WORKER_NAME_TEMPLATE, 
    SYSMETRICS_NAME_TEMPLATE,
    SYSMETRICS_PORT, 
    DIRECTOR_PORT, 
    TTP_PORT, 
    WORKER_PORT
)
from .utils import StructlogUtils

##################
# Configurations #
##################


############################################
# Organisation Core Class - DirectorLogger #
############################################

class DirectorLogger(RootLogger):

    def __init__(
        self, 
        logger_name: str,
        logging_variant: str = "basic",
        server: str = None,
        port: int = None,
        logging_level: int = logging.INFO, 
        debugging_fields: bool = False,
        filter_functions: List[str] = [], 
        censor_keys: list = [],
        file_path: str = ""
    ):
        # General attributes
        # e.g. misc attibutes unique to problem


        # Network attributes
        # e.g. server IP and/or port number
        PORT = port if port else DIRECTOR_PORT 

        # Data attributes
        # e.g participant_id/run_id in specific format
        NODE_NAME = DIRECTOR_NAME_TEMPLATE.safe_substitute(name=logger_name)

        # Optimisation attributes
        # e.g multiprocess/asyncio if necessary for optimisation


        # Export Attributes 
        # e.g. any artifacts that are going to be exported eg Records
    

        super().__init__(
            server=server, 
            port=PORT, 
            logger_name=NODE_NAME, 
            logging_level=logging_level, 
            logging_variant=logging_variant, 
            debugging_fields=debugging_fields, 
            filter_functions=filter_functions, 
            censor_keys=censor_keys,
            file_path=file_path
        )



#######################################
# Organisation Core Class - TTPLogger #
#######################################

class TTPLogger(RootLogger):

    def __init__(
        self, 
        logger_name: str,
        logging_variant: str = "basic",
        server: str = None,
        port: int = None,
        logging_level: int = logging.INFO, 
        debugging_fields: bool = False,
        filter_functions: List[str] = [], 
        censor_keys: list = [],
        file_path: str = ""
    ):
        # General attributes
        # e.g. misc attibutes unique to problem


        # Network attributes
        # e.g. server IP and/or port number
        PORT = port if port else TTP_PORT 

        # Data attributes
        # e.g participant_id/run_id in specific format
        NODE_NAME = TTP_NAME_TEMPLATE.safe_substitute(name=logger_name)

        # Optimisation attributes
        # e.g multiprocess/asyncio if necessary for optimisation


        # Export Attributes 
        # e.g. any artifacts that are going to be exported eg Records
    

        super().__init__(
            server=server, 
            port=PORT, 
            logger_name=NODE_NAME, 
            logging_level=logging_level, 
            logging_variant=logging_variant, 
            debugging_fields=debugging_fields, 
            filter_functions=filter_functions, 
            censor_keys=censor_keys,
            file_path=file_path
        )



##########################################
# Organisation Core Class - WorkerLogger #
##########################################

class WorkerLogger(RootLogger):

    def __init__(
        self, 
        logger_name: str,
        logging_variant: str = "basic",
        server: str = None,
        port: int = None,
        logging_level: int = logging.INFO, 
        debugging_fields: bool = False,
        filter_functions: List[str] = [], 
        censor_keys: list = [],
        file_path: str = "",
    ):
        # General attributes
        # e.g. misc attibutes unique to problem


        # Network attributes
        # e.g. server IP and/or port number
        PORT = port if port else WORKER_PORT

        # Data attributes
        # e.g participant_id/run_id in specific format
        NODE_NAME = WORKER_NAME_TEMPLATE.safe_substitute(name=logger_name)

        # Optimisation attributes
        # e.g multiprocess/asyncio if necessary for optimisation


        # Export Attributes 
        # e.g. any artifacts that are going to be exported eg Records


        super().__init__(
            server=server, 
            port=PORT, 
            logger_name=NODE_NAME, 
            logging_level=logging_level, 
            logging_variant=logging_variant, 
            debugging_fields=debugging_fields, 
            filter_functions=filter_functions, 
            censor_keys=censor_keys,
            file_path=file_path
        )



#############################################
# Organisation Core Class - SysmetricLogger #
#############################################

class SysmetricLogger(RootLogger):
    """
    initialise configuration for setting up a logging server using structlog

    Attributes:
        file_path (str): Path to file storing logging messages (arbitrary Graylog arguments)
        server (str): Host address of the logging server e.g. 127.0.0.1 for Graylog
        port (int): Port of the logging server e.g. 9000 for graylog
        logging_level (int): logging.DEBUG, logging.INFO, logging.WARNING etc..
        logger_name (str): Logger ID by name e.g. TTP, worker_1, worker_2
        logging_variant: Type of logging to use. There are 2 main options:
            1. "default" -> basic logging, 
            2. "graylog" -> logging to graylog server
            Default: "default"
    """
    def __init__(
        self, 
        logger_name: str,
        logging_variant: str = "basic",
        server: str = None,
        port: int = None,
        logging_level: int = logging.INFO, 
        debugging_fields: bool = False,
        filter_functions: List[str] = [], 
        censor_keys: list = [],
        file_path: str = "",
    ):
        # General attributes
        # e.g. misc attibutes unique to problem


        # Network attributes
        # e.g. server IP and/or port number
        PORT = port if port else SYSMETRICS_PORT

        # Data attributes
        # e.g participant_id/run_id in specific format
        NODE_NAME = SYSMETRICS_NAME_TEMPLATE.safe_substitute(name=logger_name)

        # Optimisation attributes
        # e.g multiprocess/asyncio if necessary for optimisation
        self.tracker = None

        # Export Attributes 
        # e.g. any artifacts that are going to be exported eg Records
    

        super().__init__(
            server=server, 
            port=PORT, 
            logger_name=NODE_NAME, 
            logging_level=logging_level, 
            logging_variant=logging_variant, 
            debugging_fields=debugging_fields, 
            filter_functions=filter_functions, 
            censor_keys=censor_keys,
            file_path=file_path
        )

    ############    
    # Checkers #
    ############

    def is_tracking(self) -> bool:
        """ Checks if logger is currently tracking to enforce idempotence

        Returns:
            State (bool)
        """
        return self.tracker is not None

    ###########
    # Helpers #
    ###########

    def _configure_processors(self):
        """ Overrides parent's _configure_processors() to add in system
            tracking filters

        Args:
            censor_keys (list(callable)):
        Returns:
            Structlog Processes (list(callable))
        """
        structlog_utils = StructlogUtils(
            censor_keys=self.censor_keys, 
            file_path=self.file_path
        )

        track_cpu_stats = structlog_utils.track_cpu_stats
        track_memory_stats = structlog_utils.track_memory_stats
        track_disk_stats = structlog_utils.track_disk_stats
        track_network_stats = structlog_utils.track_network_stats

        ###########################
        # Implementation Footnote #
        ###########################

        # [Cause]
        # In Structlog, a processor is a callable object that executes a 
        # certain action upon a given event_dict input, and returns an 
        # augmented event_dict as output. As such, a Structlog processor chain
        # is formed and parsed in order and sequentially. 
        #  
        # eg.
        # wrapped_logger.msg(
        #     f4(
        #         wrapped_logger, "msg",
        #         f3(
        #             wrapped_logger, "msg",
        #             f2(
        #                 wrapped_logger, "msg",
        #                 f1(
        #                     wrapped_logger, "msg", 
        #                     {"event": "some_event", "x": 42, "y": 23}
        #                 )
        #             )
        #         )
        #     )
        # )
        #
        # More details on this can be found at:
        # https://www.structlog.org/en/stable/processors.html?highlight=chain

        # [Problems]
        # However, a custom processor handling PyGelf compatibility will
        # have an asymmetric output w.r.t other processors, and thus cannot be
        # used as inputs to a subsequent processor downstream. The generic
        # processors procured from the parent class terminates with such a 
        # process.

        # [Solution]
        # Ensure that generic processors procured from the parent class are
        # ALWAYS appended at the back of the processor list, ensuring that the
        # custom PyGelf processor is ALWAYS the final processor executed.

        generic_processors = super()._configure_processors()
        hardware_processors = [
            track_cpu_stats,
            track_memory_stats,
            track_disk_stats,
            track_network_stats
        ]
        all_processors = hardware_processors + generic_processors
        
        return all_processors


    def _exit(self, signnum: str, frame) -> None:
        """ Exit signal to terminate system tracking

        Args:
            signame (str): Signal recieved
        """
        signame = signal.Signals(signnum).name
        self.synlog.info(
            f"Signal {signame} of code {signnum} on {frame} has been received.",
            signame=signame,
            signnum=signnum
        )        

        # Zero is considered “successful termination” and any nonzero value is 
        # considered “abnormal termination” by shells and the like.
        self.synlog.info("Sysmetric operations stopped.")
        sys.exit(0)


    def _probe(
        self,
        resolution: int = 1,
        descriptors: Dict[str, str] = {},
    ) -> None:
        """ Polls and logs hardware statistics in the background at a specified
            regular interval. Current statistics supported include:
            1)  CPU load percentage
            2)  Memory total
            3)  Memory available
            4)  Memory used
            5)  Memory free
            6)  Disk read count
            7)  Disk write count
            8)  Disk read bytes
            9)  Disk write bytes
            10) Network bytes sent
            11) Network bytes receieved
            12) Network packets sent
            13) Network packets receieved

        Args:
            resolution (int): Polling interval in seconds. Default: 1
            descriptors (dict(str, str)): Localisation descriptors identifying
                the current running source code segment. Default: {}
        """
        self.synlog.info(
            "Probed system's hardware usage successfully.", 
            resolution=resolution,
            **descriptors
        )
        time.sleep(resolution)

    ##################
    # Core Functions #
    ##################

    def track(
        self,
        file_path: str,
        class_name: str, 
        function_name: str,
        resolution: int = 1,
        **kwargs
    ):
        """ Commences periodic polling and logging of hardware stats of the 
            current system.

        Args:
            component: Synergos component either TTP or Worker for the 
                HardwareStatsLogger, config.TTP or config.WORKER
            file_path: The location of the file path that call this function
        Returns:
            Process (subprocess.Popen object)
        """
        
        def target(descriptors: Dict[str, str]) -> None:
            """ Triggers periodic probe for hardware statistics, incorporating
                custom localisation descriptors into the logs

            Args:
                descriptors (dict(str, str)):
            """
            # Terminate process when one of the following signal is received
            DEFAULT_SIGNALS = ('SIGINT', 'SIGTERM')
            for signame in DEFAULT_SIGNALS:
                signal_code = getattr(signal, signame)
                signal.signal(signal_code, self._exit)

            while True:
                self._probe(resolution=resolution, descriptors=descriptors)

        if not self.is_tracking():
            self.initialise()
            
            descriptors = {
                "ID_path": file_path,
                "ID_class": class_name,
                "ID_function": function_name,
                **kwargs
            }

            self.tracker = Process(target=target, args=(descriptors,))
            self.tracker.daemon = True
            self.tracker.start()

        return self.tracker


    def terminate(self) -> int:
        """ Terminate the hardware monitoring process. An exit code is returned
            in accordance to the following rules:
            1) If previously tracking, return terminated process ID.
                a) if sucessful, exit_code == 0
                b) Otherwise, exit_code > 0
            2) Otherwise, return -42

        Returns:
            Exit code (int)
        """
        if not self.is_initialised():
            raise RuntimeError(f"Attempted to terminate logger {self.logger_name} before initialisation!")

        exit_code = -42

        if self.is_tracking():
            # Sending the SIGTERM signal to the child
            self.tracker.terminate()
            self.tracker.join()
            exit_code = self.tracker.exitcode

            # Reset state of tracker
            self.tracker.close()
            self.tracker = None

            self.synlog.info(f"Tracking terminated with exit code {exit_code}")

        else:
            self.synlog.warn(f"Attempted to terminate in non-tracking state. Command skipped.")

        return exit_code
