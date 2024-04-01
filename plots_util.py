import numpy as np 
import xarray as xr
import matplotlib.pyplot as plt
import MJO_E3SM_util as mjo


def get_comp_4(comp):
    comp5 = {}
    comp5['mse'] = comp['dse'] + comp['qlv']
    comp5['tendency'] = comp['dtdse'] + comp['dtqlv']
    comp5['crmpbl'] = comp['crm_dse'] + comp['crm_qlv'] + comp['pbl_dse'] + comp['pbl_qlv']
    comp5['dyn'] = comp['dyn_dse'] + comp['dyn_qlv']
    comp5['qr'] = comp['qr']

    return comp5

def get_comp_5_new(comp):
    comp8 = {}
    comp8['mse'] = comp['dse'] + comp['qlv']
    comp8['tendency'] = comp['dtdse'] + comp['dtqlv']
    comp8['tendency_d'] = comp['dtdse'] 
    comp8['tendency_m'] = comp['dtqlv']
    comp8['crmpbl_d'] = comp['crm_dse'] + comp['pbl_dse'] 
    comp8['crmpbl_m'] = comp['crm_qlv'] + comp['pbl_qlv']
    comp8['dyn_d'] = comp['dyn_dse'] 
    comp8['dyn_m'] = comp['dyn_qlv']
    comp8['qr'] = comp['qr']

    return comp8



