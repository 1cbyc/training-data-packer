from pathlib import Path
from typing import Any

from loguru import logger

from training_data_packer.metadata import Metadata, read_metadata
from training_data_packer.metadata.defaults import PREFIX_DEFAULT, RUBBER_DEFAULT
from training_data_packer.metadata.schema import Validator
from training_data_packer.processor.sample.sampler import read_sampler_fn


def process(collection_dir: Path) -> bool:
    metadata_file = collection_dir / "metadata.yaml"
    if not metadata_file.exists():
        logger.error(f"Metadata file does not exist in {collection_dir}")
        return False
    try:
        metadata = read_metadata(collection_dir.joinpath("metadata.yaml"))
        metadata["_internal"]["mode"] = "lint"
        check_all_release_parts(metadata)
    except ValueError:
        return False
    return True


def check_all_release_parts(metadata: Metadata) -> None:
    for part in metadata.get_all_part_names("release"):
        if "'" in part:
            part_path = f'release."{part}"'
        else:
            part_path = f"release.'{part}'"
        try:
            _check_release_part(part_path, metadata)
        except ValueError as e:
            logger.error(f"Part {part_path} failed validation. Reason: {e}")
            raise e


def _check_release_part(part_path: str, metadata: Metadata) -> None:
    part_settings = metadata.get_part(part_path)
    Validator().validate_release_part(part_settings)
    _check_sample_config(part_path, part_settings)
    _check_pack_config(part_path, part_settings)


def _check_pack_config(name: str, part: dict[str, Any]):
    match part["pack"]:
        case "flat":
            if "prefix" not in part:
                logger.warning(
                    f"In {name} setting `prefix` is recommended when `pack` has value `flat` to get unique names."
                    f"`prefix` default to `{PREFIX_DEFAULT}`."
                )
        case "tree":
            pass
        case _:
            raise ValueError(f"In {name} pack has an unknown value: {part['pack']}")


def _check_sample_config(name: str, part: dict[str, Any]):
    match part["sample"]:
        case "full":
            pass
        case "random":
            if "rubber" not in part:
                logger.warning(
                    f"In {name} setting `rubber` is recommended when `sample` has value `random`."
                    f"`rubber` default to `{RUBBER_DEFAULT}`."
                )
            if "budget" not in part:
                raise ValueError(f"In {name} `sample` is `random` but `budget` is missing for part {name}.")
        case "dynamic":
            if "filter" not in part:
                raise ValueError(f"In {name} sample is dynamic but filter is missing for part {name}.")
            if "parameters" not in part:
                raise ValueError(f"In {name} sample is dynamic but parameters is missing for part {name}.")
            try:
                read_sampler_fn(part["filter"])
            except Exception as e:
                raise ValueError(f"Fail to read sampler function for part {name}: {e}") from e
        case "wds+register":
            pass
        case _:
            raise ValueError(f"In {name} sample has an unknown value: {part['sample']}")
