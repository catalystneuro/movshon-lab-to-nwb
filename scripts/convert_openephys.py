from movshon_lab_to_nwb import MovshonOpenEphysNWBConverter
from nwb_conversion_tools.utils.json_schema import dict_deep_update
from nwb_conversion_tools.utils.metadata import load_metadata_from_file


def main(output_file, dir_oephys, file_expo, file_ttl, file_metadata):
    # Source data
    source_data = dict(
        OpenEphysRecordingExtractorInterface=dict(folder_path=str(dir_oephys)),
        ExpoDataInterface=dict(
            expo_file=str(file_expo),
            ttl_file=str(file_ttl)
        )
    )

    # Initialize converter
    converter = MovshonOpenEphysNWBConverter(source_data=source_data)

    # Get metadata from source data and modify any values you want
    metadata = converter.get_metadata()
    if file_metadata:
        m = load_metadata_from_file(file_metadata)
        metadata = dict_deep_update(metadata, m)
        converter.validate_metadata(metadata)

    # Get conversion options and modify any values you want
    conversion_options = converter.get_conversion_options()

    # Run conversion
    converter.run_conversion(
        metadata=metadata, 
        nwbfile_path=output_file, 
        save_to_file=True,
        overwrite=True,
        conversion_options=conversion_options
    )


def parse_arguments():
    """
    Command line shortcut to run conversion script.
    Usage example:
    $ python convert_openephys.py 
      --output path_to/output.nwb
      --dir_oephys path_to/openephys_directory/
      --file_expo path_to/file_expo.xml
      --file_ttl path_to/file_ttl.continuous
      --file_metadata path_to/metadata.yml
    """
    import argparse

    parser = argparse.ArgumentParser(
        description='Convert OpenEphys data to NWB',
    )

    parser.add_argument(
        "--output",
        default='output_openephys.nwb',
        help="Output NWB file."
    )
    parser.add_argument(
        "--dir_oephys",
        default=None,
        help="Path to the directory containing OpenEphys data."
    )
    parser.add_argument(
        "--file_expo",
        default=None,
        help="Path to the file containing Expo data."
    )
    parser.add_argument(
        "--file_ttl",
        default=None,
        help="Path to the file containing ttl data."
    )
    parser.add_argument(
        "--file_metadata",
        default=None,
        help="Path to the YAML or JSON file containing session metadata."
    )

    # Parse arguments
    args = parser.parse_args()

    return args


# Command line call
if __name__ == "__main__":
    run_args = parse_arguments()
    args = dict(
        output_file=run_args.output,
        dir_oephys=run_args.dir_oephys,
        file_expo=run_args.file_expo,
        file_ttl=run_args.file_ttl,
        file_metadata=run_args.file_metadata,
    )

    main(**args)