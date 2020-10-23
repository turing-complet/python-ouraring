import logging
import json

logger = logging.getLogger(__name__)


class OuraModel:
    # TODO factor out common keys, like "summary_date"
    _KEYS = []

    def __init__(self, json_raw=None, json_parsed=None):
        obj = json_parsed if json_parsed is not None else json.loads(json_raw)
        set_attrs(self, obj)

    def __str__(self):
        return ", ".join(["{}={}".format(k, getattr(self, k)) for k in self._KEYS])


def set_attrs(instance, lookup):
    [setattr(instance, k, lookup[k]) for k in instance._KEYS if k in lookup.keys()]


def from_dict(response_dict, typename: OuraModel):
    obj = typename()

    for k in obj._KEYS:
        if k in response_dict.keys():
            setattr(obj, k, response_dict[k])
        else:
            setattr(obj, k, None)
            logger.warning(
                "Expected property missing from json response. property={}, class={}".format(
                    k, typename.__class__.__name__
                )
            )

    return obj


def from_json(raw_json, typename: OuraModel):

    json_dict = json.loads(raw_json)
    return from_dict(json_dict, typename)
