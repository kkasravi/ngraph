from neon import NervanaObject  # noqa

from ngraph.transformers.base import Transformer, Computation, make_transformer_factory, set_transformer_factory
from ngraph.transformers.passes.hetrpasses import DeviceAssignPass, CommunicationPass

class HetrComputation(Computation):
    """
    Lightweight wrapper class for handling runtime execution of child computations for HeTr
    """

    def __init__(self, computations):
        super(HetrComputation, self).__init__()

        self.computations = computations

    def __call__(self):
        """
        TODO
        Implement threading driver to call each of the computations in self.computations
        :return: 
        """

class HeTrTransformer(Transformer):
    """
    Transformer for executing graphs on a CPU, backed by numpy.

    Given a list of ops you want to compute the results of, this transformer
    will compile the graph required to compute those results and exposes an
    evaluate method to execute the compiled graph.
    """

    transformer_name = "hetr"

    def __init__(self, **kwargs):
        super(HeTrTransformer, self).__init__(**kwargs)

        self.HeTrPasses = [DeviceAssignPass(default_device='gpu'), CommunicationPass()]


    def computation(self, results, *parameters, **kwargs):
        """
        TODO

        run the HetrPasses here, instead of running them with the other graph passes.
            * this is probably a bit of a hack, but lets go with it for now

        once the HetrPasses have run, we know which device/transformer hints apply to each node

        use the helper function (build_transformers) to construct child transformers for all the hinted ids in the graph

        build a dictionary mapping from transformer hint_string to results
            * sendnode should be included as a 'result', but recvnode should be ignored as it will be uncovered by traversal

            i.e. {'numpy0': [x_plus_1, send1],
                  'numpy1': [some_other_tensor]}

        now, for each transformer in the child transformers, create a child computation, passing in the results for that transformer
            * i skipped placeholders in the map of results; these need to be mapped in a corresponding way

        Create a HetrComputation object, passing a list of child computations

        return the HetrComputation

        :param results:
        :param parameters:
        :param kwargs:
        :return: a HetrComputation object
        """
        pass


    def build_transformers(self, results):
        """
        TODO

        implement one more graph traversal, which builds a set of transformer hints (i.e. numpy0, numpy1)

        then, for each string in the set, build a real transformer and put them in a dictionary
            i.e. {'numpy0': NumpyTransformer(),
                  'numpy1': NumpyTransformer()}

        :param results: the graph nodes that we care about, for the computation
        :return: the dictionary of transformers, with names matching the graph node hints
        """
        pass

    def get_transformer(self, hint_string):
        """
        TODO

        for now, implement a basic mapping.
            {'numpy': NumpyTransformer,
             'gpu': GPUTransformer}

        then do a string compare on the hint_string, and return whichever one of the mapped transformers
        matches the beginning of the hint string

        :param hint_string: a string such as 'numpy0'
        :return: The NumpyTransformer class, in this case
        """

    def device_buffer_storage(self, bytes, dtype, name):
        """
        Make a DeviceBuffer.

        Arguments:
            bytes: Size of buffer.
            alignment: Alignment of buffer.

        Returns: A DeviceBuffer.
        """
        print("device_buffer_storage")
        return []


    def device_buffer_reference(self):
        """
        Make a DeviceBufferReference.

        Returns: A DeviceBufferReference.
        """
        print("device_buffer_reference")
        return None


    def start_transform_allocate(self):
        print("start_transform_allocate")

    def finish_transform_allocate(self):
        print("finish_transform_allocate")

    def transform_ordered_ops(self, ordered_ops, name):
        print(name, ordered_ops)
        return name + 1


    def finish_transform(self):
        pass


    def allocate_storage(self):
        pass

set_transformer_factory(
    make_transformer_factory(HeTrTransformer.transformer_name))