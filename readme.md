# Summer: A simple, lightweight, and fast static site generator

Summer is a simple, lightweight, and fast static site generator written in Python. You can only use XML and python function
to design your web service. It also supports dynamical updating.

## How to use

### 1, Install

download our source code.

### 2, write your functions

write your functions in anywhere you want. but be sure that you have install required packages for your codes.

### 3, write xml or update our example xml

write your xml file according to your true situation. you can also update our example xml file.

see ```/summer/core/configloader/example_chain.xml``` for more details.

in our example, we want to use summer.core.node.test_node.run1, summer.core.node.test_node.run2, summer.core.node.test_node_2.run1
to calculate the value of input a and b in code and return the result d in code. but we firstly should give function param an unqiue name:
```xml
<!-- node id is unique -->
<node id="n_1">
    <!-- Absolute Path of your .py file -->
    <path>Absolute Path</path>
    <!-- Function Name in your .py file you want to use -->
    <function_name>run1</function_name>
    <!-- refer other nodes output, if you want to use other nodes output, you should refer them first -->
    <pred_nodes>
    </pred_nodes>
    <!-- input params -->
    <input_params_name>
        <!-- code names is param in function defined in your .py file -->
        <!-- value is the name in content of framework-->
        <!-- input params is only used to refer pred_nodes output and chain input params -->
        <!-- It means that function param 'a' value is get by framework from content variable named 'in_1' -->
        <param code_name="a">in_1</param>
        <param code_name="b">in_2</param>
    </input_params_name>
    <output_params_name>
        <!-- output params is same as input params -->
        <!-- It means that function param 'c' value will give to variable named 'value_1' in framework content-->
        <param code_name="c">value_1</param>
    </output_params_name>
</node>
```

When finish define node in xml, you should define the chain of nodes:

```xml
<!-- chain name is unique -->
<chain name="chain_1">
    <!-- chain's input params is means that input params is code_name and value is the name in content of framework-->
    <!-- It means that function param 'in_p_1' value is get by framework from content variable named 'in_1' -->
    <!-- It's global variable for all nodes in chain -->
    <input_params_name>
        <param code_name="in_p_1">in_1</param>
        <param code_name="in_p_2">in_2</param>
    </input_params_name>
    <output_params_name>
        <param code_name="out_p_1">out_1</param>
    </output_params_name>
    <!-- nodes is the nodes in chain -->
    <nodes>
    </nodes>
    <!-- so the run this chain should give a dict like {'in_p_1': 1, 'in_p_2': 2} to framework -->
    <!-- and the framework will return a dict like {'out_p_1': xxx} -->
</chain>
```

After define the chains, you should define the web service to use the chains:   

see ```/summer/web/web_chain.xml``` for more details.

```xml

<web name="web_service_1">
    <service>
        <!-- service name is unique -->
        <name>service_1</name>
        <!-- url is the url of your web service -->
        <url>/service_3</url>
        <!-- chain_name is the chain name you want to use -->
        <chain_name>chain_1</chain_name>
        <!-- input params is means that input params is web_param and given to variable named 'in_1' in framework content-->
        <input_params_name>
            <param web_param="in_web_1">in_p_1</param>
            <param web_param="in_web_2">in_p_2</param>
        </input_params_name>
        <output_params_name>
            <param json_param="out_web_1">out_p_1</param>
        </output_params_name>
        <!-- so you will give a POST request to url  http://host:port/service_1 with json like {data:{'in_web_1': 1, 'in_web_2': 2}} -->
        <!-- and the response will return a json like {'out_web_1': xxx} -->
    </service>
</web>

```

### 4, update config.py

update ```config.py``` to your true situation.

config_xml_path is the path of your xml file.

config_web_xml_path is the path of your web xml file.


### 5, start

run ```python /summer/web/web_api.py``` to start the web service.