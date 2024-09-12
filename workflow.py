import logging
import sys
from pathlib import Path
import pyam
from nomenclature import DataStructureDefinition, RegionProcessor, process


try:
    from climate_processor import MAGICCProcessor

    FOUND_MAGICC = True
except ImportError:
    FOUND_MAGICC = False


logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] %(message)s")
log = logging.getLogger()
log.handlers.clear()
consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(logFormatter)
log.addHandler(consoleHandler)


here = Path(__file__).absolute().parent


def main(df: pyam.IamDataFrame) -> pyam.IamDataFrame:
    """Project/instance-specific workflow for scenario processing"""

    # Run the validation and region-processing
    dsd = DataStructureDefinition(here / "definitions")
    region_processor = RegionProcessor.from_directory(
        path=here / "mappings",
        dsd=dsd,
    )
    if FOUND_MAGICC:
        magicc_processor = MAGICCProcessor(
            run_type="complete",
            magicc_worker_number=8,
        )
        try:
            return process(
                df,
                dsd,
                processor=[region_processor, magicc_processor],
            )
        except Exception as e:
            log.warning(
                (
                    "Error with MAGICC processing, repeat processing without MAGICC, "
                    f"details: {e}"
                )
            )
    return process(df, dsd, processor=region_processor)
