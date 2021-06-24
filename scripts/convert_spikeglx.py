from movshon_lab_to_nwb import MovshonSpikeglxNWBConverter
from nwb_conversion_tools.utils.json_schema import dict_deep_update
from nwb_conversion_tools.utils.metadata import load_metadata_from_file


def main(output_file, file_raw, file_lfp, file_expo, file_ttl, file_metadata):
    # Source data
    source_data = dict(
        SpikeGLXRaw=dict(file_path=str(file_raw)),
        SpikeGLXLFP=dict(file_path=str(file_lfp)),
        ExpoDataInterface=dict(
            expo_file=str(file_expo),
            ttl_file=str(file_ttl)
        )
    )

    # Initialize converter
    converter = MovshonSpikeglxNWBConverter(source_data=source_data)

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
      --file_raw path_to/file_raw.ap.bin
      --file_lfp path_to/file_lfp.lf.bin
      --file_expo path_to/file_expo.xml
      --file_ttl path_to/file_raw.ap.bin
      --file_metadata path_to/metadata.yml
    """
    import argparse

    parser = argparse.ArgumentParser(
        description='Convert SpikeGLX data to NWB',
    )

    parser.add_argument(
        "--output",
        default='output_spikeglx.nwb',
        help="Output NWB file."
    )
    parser.add_argument(
        "--file_raw",
        default=None,
        help="Path to the directory containing SpikeGLX raw data."
    )
    parser.add_argument(
        "--file_lfp",
        default=None,
        help="Path to the directory containing SpikeGLX lfp data."
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
        file_raw=run_args.file_raw,
        file_lfp=run_args.file_lfp,
        file_expo=run_args.file_expo,
        file_ttl=run_args.file_ttl,
        file_metadata=run_args.file_metadata,
    )

    main(**args)