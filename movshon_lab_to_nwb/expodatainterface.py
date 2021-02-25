from nwb_conversion_tools.basedatainterface import BaseDataInterface
from pynwb import NWBFile

from .utils_expo import process_blocksV2, process_passesV2


class ExpoDataInterface(BaseDataInterface):
    """Conversion class for FRET data."""

    @classmethod
    def get_source_schema(cls):
        """Return a partial JSON schema indicating the input arguments and their types."""
        source_schema = super().get_source_schema()
        source_schema.update(
            required=[],
            properties=dict(
                expo_file=dict(
                    type="string",
                    format="file",
                    description="path to xml file containing expo data"
                )
            )
        )
        return source_schema

    @classmethod
    def get_conversion_options_schema(cls):
        """Compile conversion option schemas from each of the data interface classes."""
        conversion_options_schema = super().get_conversion_options_schema()
        conversion_options_schema.update(
            required=[],
            properties=dict(
                convert_expo=dict(
                    type="boolean",
                    description="Whether to convert Expo data to NWB or not"
                )
            )
        )
        return conversion_options_schema


    def run_conversion(self, nwbfile: NWBFile, metadata: dict, convert_expo: bool=False):
        """
        Run conversionfor this data interface.

        Parameters
        ----------
        nwbfile : NWBFile
        metadata : dict
        """
        if not convert_expo:
            print('Expo data not included in conversion')
            return

        print(f'Adding expo data...')
        expo_file = self.source_data['expo_file']
        if expo_file.endswith('.xml'):
            trials = process_passesV2(expo_file)
            blocks = process_blocksV2(expo_file)
        else:
            raise OSError(f"Expo file should be of xml type. File used: {expo_file}")

        # Add trials intervals values only if no trials data exists in nwbfile
        if nwbfile.trials is not None:
            print('Trials already exist in current nwb file. Expo trials intervals not added.')
        else:
            # Get parameters names to form trials columns
            col_names = list()
            for params in blocks.values():
                for p in params.keys():
                    if p not in col_names:
                        col_names.append(p)

            # Add trials columns
            for c in col_names:
                nwbfile.add_trial_column(
                    name=c,
                    description='no description'
                )
                
            # Add trials rows
            for tr in trials.values():
                trial_dict = dict(
                    start_time=tr['StartTime'], 
                    stop_time=tr['EndTime']
                )
                for c in col_names:
                    trial_dict[c] = blocks[str(tr['BlockID'])].get(c, '')
                    
                nwbfile.add_trial(**trial_dict)