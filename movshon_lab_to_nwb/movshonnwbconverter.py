from nwb_conversion_tools import (
    NWBConverter, BlackrockRecordingExtractorInterface, BlackrockSortingExtractorInterface,
    OpenEphysRecordingExtractorInterface, OpenEphysSortingExtractorInterface
)

from .expodatainterface import ExpoDataInterface


class MovshonBlackrockNWBConverter(NWBConverter):
    data_interface_classes = dict(
        BlackrockRecordingExtractorInterface=BlackrockRecordingExtractorInterface, 
        BlackrockSortingExtractorInterface=BlackrockSortingExtractorInterface,
        ExpoDataInterface=ExpoDataInterface
    )


class MovshonOpenEphysNWBConverter(NWBConverter):
    data_interface_classes = dict(
        OpenEphysRecordingExtractorInterface=OpenEphysRecordingExtractorInterface, 
        # OpenEphysSortingExtractorInterface=OpenEphysSortingExtractorInterface,
        ExpoDataInterface=ExpoDataInterface
    )