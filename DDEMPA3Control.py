"""
DDEMPA3Control - A Python wrapper for MPA3 data acquisition software via DDE.

Authorship:
    Original code: Ange A. Maurice / CMAM
    AI-assisted improvements: Le Chat (Mistral AI)
    - Added logging, comments, and error handling.
    - Refactored for clarity and maintainability.

Disclaimer:
    This code was polished and enhanced with the assistance of AI (Le Chat by Mistral AI).
    While the AI provided suggestions for improvements, the original logic and functionality
    were authored by Ange Maurice. The AI's role was limited to:
    - Adding comments and docstrings.
    - Implementing logging and error handling.
    - Suggesting structural improvements.

    Users of this code are responsible for validating its correctness and suitability
    for their specific use case. No warranty or liability is provided.
"""

import win32ui
import dde
import logging
from datetime import datetime

# Configure logging to include timestamps and write to both file and console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("mpa3_dde.log"),  # Log to file
        logging.StreamHandler()               # Log to console
    ]
)

class DDEMPA3Control:
    """A Python wrapper for controlling MPA3 data acquisition software via DDE.

    This class provides methods to interact with the MPA3 software, including
    starting/stopping data acquisition, retrieving data, and configuring settings.
    Uses the legacy DDE (Dynamic Data Exchange) protocol for communication.
    """

    def __init__(self):
        """Initialize the DDE client and server handles."""
        self.c = None      # DDE conversation handle
        self.server = None # DDE server handle
        self.logger = logging.getLogger("DDEMPA3Control")
        self.logger.info("DDEMPA3Control instance initialized")

    def connect(self) -> bool:
        """Connect to the MPA3 DDE server.

        Returns:
            bool: True if connection succeeded, False otherwise.
        """
        try:
            self.logger.info("Attempting to connect to MPA3 DDE server...")
            self.server = dde.CreateServer()
            self.server.Create("MPA3")
            self.c = dde.CreateConversation(self.server)
            self.c.ConnectTo("MPA3", "MPA3-")

            if self.c.Connected() == 1:
                self.logger.info("Successfully connected to MPA3 DDE server")
                return True
            else:
                self.logger.error("Failed to connect to MPA3 DDE server, Is MPA3 running?")
                return False
        except Exception as e:
            self.logger.error(f"Connection error: {e}")
            return False

    def close(self) -> None:
        """Close the DDE connection and clean up resources."""
        if self.server:
            try:
                self.server.Destroy()
                self.logger.info("DDE server connection closed")
            except Exception as e:
                self.logger.error(f"Error while closing DDE server: {e}")
        else:
            self.logger.warning("No active DDE server to close")

    def exec_dde(self, command: str) -> None:
        """Execute a DDE command.

        Args:
            command (str): The DDE command to execute.

        Raises:
            RuntimeError: If not connected to the DDE server.
        """
        if not self.c or self.c.Connected() != 1:
            error_msg = "Not connected to MPA3 DDE server"
            self.logger.error(error_msg)
            raise RuntimeError(error_msg)

        try:
            self.logger.debug(f"Executing DDE command: {command}")
            self.c.Exec(command)
        except Exception as e:
            self.logger.error(f"Failed to execute DDE command '{command}': {e}")
            raise RuntimeError(f"DDE command execution failed: {e}")

    def start(self) -> None:
        """Start data acquisition in MPA3."""
        self.exec_dde("start")
        self.logger.info("Data acquisition started")

    def stop(self) -> None:
        """Stop data acquisition in MPA3."""
        self.exec_dde("halt")
        self.logger.info("Data acquisition stopped")

    def resume(self) -> None:
        """Resume paused data acquisition in MPA3."""
        self.exec_dde("cont")
        self.logger.info("Data acquisition resumed")

    def clear(self) -> None:
        """Clear the current data in MPA3."""
        self.exec_dde("erasempa")
        self.logger.info("MPA3 data cleared")

    def beep(self) -> None:
        """Trigger a beep sound in MPA3."""
        self.exec_dde("beep")
        self.logger.info("Beep sound triggered")

    def set_current_adc(self, adc_index: int) -> None:
        """Set the current ADC (Analog-to-Digital Converter) index.

        Args:
            adc_index (int): The index of the ADC to set.

        Raises:
            ValueError: If adc_index is not a non-negative integer.
        """
        if not isinstance(adc_index, int) or adc_index < 1 or adc_index > 4:
            error_msg = f"Invalid ADC index: {adc_index}. Must be a number from 1 to 4."
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        self.exec_dde(f"ADC={adc_index}")
        self.logger.info(f"ADC index set to {adc_index}")

    def get_data(self) -> list:
        """Retrieve data from MPA3 as a list of integers.

        Returns:
            list: List of integer values from MPA3.

        Raises:
            RuntimeError: If data request fails or returns invalid format.
        """
        try:
            self.logger.debug("Requesting data from MPA3...")
            data = self.c.Request("data")
            if not data:
                error_msg = "Empty response received from MPA3"
                self.logger.error(error_msg)
                raise RuntimeError(error_msg)

            # Split data by newlines and remove the last empty value
            data = data.split("\r\n")[:-1]
            data = [int(item) for item in data]
            self.logger.debug(f"Retrieved data: {data}")
            return data
        except ValueError as e:
            error_msg = f"Invalid data format received from MPA3: {e}"
            self.logger.error(error_msg)
            raise RuntimeError(error_msg)
        except Exception as e:
            error_msg = f"Failed to retrieve data from MPA3: {e}"
            self.logger.error(error_msg)
            raise RuntimeError(error_msg)

    def get_range(self) -> int:
        """Retrieve the current ADC range from MPA3.

        Returns:
            int: The current ADC range.

        Raises:
            RuntimeError: If the range request fails.
        """
        try:
            self.logger.debug("Requesting ADC range from MPA3...")
            range_adc = self.c.Request("range")
            range_adc = range_adc.split("\r\n")[0]
            range_value = int(range_adc)
            self.logger.debug(f"ADC range: {range_value}")
            return range_value
        except Exception as e:
            error_msg = f"Failed to retrieve ADC range: {e}"
            self.logger.error(error_msg)
            raise RuntimeError(error_msg)

    def set_path(self, path: str) -> None:
        """Set the file path for MPA3 operations.

        Args:
            path (str): The file path to set.

        Raises:
            ValueError: If the path exceeds the 90-character limit.
        """
        if len(path) > 90:
            error_msg = f"Path too long (max 90 characters). Provided path: {path}"
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        self.exec_dde(f"mpaname={path}")
        self.logger.info(f"File path set to: {path}")

    def save_mpa(self) -> None:
        """Save the current MPA3 configuration."""
        self.exec_dde("savempa")
        self.logger.info("MPA3 configuration saved")

    def load_mpa(self) -> None:
        """Load the MPA3 configuration."""
        self.exec_dde("loadmpa")
        self.logger.info("MPA3 configuration loaded")

if __name__ == '__main__':
    # Example usage
    mpa = DDEMPA3Control()
    if mpa.connect():
        try:
            mpa.start()
            data = mpa.get_data()
            print(f"Retrieved data: {data}")
        finally:
            mpa.close()