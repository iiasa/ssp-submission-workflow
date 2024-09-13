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
    processed_df = process(
        df,
        dsd,
        processor=RegionProcessor.from_directory(
            path=here / "mappings",
            dsd=dsd,
        ),
    )
    if FOUND_MAGICC:
        magicc_processor = MAGICCProcessor(
            run_type="complete",
            magicc_worker_number=8,
            magicc_variables=[
                "AR6 climate diagnostics|Atmospheric Concentrations*"
                "AR6 climate diagnostics|Exceedance Probability*"
                "AR6 climate diagnostics|Effective Radiative Forcing*"
                "AR6 climate diagnostics|Surface Temperature*",
                "AR6 climate diagnostics|Infilled*",
                "AR6 climate diagnostics|Harmonized*",
            ],
        )
        try:
            return magicc_processor.apply(processed_df)
        except Exception as e:
            log.warning(
                (
                    "Error with MAGICC processing, repeat processing without MAGICC, "
                    f"details: {e}"
                )
            )
    return processed_df
