import logging
import json

logger = logging.getLogger(__name__)

class OuraModel:
    _KEYS = []

    def __str__(self):
        return ", ".join( ["{}={}".format(k, getattr(self, k)) for k in self._KEYS ] )


def from_json(raw_json, typename: OuraModel):

    json_dict = json.loads(raw_json)
    obj = typename()

    for k in obj._KEYS:
        if k in json_dict.keys():
            setattr(obj, k, json_dict[k])
        else:
            setattr(obj, k, None)
            logger.warning("Expected property missing from json response. property={}, class={}".format(k, typename.__class__.__name__))
    
    return obj