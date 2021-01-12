from nwb_conversion_tools import NWBConverter, BlackrockRecordingInterface


class MovshonNWBConverter(NWBConverter):
    data_interface_classes = dict(
        BlackrockInterface=BlackrockRecordingInterface
    )