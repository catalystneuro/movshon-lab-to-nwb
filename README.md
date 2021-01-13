# movshon-lab-to-nwb

NWB conversion scripts and tutorials. A collaboration with [Movshon Lab](https://www.cns.nyu.edu/labs/movshonlab/).

- Blackrock processing through SpikeInterface
- Blackrock conversion to NWB
- OpenEphys processing through SpikeInterface
- OpenEphys conversion to NWB
- SpikeGLX processing through SpikeInterface
- SpikeGLX conversion to NWB

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

# Use
After activating the correct environment, the conversion function can be used in different forms:

**1. Imported and run from a python script:** <br/>

<br/>

**2. Command line:** <br/>

<br/>

**3. Graphical User Interface:** <br/>
To use the GUI, just run the auxiliary function `nwb_gui.py` from terminal:
```
$ python nwb_gui.py
```
The GUI eases the task of editing the metadata of the resulting `.nwb` file, it is integrated with the conversion module (conversion on-click) and allows for visually exploring the data in the end file with [nwb-jupyter-widgets](https://github.com/NeurodataWithoutBorders/nwb-jupyter-widgets).

<br/>

**4. Tutorial:** <br/>
At [tutorials](https://github.com/catalystneuro/movshon-lab-to-nwb/tree/main/tutorials) you can also find Jupyter notebooks with the step-by-step process of conversion.