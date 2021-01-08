from nwb_conversion_tools import NWBConverter

from .blackrockinterface import BlackrockInterface


class BlackrockNWBConverter(NWBConverter):
    data_interface_classes = dict(
        BlackrockInterface=BlackrockInterface
    )

    def get_metadata(self):
        metadata = super().get_metadata()
        return metadata