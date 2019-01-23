#!/usr/bin/env python
"""Make the gammapy.org static webpage.

This is very much work in progress.
Probably we should add a static website build step.
"""
import logging
import json
import os
from pathlib import Path
import click
import hashlib

log = logging.getLogger(__name__)


def hashmd5(path):
    md5_hash = hashlib.md5()
    with open(path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            md5_hash.update(byte_block)
    return md5_hash.hexdigest()


class Dataset:
    """Dataset base class.

    The Dataset class has a local_repo property where to scan the content
    and a base_url to build access links for each file.

    A dataset has a name as identifier.
    It also has a description and list of files, each file has a given URL
    and a path that tells you where the file will be placed when downloaded.

    If you want to add a dataset, make a new class and add it to the list below.
    """

    base_url = "https://github.com/gammapy/gammapy-extra/raw/master/datasets"
    local_repo = Path(os.environ["GAMMAPY_EXTRA"]) / "datasets"

    @property
    def record(self):
        return {
            "name": self.name,
            "description": self.description,
            "files": list(self.files),
        }

    @property
    def files(self):
        for path in (self.local_repo / self.name).glob("**/*.*"):
            if not path.name.startswith('.'):
                urlpath = path.as_posix().replace(self.local_repo.as_posix(), "")
                filesize = os.path.getsize(path)
                md5 = hashmd5(path)
                yield {"path": urlpath[1:], "url": self.base_url + urlpath, "filesize": filesize, "hashmd5": md5}


class DatasetCTA1DC(Dataset):
    name = "cta-1dc"
    description = "tbd"


class DatasetDarkMatter(Dataset):
    name = "dark_matter_spectra"
    description = "tbd"


class DatasetCatalogs(Dataset):
    name = "catalogs"
    description = "tbd"


class DatasetFermi2FHL(Dataset):
    name = "fermi_2fhl"
    description = "tbd"


class DatasetFermi3FHL(Dataset):
    name = "fermi_3fhl"
    description = "tbd"


class DatasetFermiSurvey(Dataset):
    name = "fermi_survey"
    description = "tbd"


class DatasetHESSDL3DR1(Dataset):
    name = "hess-dl3-dr1"
    description = "tbd"


class DatasetImages(Dataset):
    name = "images"
    description = "tbd"


class DatasetEBL(Dataset):
    name = "ebl"
    description = "tbd"


class DatasetJointCrab(Dataset):
    name = "joint-crab"
    description = "tbd"

    base_url = "https://github.com/open-gamma-ray-astro/joint-crab/raw/master/results/spectra"
    local_repo = Path(os.environ["JOINT_CRAB"]) / 'results' / 'spectra'
    files = []

    for path in (local_repo).glob("**/*.*"):
        if not path.name.startswith('.'):
            jsonpath = str(path).replace(str(local_repo), 'joint-crab/spectra')
            urlpath = path.as_posix().replace(local_repo.as_posix(), "")
            filesize = os.path.getsize(path)
            md5 = hashmd5(path)
            files.append({"path": jsonpath, "url": base_url + urlpath, "filesize": filesize, "hashmd5": md5})


class DatasetGammaCat(Dataset):
    name = "gamma-cat"
    description = "tbd"

    base_url = "https://github.com/gammapy/gamma-cat/raw/master"
    local_repo = Path(os.environ["GAMMA_CAT"])
    files = []

    pathlist = [str(Path('output') / 'gammacat.fits.gz')]

    for item in pathlist:
        path = local_repo / item
        jsonpath = str(Path('gamma-cat') / Path(item).name)
        urlpath = path.as_posix().replace(local_repo.as_posix(), "")
        filesize = os.path.getsize(path)
        md5 = hashmd5(path)
        files.append({"path": jsonpath, "url": base_url + urlpath, "filesize": filesize, "hashmd5": md5})


class DatasetFermiLat(Dataset):
    name = "fermi-lat-data"
    description = "tbd"

    base_url = "https://github.com/gammapy/gammapy-fermi-lat-data/raw/master"
    local_repo = Path(os.environ["GAMMAPY_FERMI_LAT_DATA"])
    files = []

    pathlist = [
        str(Path('3fhl') / 'allsky' / 'fermi_3fhl_events_selected.fits.gz'),
        str(Path('3fhl') / 'allsky' / 'fermi_3fhl_exposure_cube_hpx.fits.gz'),
        str(Path('3fhl') / 'allsky' / 'fermi_3fhl_psf_gc.fits.gz'),
        str(Path('isodiff') / 'iso_P8R2_SOURCE_V6_v06.txt')
    ]

    for item in pathlist:
        path = local_repo / item
        jsonpath = str(Path('fermi_3fhl') / Path(item).name)
        urlpath = path.as_posix().replace(local_repo.as_posix(), "")
        filesize = os.path.getsize(path)
        md5 = hashmd5(path)
        files.append({"path": jsonpath, "url": base_url + urlpath, "filesize": filesize, "hashmd5": md5})


class DatasetFermi3FHLGC(Dataset):
    name = "fermi-3fhl-gc"
    description = "Prepared Fermi-LAT 3FHL dataset of the Galactic center region"
    local_repo = Path(os.environ["GAMMAPY_FERMI_LAT_DATA"])
    base_url = "https://github.com/gammapy/gammapy-fermi-lat-data/raw/master"
    files = []
    filenames = [
        "fermi-3fhl-gc-background.fits.gz",
        "fermi-3fhl-gc-background-cube.fits.gz",
        "fermi-3fhl-gc-counts.fits.gz",
        "fermi-3fhl-gc-counts-cube.fits.gz",
        "fermi-3fhl-gc-events.fits.gz",
        "fermi-3fhl-gc-exposure-cube.fits.gz",
        "fermi-3fhl-gc-exposure.fits.gz",
        "fermi-3fhl-gc-psf.fits.gz",
        "fermi-3fhl-gc-psf-cube.fits.gz",
        "gll_iem_v06_gc.fits.gz",
    ]

    for filename in filenames:
        path = local_repo / "3fhl/galactic-center" / filename
        jsonpath = str(Path('fermi-3fhl-gc') / filename)
        urlpath = path.as_posix().replace(local_repo.as_posix(), "")
        filesize = os.path.getsize(path)
        md5 = hashmd5(path)
        files.append({"path": jsonpath, "url": base_url + urlpath, "filesize": filesize, "hashmd5": md5})


class DatasetIndex:
    path = "download/data/gammapy-data-index.json"
    datasets = [
        DatasetCTA1DC,
        DatasetDarkMatter,
        DatasetCatalogs,
        DatasetFermi3FHL,
        DatasetHESSDL3DR1,
        DatasetImages,
        DatasetJointCrab,
        DatasetEBL,
        DatasetGammaCat,
        DatasetFermi3FHLGC
    ]

    def make(self):
        records = list(self.make_records())
        txt = json.dumps(records, indent=True)
        log.info(f"Writing {self.path}")
        Path(self.path).write_text(txt)

    def make_records(self):
        for cls in self.datasets:
            yield cls().record


@click.group()
def cli():
    """Make the gammapy.org webpage."""
    logging.basicConfig(level="INFO")


@cli.command("all")
@click.pass_context
def cli_all(ctx):
    """Run all steps"""
    ctx.invoke(cli_dataset_index)


@cli.command("dataset-index")
def cli_dataset_index():
    """Generate data index file"""
    DatasetIndex().make()


if __name__ == "__main__":
    cli()
