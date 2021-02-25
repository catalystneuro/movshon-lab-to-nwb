import xml.etree.ElementTree as ET
from collections import defaultdict


def process_blocksV2(expo_file):
    """Extract block parameters
    Go through the XML extracting information from <block> subsections that
    define any given expo program
    
    Parameters
    ----------
    expo_file: str

    Returns
    ----------
    output: dict
    """
    tree = ET.parse(expo_file)
    blocks = tree.findall("Blocks/Block")
    blocks_dict = dict()
    for b in blocks:
        routines_dict = dict()
        for r in b:
            ir = r.get('ID')
            routines_dict[f'routine_{ir}_name'] = r.get('Name')
            routines_dict[f'routine_{ir}_label'] = r.get('Label')
            for params in r:
                param_name = params.get('Name').lower().replace(' ', '')
                for pk, pv in params.items():
                    if pk != 'Name':
                        routines_dict[f'routine_{ir}_{param_name}_{pk.lower()}'] = pv
        blocks_dict[f"{b.get('ID')}"] = routines_dict

    return blocks_dict


def process_passesV2(expo_file):
    """
    Extract pass parameters. Go through the XML extracting information from <pass> subsections that
    define any given expo program

    Parameters
    ----------
    expo_file: str

    Returns
    ----------
    passes_dict: dict
    """
    tree = ET.parse(expo_file)
    passes = tree.findall("Passes/Pass")
    passes_dict = dict()
    for pass_elements in passes:
        event_store = defaultdict(list)
        id = int(pass_elements.get('ID'))
        passes_dict[id] = dict()
        #find core information about passes (BlockIDs,Start/End times, Pass, Slot, Block IDs)
        for pass_key, pass_value in pass_elements.items():
            if pass_key in ['StartTime', 'EndTime']:
                # start and end times are recorded with 0.1 ms resolution. This transforms them to seconds
                passes_dict[id][pass_key] = int(pass_value)/10000
            elif pass_key == 'ID':
                continue
            else:
                # -- PL: These are ALL integer values, so make them as such - i.e. typecast as INT!
                passes_dict[id][pass_key] = int(pass_value)
        #now find <event> information, like specific orientation etc.
        for events in pass_elements:
            for event_key, event_value in events.items():
                event_store[event_key].append(event_value)
        passes_dict[id]['events'] = event_store

    return passes_dict

