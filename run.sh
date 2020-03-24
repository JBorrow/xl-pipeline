#!/bin/bash

# Example script to run analysis on a run.

# Load all sub-modules that we need
source modules.sh
source plot.sh
source image.sh

# You should have a python environment with requirements.txt installed
source env/bin/activate

isnap=36
ptype="COLIBRE"

isnap_formatted=$( printf '%04d' $isnap )
# First up, an example for running the scripts on one at a time
run_directory="/cosma7/data/dp004/dc-ploe1/SIMULATION_RUNS/2020_01_COLIBRE_ref/COLIBRE_L006N0188_ref/"
run_name="COLIBRE_L006N0188_ref"
plot_directory="Plots3"
snapshot_name="data/snaps/colibre_$isnap_formatted.hdf5"
catalogue_name="data/stf/halos_$isnap_formatted.properties.0"

mkdir -p $plot_directory/$run_name
plot_run $run_directory $run_name $plot_directory $snapshot_name $catalogue_name
create_summary_plot $run_directory $run_name $plot_directory $snapshot_name $catalogue_name
image_run $run_directory $run_name $plot_directory $snapshot_name $catalogue_name

# Second, baking in a run identifier so we can leverage gnu parallel.

plot_single_run () {
  run_name=$1
  run_directory="Runs/${run_name}"
  plot_directory="Plots"
  snapshot_name="data/snaps/colibre_$isnap_formatted.hdf5"
  catalogue_name="data/stf/halos_$isnap_formatted.properties.0"

  mkdir -p $plot_directory/$run_name

  # Check if run exists before doing any of this stuff!
  if [[ -f $run_directory/$snapshot_name ]]
  then
    plot_run $run_directory $run_name $plot_directory $snapshot_name $catalogue_name
    create_summary_plot $run_directory $run_name $plot_directory $snapshot_name $catalogue_name
    image_run $run_directory $run_name $plot_directory $snapshot_name $catalogue_name $ptype
  fi
}

ls "Runs" | grep Run | parallel -n1 -j56 "plot_single_run ${path}"
