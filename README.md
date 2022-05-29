# ArduinoMKRVidor4000: FPGA_FLASHER #


By running the script ```fpga_flasher.py``` all the steps from the .SOF file (produced by Quartus II) till the final setup of the fpga in
an arduino MKR Vidor 4000 are executed. In particular, the SOF file is converted into a TTF file, which is then bit reversed producing 
an app.h file, which is loaded in he SRAM of the board in order to program the fpga (compiling and upload in a template arduino sketch).
All these operations can be executed automatically in a python terminal in a simple line.


## NECESSARY SOFTWARES 

To run the ```fpga_flasher.py``` script the following software need to be installed on your computer:

1. Quartus II Lite 21.1
2. Arduino IDE 1.8.19 (the libraries related to the MKR Vidor 4000 need to be installed, see arduino manual)
3. Python 3.9

Moreover one need also to have the arduino-cli (Command Line Interpreter) in order to run arduino sketch from terminal. The last version 
avaialbe at the moment (```arduino-cli 0.22.0 for Windows 64bit```) can be found zipped in the ```Arduino-cli``` folder of this repository.
The user need to unzip the content in order to make thescript work. Depending on your system, the ```arduino-cli 0.22.0 for Windows 64bit``` 
executable may need to be changed if you use Windows 32bit. In general 'fpga_flasher' has been developed for Windows system, and cross-platform 
compatibility is not guaranteed, despite it may be probably achieved with minor changes of the code in the various scripts (provided that 
all the software can be installed on the OS).


## PATH MANAGER CONFIGURATION 


To use the ```fpga_flasher.py``` script, the user need to configure the ```path_manager.json``` file specifying the path of certain application, which
are called at the various steps. These paths need to be written as strings according to the usual JSON convention for strings (problems
may arise with the slash ```/``` in the path or when the folder have whitespace in their name: consider eventually to change the name of 
the problematic folders and replace ```/``` with ```//```). 

In particular one need to specify:

- PATH TO THE 'quartus_cpf.exe' executable in the field ```"quartus_cpf_path"```. The standards path to the 'quartus_cpf.exe' is typically

						"C:\intelFPGA_lite\21.1\quartus\bin64\quartus_cpf.exe"
  
  but it may depend on the setting chosen during the installation.

- PATH TO THE 'arduino-cli.exe' executable in the field ```"arduino_cli_path"```. If the project is left as it is, the zipped version of this
  executable can be found in the folder "Arduino-cli".

- PATH TO THE 'vidor_template.ino' project in the field ```"arduino_sketch_path"```. It is the bath to the template arduino project which 
  compile and upload on the board the basic sketch which load the fpga configuration in the SRAM of the board. If the project is
  left as it is, all the project files can be found in the folder "vidor_template" folder (where also the 'vidor_template.ino' file
  is present)

The 'path_manager.json' can be found as default in the project folder and is automatically read. However, the user can specify a
different path during the compilation of script (see below).


## HOT TO USE fpga_flasher_MKRVidor400


To execute the 'fpga_flasher', in a python terminal simply write

```$ python fpga_flasher.py [SOF file path] -p [PORT NAME] -pm [PATH MANAGER PATH] -cb```

positional argument:

- ```[SOF file path]``` : Absolute path of the SOF file containing the configuration of the fpga. Such a file is the typical output of the
                  Quartus II software after synthesis and compilation of a HDL code.
               

optional arguments:

- ```-p, --port``` : Name of the COM port where the MKR Vidor 4000 can be found. If not given, the COM port associated to the 
             first compatible device will be selected;
- ```-pm, --path_manager``` : Path to the path manager json containing all the necessary paths to run the scripts (see above);
- ```-cb, --check_board``` : If added, it is checked if the board is installed in the arduino-cli.exe compiler.


## USEFUL INFORMATION


1. Quartus II scripting reference manual for SOF to TTF file conversion:
https://www.intel.com/content/dam/www/programmable/us/en/pdfs/literature/manual/tclscriptrefmnl.pdf

2. GitHub repository of a minimal template vidor project:
https://github.com/chelmich/vidor_template

3. Arduino command line interface:
https://blog.arduino.cc/2020/03/13/arduino-cli-an-introduction/
https://github.com/arduino/arduino-cli/releases

4. FPGA flasher current version: 0.1 (22/05/2022) 
