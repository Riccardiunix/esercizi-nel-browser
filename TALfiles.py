#!/usr/bin/env python3
import os
from sys import stderr
from datetime import datetime
from subprocess import PIPE, run

prog_lang_ext = {'Python': 'py','python': 'py'}

class TALfilesHelper():
    def __init__(self, TAc, ENV, instances_dirname = 'instances_catalogue', all_instances_subfolder = 'all_instances'):
        self.__TAc = TAc
        self.__INPUT_FILES = ENV.INPUT_FILES 
        self.__OUTPUT_FILES = ENV.OUTPUT_FILES
        self.__LOG_FILES = ENV.LOG_FILES
        self.__META_DIR = ENV.META_DIR
        self.__catalogue_path  = os.path.join(ENV.META_DIR, instances_dirname)
        self.__all_instances_path  = os.path.join(ENV.META_DIR, instances_dirname, all_instances_subfolder)


    def input_filename(self, file_handler):
        """Returns the fullname of the file associated to a given <file_handler>."""
        return os.path.join(self.__INPUT_FILES, file_handler)
        
    def exists_input_file(self, file_handler):
        """Checks whether the rtal call to the TAL service has associated a client local file to the handler <file_handler>."""
        return os.path.exists(self.input_filename(file_handler))
            
    def input_file_as_str(self, file_handler):
        """Returns, in the form of a single string, the content of the file that the rtal call to the TAL service has associated to the handler <file_handler>."""
        if not self.exists_input_file(file_handler):
            self.__TAc.print(f"Your rtal call to the service has associated no file to the handler `{file_handler}'.", "red", ["bold"])
            self.__TAc.print(f"The rtal call to the service has associated no file to the handler `{file_handler}'.", "red", ["bold"], file=stderr)
            exit(0)
        try:
            path = self.input_filename(file_handler)
            with open(path, 'r') as fin:
                file_as_str = fin.read()
                print(f'[The file you associated to the filehandler `{file_handler}` has been succesfully opened and converted to a string]')
                return file_as_str
        except IOError as ioe:
            self.__TAc.print(f"Fail to open your input file with handler `{file_handler}'.", "red", ["bold"])
            self.__TAc.print(f"Fail to open the file `{path}`", "red", ["bold"], file=stderr)
            exit(1)
        except os.error as err:
            TAc.print(f"Fail to read your input file with handler `{file_handler}'.", "red", ["bold"])
            TAc.print(f"Fail to read the input file `{path}`", "red", ["bold"], file=stderr)
            exit(1)
            
    def str2output_file(self, content, filename, timestamped = True):
        """Creates an output file to result in local to the client and with the given <content>. The filename is prefixed by a timestamp when timestamped = True."""
        if timestamped:
            filename = datetime.now(tz=None).strftime("%Y-%b-%d_%H.%M.%S.%f_") + filename
        try:
            with open(os.path.join(self.__OUTPUT_FILES,filename),'w') as fout:
                print(content, file=fout)
        except os.error as err:
            TAc.print(f"Fail to write down an output file named `{filename}'.", "red", ["bold"])
            TAc.print(f"Fail to write down an output file named `{filename}'.", "red", ["bold"], file=stderr)
            exit(1)

    def str2log_file(self, content, filename, timestamped = True):
        """Creates a logfile for an rtal call with token. This file will end up on the server and with the given <content>. The filename is prefixed by a timestamp when timestamped = True."""
        if timestamped:
            filename = datetime.now(tz=None).strftime("%Y-%b-%d_%H.%M.%S.%f_") + filename
        try:
            with open(os.path.join(self.__LOG_FILES,filename),'w') as fout:
                print(content, file=fout)
        except os.error as err:
            TAc.print(f"Fail to write down a logfile named `{filename}'.", "red", ["bold"])
            TAc.print(f"Fail to write down a logfile named `{filename}'.", "red", ["bold"], file=stderr)
            exit(1)

    def lang_extension(self, sourcecode_filename):
        result = run(f"guesslang {sourcecode_filename}", stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
        #print(f"{result.stdout=}")
        prog_lang = result.stdout.split(':')[1].strip()
        if prog_lang not in prog_lang_ext:
            return prog_lang
        else:
            return prog_lang_ext[prog_lang]

    def get_file_str_from_path(self, path):
        """Returns the contents of the file as a string from the selected path."""
        try:
            with open(path, 'r') as file:
                return file.read()
        except IOError as ioe:
            self.__TAc.print(f"Fail to open the file: {path}", "red", ["bold"])
            exit(0)

    def get_catalogue_instancefile_as_str_from_id_and_ext(self, id, format_extension):
        """Returns, in the form of a string, the contents of the instance file of a given id within the catalogue of instances stored on the server."""
        instance_filename = f'instance_{str(id).zfill(3)}.{format_extension}'
        fullpath = os.path.join(self.__all_instances_path, instance_filename)
        return self.get_file_str_from_path(fullpath)

