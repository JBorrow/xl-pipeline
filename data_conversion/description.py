"""
Generates a description.html that will be deposited into the
index.html file. Also generates a boxsize_integer.txt file containing
the box-size converted to Mpc as an integer.

Requires two parameters: path to snapshot, and path to yaml file.
"""

import yaml
from swiftsimio import load
from numpy import log10

import sys


def latex_float(f):
    float_str = "{0:.4g}".format(f)
    if "e" in float_str:
        base, exponent = float_str.split("e")
        return r"{0} \times 10^{{{1}}}".format(base, int(exponent))
    else:
        return float_str


data = load(sys.argv[1])

with open("boxsize_integer.txt", "w") as handle:
    handle.write("%d" % int(data.metadata.boxsize[0].value + 0.1))

with open(sys.argv[2], "r") as handle:
    parameter_file = yaml.load(handle, Loader=yaml.Loader)

try:
    run_name = data.metadata.run_name.decode("utf-8").replace("!!python/unicode", "")
except:
    run_name = ""

# Need to build the feedback parameters list.

# Supernovae feedback
supernova_feedback = "<li>Unknown supernovae feedback subgrid model</li>"

try:
    supernova_feedback = f"""
        <li>$f_{{\\rm E, min}} = {parameter_file['EAGLEFeedback']['SNII_energy_fraction_min']:.4g}$</li>
        <li>$f_{{\\rm E, max}} = {parameter_file['EAGLEFeedback']['SNII_energy_fraction_max']:.4g}$</li>
        <li>$n_Z = {parameter_file['EAGLEFeedback']['SNII_energy_fraction_n_Z']:.4g}$</li>
        <li>$n_{{\\rm H, 0}} = {parameter_file['EAGLEFeedback']['SNII_energy_fraction_n_0_H_p_cm3']:.4g}$</li>
        <li>$n_n = {parameter_file['EAGLEFeedback']['SNII_energy_fraction_n_n']:.4g}$</li>"""
except KeyError:
    pass

try:
    supernova_feedback = f"""
        <li><b>SNII feedback parameters:</b></li>
        <li>$E = {parameter_file['COLIBREFeedback']['SNII_energy_erg']}$</li>
        <li>$f_{{\\rm E, min}} = {parameter_file['COLIBREFeedback']['SNII_energy_fraction_min']:.4g}$</li>
        <li>$f_{{\\rm E, max}} = {parameter_file['COLIBREFeedback']['SNII_energy_fraction_max']:.4g}$</li>
    """
    try:
        supernova_feedback += f"""
                <li>$f_{{\\rm kinetic}} = {parameter_file['COLIBREFeedback']['SNII_f_kinetic']}$</li>
                <li>$v_{{\\rm kinetic}} = {parameter_file['COLIBREFeedback']['SNII_delta_v_km_p_s']}$ km/s</li>
        """
    except:
        pass
except KeyError:
    pass

# Star formation

star_formation = ""

try:
    star_formation = f"""
       <li><b>Star formation parameters:</b></li>
       <li>Temperature ceiling: ${parameter_file['COLIBREStarFormation']['temperature_threshold_K']}$ K</li>
       <li>SF model: ${parameter_file['COLIBREStarFormation']['SF_model']}$ </li>
    """
    try:
        star_formation += f"""
            <li>Virial parameter: ${parameter_file['COLIBREStarFormation']['alpha_virial']}$</li>
        """
    except KeyError:
        pass
    try:
        star_formation += f"""
            <li>$n_{{\\rm H, max}} = {parameter_file['COLIBREStarFormation']['threshold_max_density_H_p_cm3']}$ cm$^3$
            (gas gets turned into star immediately)</li>
        """
    except KeyError:
        pass
    try:
        star_formation += f"""
            <li>$n_{{\\rm H, max, sub}} = {parameter_file['COLIBREStarFormation']['subgrid_density_threshold_H_p_CM3']}$ cm$^3$
            (gas is star forming)</li>
        """
    except KeyError:
        pass

except KeyError:
    pass


# Entropy floor
entropy_floor = ""

try:
    entropy_floor = f"""
       <li><b>Entropy floor parameter:</b></li>
       <li>$n_{{\\rm H, norm}} = {parameter_file['COLIBREEntropyFloor']['Jeans_density_norm_H_p_cm3']}$ cm$^3$ </li>
       <li>$T_{{\\rm norm}}   = {parameter_file['COLIBREEntropyFloor']['Jeans_temperature_norm_K']}$ K </li>
       <li>Slope = ${parameter_file['COLIBREEntropyFloor']['Jeans_gamma_effective']}$</li>
    """
except KeyError:
    pass

# AGN / Black hole model
agn_feedback = "<li>Unknown black hole model</li>"

try:
    agn_feedback = f"""
        <li>
          AGN $\\mathrm{{d}}T = {parameter_file['EAGLEAGN']['AGN_delta_T_K']}$
          ($\\log_{{10}}(\\mathrm{{d}}T / K) = {log10(float(parameter_file['EAGLEAGN']['AGN_delta_T_K']))}$)
        </li>
        <li>AGN $C_{{\\rm eff}} = {parameter_file['EAGLEAGN']['coupling_efficiency']:.4g}$</li>
        <li>AGN Visocous $\\alpha = {parameter_file['EAGLEAGN']['viscous_alpha']}$</li>"""
except KeyError:
    pass

try:
    agn_feedback = f"""
        <li><b>AGN parameters:</b></li>
        <li>
          AGN $\\mathrm{{d}}T = {parameter_file['COLIBREAGN']['AGN_delta_T_K']}$
          ($\\log_{{10}}(\\mathrm{{d}}T / K) = {log10(float(parameter_file['COLIBREAGN']['AGN_delta_T_K']))}$)
        </li>
        <li>AGN $C_{{\\rm eff}} = {parameter_file['COLIBREAGN']['coupling_efficiency']:.4g}$</li>
        <li>AGN Visocous $\\alpha = {parameter_file['COLIBREAGN']['viscous_alpha']}$</li>"""
    try:
        # Possible additional AGN parameters
        agn_feedback += f"""
        <li>Reposition base velocity = {parameter_file['COLIBREAGN']['reposition_coefficient_upsilon']}</li>
        """
    except KeyError:
        pass
    try:
        agn_feedback += f"""
        <li>Subgrid seed mass (Msol) = {parameter_file['COLIBREAGN']['subgrid_seed_mass_Msun']}</li>
        """
    except KeyError:
        pass

    try:
        agn_feedback += f"""
        <li>Number of neighbours to heat = {parameter_file['COLIBREAGN']['AGN_num_ngb_to_heat']}</li>
        """
    except KeyError:
        pass

    try:
        agn_feedback += f"""
        <li>Use multi-phase Bondi = {parameter_file['COLIBREAGN']['use_multi_phase_bondi']}</li>
        """
    except KeyError:
        pass

    try:
        agn_feedback += f"""
        <li>Use subgrid properties = {parameter_file['COLIBREAGN']['use_subgrid_gas_properties']}</li>
        """
    except KeyError:
        pass

    try:
        agn_feedback += f"""
        <li>Use Krumholz+2006 accretion rates = {parameter_file['COLIBREAGN']['use_krumholz']}</li>
        <li>Use Krumholz+2006 vorticity term  = {parameter_file['COLIBREAGN']['with_krumholz_vorticity']}</li>
        """
    except KeyError:
        pass

    try:
        agn_feedback += f"""
        <li>Use Rosas-Guevara (2015) viscous time-scale reduction term = {parameter_file['COLIBREAGN']['with_angmom_limiter']}</li>
        """
    except KeyError:
        pass

    try:
        agn_feedback += f"""
        <li>Coupling efficiency = {parameter_file['COLIBREAGN']['coupling_efficiency']}</li>
        """
    except KeyError:
        pass

    try:
        agn_feedback += f"""
        <li>Maximal BH mass considered for BH repositioning = {parameter_file['COLIBREAGN']['max_reposition_mass']} M$_\\odot$</li>
        """
    except KeyError:
        pass

    try:
        agn_feedback += f"""
        <li>Only reposition to particles that move slowly w.r.t. the black hole =
        {parameter_file['COLIBREAGN']['with_reposition_velocity_threshold']}</li>
        """
    except KeyError:
        pass

    try:
        agn_feedback += f"""
        <li>Maximal velocity offset for repositioning (units of BH sound speed) =
        {parameter_file['COLIBREAGN']['max_reposition_velocity_ratio']}</li>
        """
    except KeyError:
        pass

except KeyError:
    pass

DM_to_baryon_ratio = int(
    round(data.metadata.n_dark_matter / (data.metadata.n_gas + data.metadata.n_stars))
)

particlenumbers = f"""
<li><b>Cube root of dark matter particle number</b>: {int(data.metadata.n_dark_matter**(1/3)+0.01)}</li>
<li><b>Cube root of baryon particle number</b>: {int((data.metadata.n_gas + data.metadata.n_stars)**(1/3)+0.01)}</li>
<li><b>Ratio dark matter to baryon particles</b>: {int(DM_to_baryon_ratio)} </li>
<li><b>Number of particles at $z={data.metadata.z:2.2f}$</b>:
    <ul>
    <li>Dark matter: {data.metadata.n_dark_matter}</li>
    <li>Gas: {data.metadata.n_gas}</li>
    <li>Star: {data.metadata.n_stars}</li>
    <li>Black hole: {data.metadata.n_black_holes}</li>
    </ul>
</li>
"""

# Now generate HTML
output = f"""<ul>
<li><b>Run Name</b>: {run_name}</li>
<li><b>Boxsize</b>: {str(data.metadata.boxsize)}</li>
{particlenumbers}
<li><b>Minimal particle masses at $z={data.metadata.z:2.2f}$</b>:
  <ul>
    <li>Dark matter: ${latex_float(data.dark_matter.masses[::100].min().to('Solar_Mass').value)}$ M$_\\odot$</li>
    <li>Gas: ${latex_float(data.gas.masses[::100].min().to('Solar_Mass').value)}$ M$_\\odot$</li>
  </ul>
</li>
<li><b>Particle gravitational softenings</b>:
  <ul>
    <li>Dark matter: {str((float(parameter_file["Gravity"]["max_physical_DM_softening"]) * data.units.length).to('kpc'))}</li>
    <li>Baryons: {str((float(parameter_file["Gravity"]["max_physical_baryon_softening"]) * data.units.length).to('kpc'))}</li>
  </ul>
</li>
<li><b>Code info</b>: {data.metadata.code_info}</li>
<li><b>Compiler info</b>: {data.metadata.compiler_info}</li>
<li><b>Hydrodynamics</b>: {data.metadata.hydro_info}</li>
<li><b>Subgrid model parameters</b>:
  <ul>
    {supernova_feedback}
    {agn_feedback}
    {entropy_floor}
    {star_formation}
  </ul>
</ul>
"""

with open("description.html", "w") as handle:
    handle.write(output)
