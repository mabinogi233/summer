import importlib


class NodeLoader():

    def load(self, path, file_name):
        '''
        load python file as a module
        :param path:
        :param file_name:
        :return:
        '''
        spec = importlib.util.spec_from_file_location(file_name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def load_class(self, path, file_name, class_name):
        '''
        load python file as a module
        :param path:
        :param file_name:
        :return:
        '''
        spec = importlib.util.spec_from_file_location(file_name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return getattr(module, class_name)

    def load_function(self, path, file_name, function_name):
        '''
        load python file as a module
        :param path:
        :param file_name:
        :return:
        '''
        spec = importlib.util.spec_from_file_location(file_name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return getattr(module, function_name)




