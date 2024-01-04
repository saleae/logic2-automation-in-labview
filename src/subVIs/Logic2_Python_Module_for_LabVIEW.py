
# ALPHA VERSION NOTICE
# --------------------
# This software is currently in the Alpha stage of its development.
# Users should be aware that this software is under active development and may contain significant bugs, missing features, or unstable interfaces.
# Use this software with caution, and expect frequent updates and changes.

# DISCLAIMER:
# This software is provided by Saleae, Inc. "as is" and any express or implied warranties, including, but not limited to, the implied warranties of merchantability and fitness for a particular purpose are disclaimed. In no event shall Saleae, Inc. be liable for any direct, indirect, incidental, special, exemplary, or consequential damages (including, but not limited to, procurement of substitute goods or services; loss of use, data, or profits; or business interruption) however caused and on any theory of liability, whether in contract, strict liability, or tort (including negligence or otherwise) arising in any way out of the use of this software, even if advised of the possibility of such damage.



from saleae import automation

# INSTRUCTIONS
# 1. Install LabVIEW, and setup an Anaconda 3 instance using Python 3.8
# 2. Install the Saleae Python library using the instructions found here:
# https://saleae.github.io/logic2-automation/getting_started.html#installing-the-python-automation-api-package
# 3. Be sure Automation is enabled in the Logic2 Software



# Global variable declaration (Note: I hope to find a better way to maintain state in the future. ESAL22)
manager = None  # Global managing the Logic2 session
capture = None  # Global managing the captured data
spi_analyzer = None # Global managing the SPI Analyzer (Doing it this way limits you to 1 SPI analyzer, hope to improve. ESAL22)
device_configuration = None # Global managing device config
capture_configuraiton = None # Global managing capture config

def open_connection(ip_address, selected_port):
    """
    Opens a connection to the Logic 2 application.

    Args:
        ip_address (str): IP Address for the connection.
        selected_port (int): Port number for the connection.
    """
    global manager
    try:
        manager = automation.Manager.connect(port=selected_port, address=ip_address)
        # Additional initialization steps can be added here
    except Exception as e:
        return f"An error occurred while opening the connection: {e}"
    return 'success'

def device_config(enable_digital_channels, digital_sample_rate, digital_threshold_volts):
    """
    Configures the capturing device using an established connection.

    Args:
        enable_digital_channels (list): List of digital channels to enable.
        digital_sample_rate (int): Sampling rate in MSa/s.
        digital_threshold_volts (float): Logic level threshold in volts, rounded to 1 decimal place.
    """
    global manager, device_configuration
    if manager is None:
        return "Manager is not connected. Please establish a connection first."

    try:
        # Device configuration
        device_configuration = automation.LogicDeviceConfiguration(
            enabled_digital_channels=enable_digital_channels,
            digital_sample_rate=digital_sample_rate,
            digital_threshold_volts=round(digital_threshold_volts, 1),
        )

    except Exception as e:
        return f"An error occurred while configuring the device: {e}"
    return 'success'


def capture_duration_config(capture_duration):
    """
    Configures the capture, in this example it is a capture of finite duration in seconds.

    Args:
        capture_duration (float): Duration of the catpure in seconds.
    """
    global manager, capture_configuration
    if manager is None:
        return "Manager is not connected. Please establish a connection first."

    try:
        # Record N seconds of data before stopping the capture
        capture_configuration = automation.CaptureConfiguration(
        capture_mode=automation.TimedCaptureMode(duration_seconds=capture_duration)
        )

    except Exception as e:
        return f"An error occurred while configuring the capture: {e}"
    return 'success'


def start_capture(device_id):
    """
    Starts a capture session using the given configurations.

    Args:
        device_id (str): ID of the device to capture from.
        device_configuration: Configuration settings for the device.
        capture_configuration: Configuration settings for the capture.
    """
    global manager, capture, device_configuration, capture_configuraiton
    if manager is None:
        return "Manager is not connected. Please establish a connection first."

    try:
        temp_capture = manager.start_capture(
            device_id=device_id,
            device_configuration=device_configuration,
            capture_configuration=capture_configuration)

        temp_capture.wait()
        capture = temp_capture  # Assign to global variable
        return "Capture started successfully"
    except Exception as e:
        return f"An error occurred while starting the capture: {e}"




def add_spi_analyzer(label, mosi, miso, clock, enable, bits_per_transfer):
    """
    Adds an SPI analyzer to the capture session.

    Args:
        label (str): Label for the analyzer.
        miso (int): MISO channel number.
        clock (int): Clock channel number.
        enable (int): Enable channel number.
        bits_per_transfer (str): Number of bits per transfer.
    """
    global capture, spi_analyzer
    if capture is None:
        return "Capture session is not valid. Please start a capture first."

    try:
        spi_analyzer = capture.add_analyzer('SPI', label=label, settings={
            'MOSI': mosi,
            'MISO': miso,
            'Clock': clock,
            'Enable': enable,
            'Bits per Transfer': bits_per_transfer
        })
        return "SPI analyzer added successfully"
    except Exception as e:
        return f"An error occurred while adding the SPI analyzer: {e}"


def export_raw_digital(output_dir, digital_channels):
    """
    Exports the raw digital capture to a CSV file.

    Args:
        output_dir (str): File path and file name for the output CSV file.
        digital_channels (list): List of channels to be exported.
    """
    global capture
    if capture is None:
        return "Capture no longer exists. Please capture data first."

    try:
           # Export raw digital data to a CSV file
        capture.export_raw_data_csv(directory=output_dir, digital_channels=digital_channels)
        return "Raw digital data successfully exported to CSV file"
    except Exception as e:
        return f"An error occurred while exporting raw digital data to CSV: {e}"

def export_spi_analyzer_table(output_dir):
    """
    Export the data from the analyzer to a CSV file.

    Args:
        output_dir (str): File path and file name for the output CSV file.
        analyzer (string): Analyzer to be exported.
    """
    global capture, spi_analyzer
    if capture is None:
        return "Capture no longer exists. Please capture data first."

    try:
        # Export analyzer data to a CSV file
        analyzer_export_filepath = output_dir
        capture.export_data_table(
            filepath=analyzer_export_filepath,
            analyzers=[spi_analyzer]
        )
        return "Analyzer successfully exported to CSV file"
    except Exception as e:
        return f"An error occurred while exporting analyzer data to CSV: {e}"

def export_saleae_capture(capture_filepath):
    """
    Export the data from the analyzer to a CSV file.

    Args:
        capture_filepath (str): File path and file name for the output CSV file.
    """
    global capture
    if capture is None:
        return "Capture no longer exists. Please capture data first."

    try:
        # Finally, save the capture to a .sal file
        capture.save_capture(filepath=capture_filepath)
        return "Analyzer successfully saved."
    except Exception as e:
        return f"An error occurred while exporting the capture: {e}"


def close_connection():
    """
    Closes the connection to the Logic 2 application.
    """
    global manager
    if manager is None:
        return "Manager is not connected. Please establish a connection first."

    try:
        # Close the session and release the port
        if manager:
            manager.close()
            manager = None
    except Exception as e:
        return f"An error occurred whileclosing the session: {e}"
    return 'Logic2 Session Closed'