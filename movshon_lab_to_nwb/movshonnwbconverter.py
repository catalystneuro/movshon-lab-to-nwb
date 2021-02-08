from nwb_conversion_tools import NWBConverter, BlackrockRecordingExtractorInterface, BlackrockSortingExtractorInterface


class MovshonBlackrockNWBConverter(NWBConverter):
    data_interface_classes = dict(
        BlackrockRecordingExtractorInterface=BlackrockRecordingExtractorInterface, 
        BlackrockSortingExtractorInterface=BlackrockSortingExtractorInterface
    )