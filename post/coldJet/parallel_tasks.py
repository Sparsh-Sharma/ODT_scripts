# parallel_tasks.py

import os
from data_py import data_py
from basic_stats import basic_stats
from pdfs import get_pdfs
from uvel import uvel, plot_uvel
from fwhm import fwhm, plot_fwhm_uvel
from eddyInfo import eddyMaps
from eddyInfo import eddyStats
from grid_stats import get_dxpdfs
from logTKEdiss import logTKEdiss
from TKEdiss import TKEdiss

def perform_basic_tasks(DI):
    if not os.path.exists(DI['cdir'] + "data_py/"):
        data_py(DI)

    basic_stats(DI, nfbins=60, do_yt=True)

    get_pdfs(DI, nbins=200)

def process_velocity_profiles(DI):
    uvel(DI, profName="uvel")

    plot_uvel(DI)

    fwhm(DI, profName="uvel")
    plot_fwhm_uvel(DI)

def perform_remaining_tasks(DI):
    eddyMaps(DI)
    eddyStats(DI)

    logTKEdiss(DI, profName="logTKEdiss")
    TKEdiss(DI, profName="TKEdiss")

    get_dxpdfs(DI, nbins=60)
