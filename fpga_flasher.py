"""
Title:
Author:
Date:

Scope:

1. Check if any board is detected;
2. Select the first detected board except if 'board' is specified;
3. Check if the board detected is installed (if not install it);
4. Check if SOF file exist;
5. Convert SOF into TTF file with quartus converter;
6. Bit reverse the TTF file producing app.h in the sketch folder;
7. Compile template sketch;

"""

#################
#####   LIBRARIES
#################


import subprocess
import sys
import os
import serial.tools.list_ports

from utils import PathManager,generate_app_file,read_args


############
#####   MAIN
############


if __name__ == '__main__':

    # get input arguments
    arguments = read_args(sys.argv)
    path_SOF_file = arguments['sof_path']
    port_to_use = None
    if not arguments['port'] is None:

        port_to_use = arguments['port']

    path_manager_json_path = os.getcwd() + os.sep + 'path_manager.json'
    if not arguments['path_manager'] is None:

        path_manager_json_path = arguments['path_manager']

    check_board = False
    if arguments['check_board']:

        check_board = True

    # Setup
    PM = PathManager(path_to_path_manager_json=path_manager_json_path)
    print('#######################################')
    print('FPGA FLASHER for ARduino MKR Vidor 4000')
    print('#######################################\n\n')
    print('Process start.\n\n')

    # Detect devices
    print('Scanning COM ports...')
    connected_usb_device_list = list(serial.tools.list_ports.comports())
    connected_arduinos = {}
    for connected_usb_device in connected_usb_device_list:

        port = connected_usb_device.device
        dev_name = connected_usb_device.description.replace(' ({})'.format(port), '')
        print('Found ' + dev_name + ' connected at port ' + port + '.')
        if 'Arduino' in dev_name:

            connected_arduinos.update({port: dev_name})

    N_arduinos_found = len(connected_arduinos)
    print('{} arduino-like device{} found{}!\n'.format(N_arduinos_found, 's' if N_arduinos_found > 1 else '',
                                                       '' if N_arduinos_found > 1 else 's'))
    # Select port
    if port_to_use is None:

        port_to_use = list(connected_arduinos.keys())[0]

    if port_to_use in list(connected_arduinos.keys()):

        dev_to_use = connected_arduinos[port]
        print('Port {} with device {} will be used.\n'.format(port_to_use, dev_to_use))

    else:

        print('>>> Error: Port {} not found!'.format(port_to_use))
        sys.exit(0)

    # Check device installation
    arduino_cli_path = PM.path_manager_json['arduino_cli_path']
    if check_board:

        print('Checking board installation in arduino-cli...')
        try:
            subp = subprocess.run([r'cd {}; arduino-cli.exe board list'.format(arduino_cli_path)],
                                  shell=True,
                                  stdout=subprocess.PIPE,
                                  executable=r'c:\Windows\System32\WindowsPowerShell\v1.0\PowerShell.exe')

        except subprocess.CalledProcessError as err:

            print('>>> Error: subprocess error \'{}\'.'.format(err.output))
            sys.exit(0)

        installed_boards_info = subp.stdout.decode('utf-8').replace('\n\n', '').split('\n')[1:]
        for info in installed_boards_info:

            if port_to_use in info:

                print('ok...board {} already installed.\n'.format(dev_to_use))

            else:

                print('Board not installed. Installation...')
                # TODO
                raise NotImplementedError
                sys.exit(0)

    # Convert SOF file into TTF file
    print('Generating TTF file from SOF file...')
    quartus_cpf_path = PM.path_manager_json['quartus_cpf_path']
    SOF_folder_path = os.path.dirname(path_SOF_file)
    SOF_file_name = os.path.basename(path_SOF_file)
    TTF_file_path = SOF_folder_path + os.sep + SOF_file_name.replace('.sof', '.ttf')
    try:

        subprocess.run([r'cd {}; quartus_cpf.exe -c {} {}'.format(quartus_cpf_path, path_SOF_file, TTF_file_path)],
                       shell=True,
                       executable=r'c:\Windows\System32\WindowsPowerShell\v1.0\PowerShell.exe')

    except subprocess.CalledProcessError() as err:

        print('>>> Error: subprocess error \'{}\'.'.format(err.output))
        sys.exit(0)

    print(' ...TTF file generated!\n')

    # Generate app.h file in the sketch folder
    print('Generating \'app.h\' file...')
    arduino_sketch_path = PM.path_manager_json['arduino_sketch_path']
    arduino_sketch_folder_path = os.path.dirname(arduino_sketch_path)
    generate_app_file(TTF_file_path, arduino_sketch_folder_path + os.sep + 'app.h')
    print(' ...\'app.h\' file generated!\n')

    # Compile and upload sketch template for coding the fpga
    print('Compiling sketch...')
    try:

        subprocess.run([r'cd {}; arduino-cli.exe compile --fqbn arduino:samd:mkrvidor4000 {}'.format(
            arduino_cli_path,arduino_sketch_path)],
                       shell=True,
                       executable=r'c:\Windows\System32\WindowsPowerShell\v1.0\PowerShell.exe')

    except subprocess.CalledProcessError() as err:

        print('>>> Error: subprocess error \'{}\'.'.format(err.output))
        sys.exit(0)

    print(' ...compilation terminated!\n')
    print('Uploading sketch to the board {}...'.format(dev_to_use))
    try:

        subprocess.run([r'cd {}; arduino-cli.exe upload -p {} --fqbn arduino:samd:mkrvidor4000 {}'.format(
            arduino_cli_path,port_to_use,arduino_sketch_path)],
                       shell=True,
                       executable=r'c:\Windows\System32\WindowsPowerShell\v1.0\PowerShell.exe')

    except subprocess.CalledProcessError() as err:

        print('>>> Error: subprocess error \'{}\'.'.format(err.output))
        sys.exit(0)

    print(' ... sketch uploaded!')
    print('\n\nFPGA flashed with success!')