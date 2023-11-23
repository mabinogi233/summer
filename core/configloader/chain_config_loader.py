import os
import xml.etree.ElementTree as ET
import traceback

from summer.core.node.nodeloader import NodeLoader

class ChainNode():

    def __init__(self,
                 input_code_name_2_name_dict,
                 output_code_name_2_name_dict,
                 func,
                 pre_node_list,
                 id):
        self.input_code_name_2_name_dict = input_code_name_2_name_dict
        self.output_code_name_2_name_dict = output_code_name_2_name_dict

        self.code_names = list(input_code_name_2_name_dict.keys())
        self.func = func
        self.pre_node_list = pre_node_list
        self.id = id

    def make_input(self,env_dict):
        input_dict = {}
        for code_name in self.code_names:
            if self.input_code_name_2_name_dict[code_name] not in env_dict:
                raise Exception("not have required params: ",self.input_code_name_2_name_dict[code_name],
                                " of node: ",self.id)
            input_dict[code_name] = env_dict[self.input_code_name_2_name_dict[code_name]]
        return input_dict

    def make_output(self,output_code_name_dict):
        output_name_dict = {}
        for code_name in output_code_name_dict.keys():
            output_name_dict[self.output_code_name_2_name_dict[code_name]] = output_code_name_dict[code_name]
        return output_name_dict

    def call(self,env_dict):
        # env: name-value
        input_dict = self.make_input(env_dict)
        output_dict = self.func(**input_dict)
        return self.make_output(output_dict)


class Chain():

    def __init__(self,
                 chain_name,
                 node_list,
                 input_code_name_2_name_dict,
                 output_code_name_2_name_dict):
        self.node_list = node_list
        self.input_code_name_2_name_dict = input_code_name_2_name_dict
        self.output_code_name_2_name_dict = output_code_name_2_name_dict
        self.code_names = list(input_code_name_2_name_dict.keys())
        self.chain_name = chain_name

    def make_input(self,env_dict):
        input_dict = {}
        for code_name in self.code_names:
            if self.input_code_name_2_name_dict[code_name] not in env_dict:
                raise Exception("not have required params: ",self.input_code_name_2_name_dict[code_name],
                                " of chain: ",self.chain_name)
            input_dict[code_name] = env_dict[self.input_code_name_2_name_dict[code_name]]
        return input_dict

    def make_output(self,output_code_name_dict):
        output_name_dict = {}
        for code_name in output_code_name_dict.keys():
            output_name_dict[self.output_code_name_2_name_dict[code_name]] = output_code_name_dict[code_name]
        return output_name_dict

    def run(self,env_dict):
        # env: name-value
        input_dict = self.make_input(env_dict)

        output_dict = {node.id:None for node in self.node_list}
        finished_node_list = []
        while len(finished_node_list) < len(self.node_list):
            # find a node to run, this node pres are all finished
            has_node_to_run = False
            run_node = None
            for node in self.node_list:
                if node.id in finished_node_list:
                    continue
                this_node_pre_finished = True
                for parent in node.pre_node_list:
                    if parent not in finished_node_list:
                        this_node_pre_finished = False
                        break
                if this_node_pre_finished:
                    has_node_to_run = True
                    run_node = node
                    break
            if not has_node_to_run:
                break
            # run node
            # make env and pred output
            node_env_dict = {}

            for k,v in input_dict.items():
                node_env_dict[k] = v
            for parent in run_node.pre_node_list:
                for k,v in output_dict[parent].items():
                    node_env_dict[k] = v

            # run node
            node_output_dict = run_node.call(node_env_dict)
            # update output
            output_dict[run_node.id] = node_output_dict
            finished_node_list.append(run_node.id)


        # update finished node list
        o = {}
        for _,value in output_dict.items():
            for k,v in value.items():
                if v is not None and k in self.output_code_name_2_name_dict.values():
                    # find x that (x,k) in output_code_name_2_name_dict
                    for x,y in self.output_code_name_2_name_dict.items():
                        if y == k:
                            o[x] = v
                            break
        return o


class ChainConfigLoader():
    def __init__(self):
        pass

    def load(self,config_xml_path):
        xml_data = open(config_xml_path, 'r').read()
        config = ET.fromstring(xml_data)
        chain_list = []
        for chain in config:
            chain_input_code_name_2_name_dict = {}
            chain_output_code_name_2_name_dict = {}
            chain_name = chain.attrib['name']
            node_list = []
            for info in chain:
                if info.tag == 'input_params_name':
                    for input_param in info:
                        code_name = input_param.attrib['code_name']
                        name = input_param.text
                        chain_input_code_name_2_name_dict[code_name] = name
                elif info.tag == 'output_params_name':
                    for output_param in info:
                        code_name = output_param.attrib['code_name']
                        name = output_param.text
                        chain_output_code_name_2_name_dict[code_name] = name
                elif info.tag == 'nodes':
                    for _node in info:
                        id = _node.attrib['id']
                        for node in _node:
                            if node.tag == 'path':
                                path = node.text
                            elif node.tag == 'pred_nodes':
                                pre_node_list = []
                                for pre_node in node:
                                    pre_node_list.append(pre_node.text)
                            elif node.tag == 'function_name':
                                func_name = node.text
                            elif node.tag == 'input_params_name':
                                node_input_code_name_2_name_dict = {}
                                for input_param in node:
                                    code_name = input_param.attrib['code_name']
                                    name = input_param.text
                                    node_input_code_name_2_name_dict[code_name] = name
                            elif node.tag == 'output_params_name':
                                node_output_code_name_2_name_dict = {}
                                for output_param in node:
                                    code_name = output_param.attrib['code_name']
                                    name = output_param.text
                                    node_output_code_name_2_name_dict[code_name] = name
                            # load node
                        try:
                            file_name = path.split(os.sep)[-1]
                            if '.' in file_name:
                                file_name = file_name.split('.')[0]
                            func = NodeLoader().load_function(path, file_name, func_name)
                            node = ChainNode(
                                input_code_name_2_name_dict=node_input_code_name_2_name_dict,
                                output_code_name_2_name_dict=node_output_code_name_2_name_dict,
                                func=func,
                                pre_node_list=pre_node_list,
                                id=id
                            )
                            node_list.append(node)
                        except Exception as e:
                            print('load node error:',e)
                            traceback.print_exc()
                            continue

            chain_ = Chain(
                input_code_name_2_name_dict=chain_input_code_name_2_name_dict,
                output_code_name_2_name_dict=chain_output_code_name_2_name_dict,
                node_list=node_list,
                chain_name=chain_name
            )
            chain_list.append(chain_)

        return chain_list


def test_load_example():
    from summer.core.node import test_node, test_node_2
    node_1 = ChainNode(
        input_code_name_2_name_dict={'a': 'in_1', 'b': 'in_2'},
        output_code_name_2_name_dict={'c': 'value_1'},
        func=test_node.run1,
        pre_node_list=[],
        id='n_1'
    )
    node_2 = ChainNode(
        input_code_name_2_name_dict={'a': 'value_1'},
        output_code_name_2_name_dict={'b': 'value_2'},
        func=test_node_2.run2,
        pre_node_list=['n_1'],
        id='n_2'
    )
    node_3 = ChainNode(
        input_code_name_2_name_dict={'a': 'value_1', 'b': 'value_2', 'c': 'in_2'},
        output_code_name_2_name_dict={'d': 'out_1'},
        func=test_node.run3,
        pre_node_list=['n_1', 'n_2'],
        id='n_3'
    )

    chain = Chain(
        chain_name='test_chain',
        node_list=[node_1, node_2, node_3],
        input_code_name_2_name_dict={'in_1': 'in_1', 'in_2': 'in_2'},
        output_code_name_2_name_dict={'out_1': 'out_1'},
    )

    input_ = {'in_1': 1, 'in_2': 2}
    output = chain.run(input_)
    print(output)

    ChainConfigLoader().load('example_chain.xml')


def test_load_example_2():
    ChainConfigLoader().load('example_chain.xml')


if __name__ == '__main__':
    chains = ChainConfigLoader().load('example_chain.xml')
    for chain in chains:
        chain.run({'in_1': 1, 'in_2': 2})

