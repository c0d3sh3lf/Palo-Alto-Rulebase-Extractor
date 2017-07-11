#!/usr/bin/python

__author__ = "Sumit Shrivastava"
__version__ = "1.0.0"

from xml.dom.minidom import parse
import xml.dom.minidom
import optparse, sys


def readXMLFile(inputfilename):
    DOMTree = xml.dom.minidom.parse(inputfilename)
    return DOMTree

def printConfigVersion(DOMTree):
    configuration = DOMTree.documentElement
    if configuration.hasAttribute('urldb'):
        print "URL DB :", configuration.getAttribute('urldb')
    if configuration.hasAttribute('version'):
        print "Configuration Version :", configuration.getAttribute('version')

def parseXMLFile(DOMTree):
    configuration = DOMTree.documentElement
    rulebase = configuration.getElementsByTagName('devices')[0].getElementsByTagName('vsys')[0].getElementsByTagName('entry')[0].getElementsByTagName('rulebase')[0]
    rules = rulebase.getElementsByTagName("security")[0].getElementsByTagName("rules")[0].getElementsByTagName("entry")
    outputdata = "Sr. No.,Name,To,From,Source,Destination,Source User,Category,Application,Service,HIP Profiles,Action,Log Start,Log Setting\n"
    srno = 1
    for entry in rules:
        outputdata += str(srno) + ","
        outputdata += entry.getAttribute("name") + ",\""
        for members in entry.getElementsByTagName("to")[0].getElementsByTagName("member"):
            outputdata += members.childNodes[0].data + ","
        outputdata = outputdata[:-1:]
        outputdata += "\",\""
        for members in entry.getElementsByTagName("from")[0].getElementsByTagName("member"):
            outputdata += members.childNodes[0].data + ","
        outputdata = outputdata[:-1:]
        outputdata += "\",\""
        for members in entry.getElementsByTagName("source")[0].getElementsByTagName("member"):
            outputdata += members.childNodes[0].data + ","
        outputdata = outputdata[:-1:]
        outputdata += "\",\""
        for members in entry.getElementsByTagName("destination")[0].getElementsByTagName("member"):
            outputdata += members.childNodes[0].data + ","
        outputdata = outputdata[:-1:]
        outputdata += "\",\""
        for members in entry.getElementsByTagName("category")[0].getElementsByTagName("member"):
            outputdata += members.childNodes[0].data + ","
        outputdata = outputdata[:-1:]
        outputdata += "\",\""
        for members in entry.getElementsByTagName("application")[0].getElementsByTagName("member"):
            outputdata += members.childNodes[0].data + ","
        outputdata = outputdata[:-1:]
        outputdata += "\",\""
        for members in entry.getElementsByTagName("service")[0].getElementsByTagName("member"):
            outputdata += members.childNodes[0].data + ","
        outputdata = outputdata[:-1:]
        outputdata += "\",\""
        for members in entry.getElementsByTagName("hip-profiles")[0].getElementsByTagName("member"):
            outputdata += members.childNodes[0].data + ","
        outputdata = outputdata[:-1:]
        outputdata += "\","
        outputdata += entry.getElementsByTagName("action")[0].childNodes[0].data + ","
        try:
            outputdata += entry.getElementsByTagName("log-start")[0].childNodes[0].data + ","
        except:
            outputdata += ","
        try:
            outputdata += entry.getElementsByTagName("log-setting")[0].childNodes[0].data + ","
        except:
            outputdata += ","
        outputdata +="\n"
        srno += 1
    return outputdata

def writeCSV(outputfilename, outputdata):
    csvfile = open(outputfilename, "w")
    csvfile.write(outputdata)
    csvfile.flush()
    csvfile.close()
    print "[+]", outputfilename, "written successfully."

def main():
    parser = optparse.OptionParser("python pa_rulebase.py -x XMLFILE -c CSVFILE\n\r\n\rIf CSVFILE not provided, CSV filename will be same as that of XMLFILE")
    parser.add_option("-x", "--xml", dest="xmlfile", help="Palo Alto Extracted Configuration File")
    parser.add_option("-c", "--csv", dest="csvfile", help="Output CSV filename")
    options, args = parser.parse_args()
    if not(options.xmlfile):
        print "[-] XML file is required"
        parser.print_help()
        sys.exit(1)
    else:
        if not(options.csvfile):
            options.csvfile = options.xmlfile.split(".")[0] + ".csv"
        else:
            if not(options.csvfile.split(".")[len(options.csvfile.split("."))-1] == "csv"):
                options.csvfile = options.csvfile + ".csv"
        printConfigVersion(readXMLFile(options.xmlfile))
        writeCSV(options.csvfile, parseXMLFile(readXMLFile(options.xmlfile)))

if __name__ == "__main__":
    main()