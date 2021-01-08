from pynwb import NWBFile
from nwb_conversion_tools.baserecordingextractorinterface import BaseRecordingExtractorInterface
from nwb_conversion_tools.json_schema_utils import get_schema_from_method_signature
from spikeextractors import BlackrockRecordingExtractor


class BlackrockInterface(BaseRecordingExtractorInterface):
    """Primary data interface class for converting Blackrock data """

    @classmethod
    def get_source_schema(cls):
        raise NotImplementedError('TODO')
        source_schema = get_schema_from_method_signature(
            class_method=cls.RX.__init__,
            exclude=['smrx_channel_ids']
        )
        source_schema.update(additionalProperties=True)
        source_schema['properties'].update(
            file_path=dict(
                type=source_schema['properties']['file_path']['type'],
                format="file",
                description="path to data file"
            )
        )
        return source_schema

    def run_conversion(self, nwbfile: NWBFile, metadata: dict = None, stub_test: bool = False):
        raise NotImplementedError('TODO')