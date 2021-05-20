from nwb_conversion_tools import (
    NWBConverter, BlackrockRecordingExtractorInterface, BlackrockSortingExtractorInterface,
    OpenEphysRecordingExtractorInterface, OpenEphysSortingExtractorInterface,
    SpikeGLXRecordingInterface
)

from .expodatainterface import ExpoDataInterface


class MovshonBlackrockNWBConverter(NWBConverter):
    data_interface_classes = dict(
        BlackrockRaw=BlackrockRecordingExtractorInterface, 
        BlackrockProcessed=BlackrockRecordingExtractorInterface, 
        BlackrockSorting=BlackrockSortingExtractorInterface
    )

    def get_conversion_options(self):
        conversion_options = dict(
            BlackrockRaw=dict(
                write_as='raw', 
                es_key='ElectricalSeries_raw', 
                stub_test=False
            ),
            BlackrockProcessed=dict(
                write_as='processed', 
                es_key='ElectricalSeries_processed', 
                stub_test=False
            )
        )
        return conversion_options


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


class MovshonExpoNWBConverter(NWBConverter):
    data_interface_classes = dict(
        ExpoDataInterface=ExpoDataInterface
    )