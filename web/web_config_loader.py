import os
import xml.etree.ElementTree as ET
import traceback

from summer.core.configloader.container import content

class WebService():

    def __init__(self,
                 name,
                 url,
                 chain_name,
                 input_web_param_to_name_dict,
                 output_web_param_to_name_dict):
        self.name = name
        self.chain_name = chain_name
        self.input_web_param_to_name_dict = input_web_param_to_name_dict
        self.output_web_param_to_name_dict = output_web_param_to_name_dict
        self.url = url.strip('/')

        self.chain = content.get(self.chain_name)
        if self.chain is None:
            raise Exception("chain not found: ",self.chain_name)


    def make_chain_input(self,env_dict):
        chain_input_dict = {}
        for web_param in self.input_web_param_to_name_dict.keys():
            chain_input_dict[self.input_web_param_to_name_dict[web_param]] = env_dict[web_param]
        return chain_input_dict

    def make_chain_output(self,chain_output_dict):
        output_dict = {}
        for chain_param in chain_output_dict.keys():
            # param_param:chain_param , find param_name
            for k,v in self.output_web_param_to_name_dict.items():
                if v == chain_param:
                    output_dict[k] = chain_output_dict[chain_param]
        return output_dict

    def run(self,env_dict):
        chain_input_dict = self.make_chain_input(env_dict)
        chain_output_dict = self.chain.run(chain_input_dict)
        output_dict = self.make_chain_output(chain_output_dict)
        return output_dict


class WebConfigLoader():
    def __init__(self):
        pass

    def load(self,config_xml_path):
        xml_data = open(config_xml_path, 'r').read()
        config = ET.fromstring(xml_data)
        services = []
        for web in config:
            for service in web:
                for service_info in service:
                    if service_info.tag == 'name':
                        name = service_info.text
                    if service_info.tag == 'url':
                        url = service_info.text
                    if service_info.tag == 'chain_name':
                        chain_name = service_info.text
                    if service_info.tag == 'input_params_name':
                        input_web_param_to_name_dict = {}
                        for param in service_info:
                            web_param = param.attrib['web_param']
                            input_web_param_to_name_dict[web_param] = param.text
                    if service_info.tag == 'output_params_name':
                        output_web_param_to_name_dict = {}
                        for param in service_info:
                            json_param = param.attrib['json_param']
                            output_web_param_to_name_dict[json_param] = param.text
                try:
                    service = WebService(name,
                                         url,
                                         chain_name,
                                         input_web_param_to_name_dict,
                                         output_web_param_to_name_dict)
                    services.append(service)
                except Exception as e:
                    traceback.print_exc()
                    print("load service error: ",name)
        return services

