from movshon_lab_to_nwb import MovshonBlackrockNWBConverter
from nwb_conversion_tools.utils.json_schema import dict_deep_update
from nwb_conversion_tools.utils.metadata import load_metadata_from_file


def main(output_file, file_recording_raw, file_recording_processed, file_sorting, file_metadata):
    # Source data
    source_data = dict(
        BlackrockRaw=dict(filename=file_recording_raw),
        BlackrockProcessed=dict(filename=file_recording_processed),
        BlackrockSorting=dict(
            filename=file_sorting,
            nsx_to_load=6
        )
    )

    # Initialize converter
    converter = MovshonBlackrockNWBConverter(source_data=source_data)

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
    $ python convert_blackrock.py 
      --output path_to/output.nwb
      --file_recording_raw path_to/raw_data.ns6
      --file_recording_processed path_to/processed_data.ns3 
      --file_sorting path_to/sorted_data.nev
      --file_metadata path_to/metadata.yml
    """
    import argparse

    parser = argparse.ArgumentParser(
        description='Convert Blackrock data to NWB',
    )

    parser.add_argument(
        "--output",
        default='output_blackrock.nwb',
        help="Output NWB file."
    )
    parser.add_argument(
        "--file_recording_raw",
        default=None,
        help="Path to the file containing raw Blackrock data."
    )
    parser.add_argument(
        "--file_recording_processed",
        default=None,
        help="Path to the file containing processed Blackrock data."
    )
    parser.add_argument(
        "--file_sorting",
        default=None,
        help="Path to the file containing the spike sorted Blackrock data."
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
        file_recording_raw=run_args.file_recording_raw,
        file_recording_processed=run_args.file_recording_processed,
        file_sorting=run_args.file_sorting,
        file_metadata=run_args.file_metadata,
    )

    main(**args)