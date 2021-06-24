# movshon-lab-to-nwb

[![PyPI version](https://badge.fury.io/py/movshon-lab-to-nwb.svg)](https://badge.fury.io/py/movshon-lab-to-nwb)

NWB conversion scripts and tutorials. A collaboration with [Movshon Lab](https://www.cns.nyu.edu/labs/movshonlab/).

- Blackrock processing through SpikeInterface
- Blackrock conversion to NWB
- OpenEphys processing through SpikeInterface
- OpenEphys conversion to NWB
- SpikeGLX processing through SpikeInterface
- SpikeGLX conversion to NWB
- Expo conversion to NWB

# Install
To clone the repository and set up a conda environment, do:
```
$ git clone https://github.com/catalystneuro/movshon-lab-to-nwb
$ conda env create -f movshon-lab-to-nwb/make_env.yml
$ source activate env_movshon
```

Alternatively, to install directly in an existing environment:
```
$ pip install movshon-lab-to-nwb
```


# Spike sorting
SpikeInterface examples for each experiment can be found in [tutorials](https://github.com/catalystneuro/movshon-lab-to-nwb/tree/main/tutorials).

Check SpikeInterface [documentation](https://spikeinterface.readthedocs.io/en/latest/sortersinfo.html) for a list of available spike sorters and how to install them.


# NWB conversion
After activating the correct environment, the conversion function can be used in different forms:

**1. Run conversion script from Jupyter notebooks:** <br/>
Detailed and simple examples for each experiment can be found in [tutorials](https://github.com/catalystneuro/movshon-lab-to-nwb/tree/main/tutorials).

**2. Run conversion script from command line:** <br/>
You will find conversion scripts for each experiment in [scripts](https://github.com/catalystneuro/movshon-lab-to-nwb/tree/main/scripts). If running them from command line, you can get the available arguments with:
```shell
$ python convert_blackrock.py --help
```

Example for Blackrock:
```shell
$ python convert_blackrock.py 
--file_recording_raw data_blackrock/XX_LE_textures_20191128_002.ns6 
--file_recording_processed data_blackrock/XX_LE_textures_20191128_002.ns3 
--file_sorting data_blackrock/XX_LE_textures_20191128_002.nev 
--file_metadata metadata_example.yml
```

**3. Graphical User Interface:** <br/>
To use the GUI, first install [nwb-web-gui](https://github.com/catalystneuro/nwb-web-gui):
```shell
$ pip install nwb-web-gui
```

The GUI can be run from the terminal:
```shell
$ nwbgui-movshon [experiment_name]
```
Current options for experiment names are: `blackrock`, `openephys`, and `spikeglx`. The NWB Web GUI should open in your browser. If it does not open automatically (and no error messages were printed in your terminal), just open your browser and navigate to `localhost:5000`.

The GUI eases the task of editing the metadata of the resulting `nwb` file, it is integrated with the conversion module (conversion on-click) and allows for quick visual exploration the data in the end file with [nwb-jupyter-widgets](https://github.com/NeurodataWithoutBorders/nwb-jupyter-widgets).
