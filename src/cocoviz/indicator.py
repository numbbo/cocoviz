"""Functions and data structures for dealing with performance indicators"""

import dataclasses

from typing import Union

from .exceptions import UnknownIndicatorException


KNOWN_INDICATORS = dict()


@dataclasses.dataclass(eq=True, frozen=True)
class Indicator:
    """Description of a performance indicator

    Attributes
    ----------
    name : str
        Name of the quality indicator. Must match the column name in the Results 
        object.
    display_name : str
        String used as name of the indicator in plots and error messages
    larger_is_better : bool, default = True
        True if larger values of the indicator are better, False otherwise.
    """
    name: str
    display_name: str = None
    larger_is_better: bool = True

    def __post_init__(self):
        if self.display_name is None:
            self.display_name = self.name


def register(ind: Indicator):
    """Register a new performance indicator

    cocoviz has a global list of know performance indicators with their
    associated metadata. Using this function, you can add additional indicators
    so that you do not have to specify their properties every time.

    Parameters
    ----------
    ind : Indicator
        Indicator to add to list of known indicators
    """
    KNOWN_INDICATORS[ind.name] = ind


def deregister(ind: Union[Indicator, str]):
    """_summary_

    Parameters
    ----------
    ind : Indicator or str
        Indicator to remove from list of known indicators

    Raises
    ------
    NotImplementedError
        when `ind` is neither a string nor an instance of Indicator
    """
    if isinstance(ind, str):
        del KNOWN_INDICATORS[ind]
    elif isinstance(ind, Indicator):    
        del KNOWN_INDICATORS[ind.name]
    else:
        raise NotImplementedError()


def resolve(indicator) -> Indicator:
    """Resolve something to an Indicator using the previously registered indicators

    Parameters
    ----------
    indicator : any
        Thing to resolve into an Indicator instance

    Returns
    -------
    Indicator
        Instance of Indicator for `indicator`        

    Raises
    ------
    UnknownIndicatorException
        Raised when `indicator` cannot be resolved.
    """
    if isinstance(indicator, Indicator):
        return indicator

    try:
        return KNOWN_INDICATORS[indicator]
    except KeyError:
        raise UnknownIndicatorException(indicator)    


## Register some common and not so common performance indicators
register(Indicator("hypervolume", "Hypervolume", larger_is_better=True))
register(Indicator("Hypervolume", "Hypervolume", larger_is_better=True))
register(Indicator("hv", "Hypervolume", larger_is_better=True))
register(Indicator("uhvi", "UHVI", larger_is_better=True))
register(Indicator("time", "Time", larger_is_better=False))
register(Indicator("r2", "R2", larger_is_better=False))
register(Indicator("igd+", "IGD+", larger_is_better=False))
register(Indicator("igdplus", "IGD+", larger_is_better=False))
register(Indicator("igdp", "IGD+", larger_is_better=False))

