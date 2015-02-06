"""MythTV Web Services Python API

This module provides convenient access to the MythTV Web Services using
suds-jurko.

TODO:

* suds-jurko doesn't execute the schema imports specified by the MythTV wsdl.
  Currently MythTVService downloads all the schema and merges it in to a single
  file.
  Either MythTV is correct and suds-jurko should be modified to handle it, or
  MythTV is incorrect and needs to be fixed."""

from lxml.etree import parse
from os.path import exists, join
from urllib.request import urlopen
from suds.client import Client

from mythtvlib.utils import get_tmp_dir

class MythTVServiceException(Exception):
    pass

class MythTVServiceAPI(object):
    """Provide convenient access to the low-level MythTV Web Services."""

    services = ['Capture', 'Channel', 'Content', 'DVR', 'Frontend', 'Guide', 'Myth', 'Video']

    def __init__(self, service_name, backend):
        self.service_name = service_name
        self.backend = backend
        self.wsdl = None
        self.wsdl_fname = join(get_tmp_dir(),
                               "MythTV-{0}.wsdl".format(service_name))
        self.client = self._client_for(service_name)
        self.service = self.client.service
        self.wsdl_namespaces = self.wsdl.getroot().nsmap
        # FIXME: The wsdl namespace seems to have None as its name
        self.wsdl_namespaces['wsdl'] = self.wsdl_namespaces[None]
        del self.wsdl_namespaces[None]
        self._operations = None
        return

    def _fetch_imports_includes(self, root, imports):
        """As part of working around suds-jurko and the MythTV wsdl
        not playing nicely together, search through the supplied Element and
        fetch each import to be later inserted back in to the root WSDL."""
        import_elements = root.findall(".//*[@schemaLocation]/..")
        for import_element in list(import_elements):
            for imp in list(import_element):
                location = imp.get('schemaLocation')
                if location is None:
                    continue
                if location in imports.keys():
                    continue
                import_string = urlopen(location)
                import_tree = parse(import_string)
                imports[location] = {
                    'import': imp,
                    'source': import_string,
                    'tree': import_tree
                    }
                self._fetch_imports_includes(import_tree, imports)
                import_element.remove(imp)
        return

    def _write_wsdl_for(self, service):
        """Work around suds-jurko and the MythTV wsdl
        not playing nicely together.
        
        1. Retrieve the WSDL
        2. Search through and retrieve the imported definitions,
           removing the imports as we go.
        3. Place the definitions in the original WSDL"""
    
        url = 'http://{hostname}:{port}/{service}/wsdl'.format(
                service=service,
                hostname=self.backend.hostname,
                port=self.backend.port)
        wsdl_string = urlopen(url)
        wsdl = parse(wsdl_string)
        root = wsdl.getroot()
        schema = root.find(".//*[@targetNamespace='http://mythtv.org']")
        imports = {}
        
        self._fetch_imports_includes(root, imports)
        for k, imp in imports.items():
            vroot = imp['tree'].getroot()
            for e in list(vroot):
                if 'schemaLocation' in e.keys():
                    continue
                schema.insert(1, e)
        wsdl.write(self.wsdl_fname, encoding='utf-8', xml_declaration=True)
        self.wsdl = wsdl
        return

    def _get_wsdl_for(self, service):
        """Retrieve the suds-jurko friendly wsdl definitions.
        If the cache file exists, use it directly,
        otherwise download it from the backend."""
        if exists(self.wsdl_fname):
            self.wsdl = parse(self.wsdl_fname)
        else:
            self._write_wsdl_for(service)
        return

    def _client_for(self, service):
        """Return the suds client for the specified service"""
        if service not in self.services:
            raise MythTVServiceException("Unknown service: {0}".format(service))
        self._get_wsdl_for(service)
        url='file://{0}'.format(self.wsdl_fname)
        client = Client(url)
        return client

    def operations(self, types=['GET']):
        """Return the automatically supported command names for the receivers
        service.  Currently this means any operation that uses http get, and
        thus isn't expected to modify the database in any way."""
        if self._operations is not None:
            return self._operations

        command_elements = self.wsdl.findall('.//wsdl:operation/wsdl:documentation/..', self.wsdl_namespaces)
        ops = []
        for operation in command_elements:
            try:
                optype = operation.find("./wsdl:documentation", self.wsdl_namespaces).text.strip()
            except AttributeError:
                optype = "None"
            if optype in types:
                ops.append(operation.get("name"))
        self._operations = ops
        return self._operations

    def operation_parameters(self, operation):
        """Return the list of parameters for the requested operation"""
        operation_elements = self.wsdl.findall(".//xs:element[@name='{0}']".format(operation),
                                               self.wsdl_namespaces)
        assert len(operation_elements) == 1, "Expected single operation element"
        parameters = operation_elements[0].findall(".//xs:element",
                                                   self.wsdl_namespaces)
        return parameters

    def print_help(self, show_post=False):
        """Print the list of supported operations and their parameter names"""
        if show_post:
            types = ["GET", "POST"]
        else:
            types = ["GET"]
        print("Supported Operations:")
        for operation in self.operations(types):
            parameters = self.operation_parameters(operation)
            parameter_names = [x.get('name') for x in parameters]
            parameter_string = ", ".join(parameter_names)
            print("    {0:<30} {1}".format(operation, parameter_string))
        return

    def print_operation_help(self, op_name):
        """Print the parameter details for the requested operation"""
        print(op_name, "parameters:")
        parameters = self.operation_parameters(op_name)
        fmt_string = "    {name:<30} {ptype:<20} {minoccurs:<9} {nillable}"
        print(fmt_string.format(
                name="Name",
                ptype="Type",
                minoccurs="MinOccurs",
                nillable="Nillable"))
        for param in parameters:
            print(fmt_string.format(
                name=param.get('name'),
                ptype=param.get('type'),
                minoccurs=param.get('minOccurs'),
                nillable=param.get('nillable')))
        return

    def execute_args(self, args):
        op_name = args[0]
        op_args = args[1:]
        if len(op_args) == 1 and op_args[0] == "help":
            self.print_operation_help(op_name)
            resp = ""
        else:
            resp = getattr(self.client.service, op_name)(*op_args)
        return resp

    def __repr__(self):
        return "{cls}({svc})".format(cls=self.__class__.__name__, svc=self.service_name)
