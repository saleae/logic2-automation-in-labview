# logic2-automation-in-labview
 Automated control of Logic2 software from LabVIEW. Supports Logic 8, Logic Pro 8, and Logic Pro 16

# Overview
Demonstrates how to use Python to automate the Saleae Logic2 software.
    
# Requirements 
LabVIEW 2021 or newer
Python 3.8, 3.9 or 3.10 with the same bitness as LabVIEW.

# Instructions
1. Install LabVIEW, and setup an Anaconda 3 instance using Python 3.8
  https://knowledge.ni.com/KnowledgeArticleDetails?id=kA00Z0000015C6tSAE&l=en-US 
2. Install the Saleae Python library using the instructions found here:
  https://saleae.github.io/logic2-automation/getting_started.html#installing-the-python-automation-api-package
3. Be sure Automation is enabled in the Logic2 Software (Saleae link above)
4. Load [Python_Logic2_Automation.vi]. The key parameters in the main VI are the Anaconda setings and the Saleae Logic 'Device ID' (F4241 is the default simulated Logic Pro 16)

# Included in this release 0.1
Reproduction of the [saleae_example.py] shipping example.

## Python_Logic2_Automation.vi
 - Highest level example VI that contains the user interface and all of the supporting subVIs

## Logic 2 Automation Supporting SubVIs
### Logic_Open_Connection.vi
- Inputs: ip_address, selected_port
- Establishes a connection to the Logic 2 application using a specified IP address and port number.

### Logic_Config_Device.vi
- Inputs: enable_digital_channels, digital_sample_rate, digital_threshold_volts
- Configures the capturing device with settings like enabled digital channels, sample rate, and logic level threshold.

### Logic_Config_Capture_Duration.vi
- Inputs: capture_duration
- Sets up the capture configuration, specifically the duration of the capture.

### Logic_Start_Capture.vi
 - Inputs: device_id
 - Initiates a capture session using the provided device and configuration settings.

### Logic_Add_SPI_Analyzer.vi
- Inputs: label, mosi, miso, clock, enable, bits_per_transfer
- Adds an SPI (Serial Peripheral Interface) analyzer to the capture session with specified settings for channels and transfer bits.

### Export_Raw_Digital_to_CSV.vi
- Inputs: file path, digital channels to export
- Exports the captured raw digital data to a CSV file.

### Export_SPI_Analyzer_Table_to_CSV.vi
- Inputs: output_dir
- Exports data from an analyzer (in this case, the SPI analyzer) to a CSV file.

### Export_Saleae_Capture_File.vi
- Inputs: capture_filepath
- Saves the entire capture session to a file.

### Logic_Close_Connection.vi
- Inputs: None
- Closes the connection to the Logic 2 application.


## Additional Supporting VIs
### Build_Filename_with_Date_Time.vi
- Inputs: File Path, File Name Prefix, File Exension
- Adds the time and date stamp to a file name to ensure a unique file is created



# Additional Notes
## To control Logic2 running on another computer, the Logic2 software must be run with the following command line arguments:

Mac:
do shell script "open -a '/Applications/Logic2.app' --args --automation --automationHost 0.0.0.0 --automationPort 10430"

PC: 
start "" "C:\Path\To\Logic2.exe" --automation --automationHost 0.0.0.0 --automationPort 10430

Linux:
/path/to/Logic2 --automation --automationHost 0.0.0.0 --automationPort 10430

Note: The "path to Logic2" should be replaced with the path to and name of the Logic2 executable.





# Troubleshooting








# Know Issues and Limitations
1. Global Variable Usage
- In order to preserve the state between LabVIEW calls, several session variables are estrablished as global variables. This is generally bad programming practice and I have not had enough time to find another way to accomplish this using classes or some other method. Feedback and suggestions welcome!

2. Configurations VIs and funcations are application specific.
- Currently the configuration VIs and supporting Python functions are very specific to the example use case. This can be expanded to be more generic and thus handling more use cases. For example the 'Device Configuration' only exposes the digital parameters and not the Analog settings. Each named control and selection value in the Logic2 Graphical User Interface can be remotely controlled from the Automation software, so there is lots of room for the LabVIEW based automation library to grow!



