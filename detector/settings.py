# -*- coding: utf-8 -*-
import os
import sys

execution_path=os.getcwd()
load_dir_default=os.path.join(execution_path,"to_analyze")
save_dir_default=os.path.join(execution_path,"analyzed")

def print_usage():
       
       print("\n    Usage:\n\n     "+sys.argv[0]+" [OPTIONS]\n")
       print("\n    Options:\n")

       print("     -load <input directory path>  : load image(s) from the user set path. If the path is not valid, \n"+
             "                                     it will be used the default input path "+load_dir_default+"\n")

       print("     -save <output directory path> : save results from the user set path. If the path is not valid,  \n"
            +"                                     it will be used the default output path "+save_dir_default+"\n")

       print("                             -face : enable face detection on the input images. If no specified it is\n"
            +"                                     enabled by default\n")
       
       print("                              -age : enable age prediction on the input images. If no specified it is\n"
            +"                                     enabled by default\n")

       print("                              -gen : enable gender detection on the input images. If no specified it \n"
            +"                                     is enabled by default\n")

       print("                               -em : enable emotion detection on the input images. If no specified it\n"
            +"                                     is enabled by default\n")

       print("                             -help : show help screen\n")

       print("                            -nores : disable the result text file generation in output directory\n")

       print("                            -all : enable all detection type on the input images\n")

       
       sys.exit()





def invalid_command(command):
     print("\n   "+str(command)+" : invalid command")
     print_usage()


