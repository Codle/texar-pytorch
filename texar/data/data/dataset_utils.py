from typing import Dict, Any, Optional


class Batch:
    r"""Wrapper over Python dictionaries representing a batch. This provides a
    common interface with :class:`~texar.data.data.dataset_utils.Batch` that
    allows accessing via attributes.
    """

    def __init__(self, batch_size: int, batch: Optional[Dict[str, Any]] = None,
                 **kwargs):
        self.batch_size = batch_size
        self._batch = batch or {}
        self._batch.update(kwargs)

    def __getattr__(self, item):
        if item not in super().__getattribute__('_batch'):
            raise AttributeError
        return self._batch[item]

    def __getitem__(self, item):
        return self._batch[item]

    def __len__(self) -> int:
        return self.batch_size


class FieldBatch(Batch):
    r"""Defines a batch of examples with support for multiple fields. This is
    a simplified version of `torchtext.data.Batch`, with all the useless stuff
    removed.
    """

    def __init__(self, data=None, dataset=None, device=None):
        """Create a Batch from a list of examples."""
        if data is not None:
            batch_size = len(data)
            _batch_dict = {}
            for (name, field) in dataset.fields.items():
                if field is not None:
                    batch = [getattr(x, name) for x in data]
                    _batch_dict[name] = field.process(batch, device=device)
            super().__init__(batch_size, _batch_dict)
        else:
            super().__init__(0)
