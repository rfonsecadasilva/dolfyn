from dolfyn.test import test_read_adp as tr, test_adv as tv
from dolfyn.test.base import load_ncdata as load, save_ncdata as save
from xarray.testing import assert_allclose
import numpy as np
from dolfyn import VelBinner
import dolfyn.adv.api as avm

class adv_setup():
    def __init__(self, tv):
        self.dat1 = tv.dat
        self.dat2 = tv.dat_imu
        self.avg_tool = VelBinner(self.dat1.fs, self.dat1.fs)
        
class adp_setup():
    def __init__(self, tr):
        self.dat = tr.dat_sig
        self.avg_tool = VelBinner(self.dat.fs*20, self.dat.fs)
        
        
# test each of VelBinner's functions on an ADV and ADCP
def test_do_avg(make_data=False):
    dat_vec = adv_setup(tv)
    adat_vec = dat_vec.avg_tool.do_avg(dat_vec.dat1)
    
    dat_sig = adp_setup(tr)
    adat_sig = dat_sig.avg_tool.do_avg(dat_sig.dat)
    
    if make_data:
        save(adat_vec, 'ADV_average.nc')
        save(adat_sig, 'ADCP_average.nc')
        return
    
    saved_adat_vec = load('ADV_average.nc')
    saved_adat_sig = load('ADCP_average.nc')
    
    assert_allclose(adat_vec, saved_adat_vec, atol=1e-5)
    assert_allclose(adat_sig, saved_adat_sig, atol=1e-5)
    
    
def test_do_var(make_data=False):
    dat_vec = adv_setup(tv)
    vdat_vec = dat_vec.avg_tool.do_var(dat_vec.dat1)
    
    dat_sig = adp_setup(tr)
    vdat_sig = dat_sig.avg_tool.do_var(dat_sig.dat)
    
    if make_data:
        save(vdat_vec, 'ADV_variance.nc')
        save(vdat_sig, 'ADCP_variance.nc')
        return
    
    saved_vdat_vec = load('ADV_variance.nc')
    saved_vdat_sig = load('ADCP_variance.nc')
    
    assert_allclose(vdat_vec, saved_vdat_vec, atol=1e-5)
    assert_allclose(vdat_sig, saved_vdat_sig, atol=1e-5)
    
    
def test_calc_coh(make_data=False):
    dat_vec = adv_setup(tv)
    coh = dat_vec.avg_tool.calc_coh(dat_vec.dat1.vel, dat_vec.dat2.vel)
    
    if make_data:
        save(coh, 'coherence.nc')
        return
    saved_coh = load('coherence.nc')
    
    assert_allclose(coh, saved_coh.coherence, atol=1e-5)
    
    
def test_calc_phase_angle(make_data=False):
    dat_vec = adv_setup(tv)
    pang = dat_vec.avg_tool.calc_phase_angle(dat_vec.dat1.vel, 
                                                dat_vec.dat2.vel)
    if make_data:
        save(pang, 'phase_angle.nc')
        return
    saved_pang = load('phase_angle.nc')
    
    assert_allclose(pang, saved_pang.phase_angle, atol=1e-5)
    
    
def test_calc_acov(make_data=False):
    dat_vec = adv_setup(tv)
    acov = dat_vec.avg_tool.calc_acov(dat_vec.dat1.vel)
    
    if make_data:
        save(acov, 'auto-cov.nc')
        return
    saved_acov = load('auto-cov.nc')
    
    assert_allclose(acov, saved_acov['auto-covariance'], atol=1e-5)
    
    
def test_calc_xcov(make_data=False):
    dat_vec = adv_setup(tv)
    xcov = dat_vec.avg_tool.calc_xcov(dat_vec.dat1.vel, dat_vec.dat2.vel)
    
    if make_data:
        save(xcov, 'cross-cov.nc')
        return
    saved_xcov = load('cross-cov.nc')
    
    assert_allclose(xcov, saved_xcov['cross-covariance'], atol=1e-5)
    
     
def test_calc_tke(make_data=False):
    dat_vec = adv_setup(tv)
    tke = dat_vec.avg_tool.calc_tke(dat_vec.dat1.vel)
    
    if make_data:
        save(tke, 'tke_vector.nc')
        return
    saved_tke = load('tke_vector.nc')
    
    assert_allclose(tke, saved_tke.tke_vec, atol=1e-5)
    
    
def test_calc_stress(make_data=False):
    dat_vec = adv_setup(tv)
    stress = dat_vec.avg_tool.calc_stress(dat_vec.dat1.vel)
    
    if make_data:
        save(stress, 'stress_vector.nc')
        return
    saved_stress = load('stress_vector.nc')
    
    assert_allclose(stress, saved_stress.stress_vec, atol=1e-5)
    
    
def test_do_tke(make_data=False):
    dat_vec = adv_setup(tv)
    adat = dat_vec.avg_tool.do_avg(dat_vec.dat1)
    tkedat = dat_vec.avg_tool.do_tke(adat, out=adat)
    
    if make_data:
        save(tkedat, 'ADV_avg+tke.nc')
        return
    saved_tkedat = load('ADV_avg+tke.nc')
    
    assert_allclose(tkedat, saved_tkedat, atol=1e-5)
    
    
def test_calc_freq(make_data=False):
    dat_vec = adv_setup(tv)
    
    f = dat_vec.avg_tool.calc_freq(units='Hz')
    omega = dat_vec.avg_tool.calc_freq(units='rad/s')
    
    np.testing.assert_equal(f, np.arange(1, 17, 1, dtype='float'))
    np.testing.assert_equal(omega, np.arange(1, 17, 1, dtype='float')*(2*np.pi))
    
    
def test_calc_vel_psd(make_data=False):
    dat_vec = adv_setup(tv)    
    spec = dat_vec.avg_tool.calc_vel_psd(dat_vec.dat1.vel)
    
    if make_data:
        save(spec, 'spectra.nc')
        return
    saved_spec = load('spectra.nc')
    
    assert_allclose(spec, saved_spec.S, atol=1e-5)
    
    
def test_calc_vel_csd(make_data=False):
    dat_vec = adv_setup(tv)    
    cspec = dat_vec.avg_tool.calc_vel_csd(dat_vec.dat1.vel)
    
    if make_data:
        save(cspec, 'cross-spectra.nc')
        return
    saved_cspec = load('cross-spectra.nc')
    
    assert_allclose(cspec, saved_cspec.csd, atol=1e-5)


# test each of TurbBinner's functions on an ADV
def test_calc_turbulence(make_data=False):
    dat = tv.dat
    tdat = avm.calc_turbulence(dat, n_bin=20.0, fs=dat.fs)
    
    if make_data:
        save(tdat, 'turb_data.nc')
        return
    saved_tdat = load('turb_data.nc')
    
    assert_allclose(tdat, saved_tdat, atol=1e-5)
    
    
def test_calc_epsilon(make_data=False):
    dat = tv.dat
    bnr = avm.TurbBinner(n_bin=20.0, fs=dat.fs)
    tdat = bnr(dat)
    
    LT83 = bnr.calc_epsilon_LT83(tdat.S, tdat.Veldata.U_mag)
    SF = bnr.calc_epsilon_SF(dat.vel[0], tdat.Veldata.U_mag)
    TE01 = bnr.calc_epsilon_TE01(dat, tdat)
    
    if make_data:
        save(LT83, 'dissipation_LT83.nc')
        save(SF, 'dissipation_SF.nc')
        save(TE01, 'dissipation_TE01.nc')
        return
    
    saved_LT83 = load('dissipation_LT83.nc')
    saved_SF = load('dissipation_SF.nc')
    saved_TE01 = load('dissipation_TE01.nc')
    
    assert_allclose(LT83, saved_LT83.dissipation_rate, atol=1e-5)
    assert_allclose(SF, saved_SF.dissipation_rate, atol=1e-5)
    assert_allclose(TE01, saved_TE01.dissipation_rate, atol=1e-5)
    
    
def test_calc_L_int(make_data=False):
    dat = tv.dat
    bnr = avm.TurbBinner(n_bin=20.0, fs=dat.fs)
    tdat = bnr(dat)
    acov = bnr.calc_acov(dat.vel)
    
    L = bnr.calc_L_int(acov, tdat.vel)
    
    if make_data:
        save(L, 'length_scales.nc')
        return
    saved_L = load('length_scales.nc')
    
    assert_allclose(L, saved_L.L_int, atol=1e-5)
    
    
if __name__ == '__main__':
    test_do_avg()
    test_do_var()
    test_calc_coh()
    test_calc_phase_angle()
    test_calc_acov()
    test_calc_xcov()
    test_calc_tke()
    test_calc_stress()
    test_do_tke()
    test_calc_freq()
    test_calc_vel_psd()
    test_calc_vel_csd()
    test_calc_turbulence()
    test_calc_epsilon()
    test_calc_L_int()
    