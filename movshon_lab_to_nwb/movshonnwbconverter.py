from nwb_conversion_tools import (
    NWBConverter, BlackrockRecordingExtractorInterface, BlackrockSortingExtractorInterface,
    OpenEphysRecordingExtractorInterface, OpenEphysSortingExtractorInterface,
    SpikeGLXRecordingInterface
)

from .expodatainterface import ExpoDataInterface


class MovshonBlackrockNWBConverter(NWBConverter):
    data_interface_classes = dict(
        BlackrockRecordingExtractorInterface=BlackrockRecordingExtractorInterface, 
        BlackrockSortingExtractorInterface=BlackrockSortingExtractorInterface
    )


class MovshonOpenEphysNWBConverter(NWBConverter):
    data_interface_classes = dict(
        OpenEphysRecordingExtractorInterface=OpenEphysRecordingExtractorInterface, 
        ExpoDataInterface=ExpoDataInterface
    )


class MovshonSpikeglxNWBConverter(NWBConverter):
    data_interface_classes = dict(
        SpikeGLXRecordingExtractorInterface=SpikeGLXRecordingInterface, 
        ExpoDataInterface=ExpoDataInterface
    )