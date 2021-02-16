from nwb_conversion_tools import (
    NWBConverter, BlackrockRecordingExtractorInterface, BlackrockSortingExtractorInterface,
    OpenEphysRecordingExtractorInterface, OpenEphysSortingExtractorInterface
)


class MovshonBlackrockNWBConverter(NWBConverter):
    data_interface_classes = dict(
        BlackrockRecordingExtractorInterface=BlackrockRecordingExtractorInterface, 
        BlackrockSortingExtractorInterface=BlackrockSortingExtractorInterface
    )

class MovshonOpenEphysNWBConverter(NWBConverter):
    data_interface_classes = dict(
        OpenEphysRecordingExtractorInterface=OpenEphysRecordingExtractorInterface, 
        # OpenEphysSortingExtractorInterface=OpenEphysSortingExtractorInterface
    )