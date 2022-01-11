import ROOT
import numpy as np

'''
Functions for creating or setting up branches of the TTrees for GRAND

Run TTrees store information that do not change through the whole Run
The rest of the Trees store data changing event by event (each TTree entry is an event)
The GRANDDetectorInfo stores data for each detector (each entry is a separate detector)

To use these functions, create a TTree and then call the specific function with this TTree as parameter
If used for the first time - to create branches - the "create_branches" parametes should be True.
If just resetting addresses of the branches already created (for example new vectors, etc.), it should be False.

'''

# Create branches of a TTree t with a list of values and root_types
def create_branches(values, root_types, t):
    for key, val in values.items():
        # If the branches are created for the first time
        if create_branches:
            # Vector branch
            if root_types[key] == "/C":
                t.Branch(key, val)
            # Scalar branch
            else:
                t.Branch(key, val, f"{key}{root_types[key]}")
        # If branches are reaccessed, just set their addresses
        else:
            t.SetBranchAddress(key, val)


# Create or Set rhe TTree branches for shower properties of the whole run
def Setup_GRANDRun_Branches(tree,create_branches=True):
    t = tree
    # Reset all branch addresses just in case
    t.ResetBranchAddresses()

    values = {"run_id": np.zeros(1, np.uint32),  #runID TODO: datatype. standarize. Do we want also a name or a short description? (so, a number and a string) # LWP: we need hardware/software information, because this can change over time. Looking at the stuff I coded for JEM-EUSO: experiment_name (GP300, GP10k, etc.), experiment_type (real, simulation), antenna_count?, antenna_type? (or more antenna information that can change in time), antenna_layout?, antenna_frequency_window?, firmware_vetsion?, hardware pieces versions, sampling, etc. MJT: Agreed. Some of this will also be duplicated on RawData Part.
              "site": ROOT.vector("string")(),  # Event Site: TODO: standarize
              "site_lat_long": np.zeros(2, np.float32),  # Site latitude and longitude (deg)
              "origin_geoid": np.zeros(3, np.float32)}  #origin of the coordinate system used for the array TODO: Standarize. Lat, Long, Altitude? smthing else is needed? Geoid?

    root_types = {"run_id": "/i",
                  "site": "/C",
                  "site_lat_long": "[2]/F",
                  "origin_geoid": "[3]/F"}

    create_branches(values, root_types, t)

    return values


# Create or Set rhe TTree branches for simulation-only shower properties of the whole run
def Setup_GRANDShowerRunSimdata_Branches(tree, create_branches=True):
    t = tree
    # Reset all branch addresses just in case
    t.ResetBranchAddresses()

    values = {"run_id": np.zeros(1, np.uint32), # runID TODO: datatype. standarize. Do we want also a name or a short description? (so, a number and a string) # LWP: we need hardware/software information, because this can change over time. Looking at the stuff I coded for JEM-EUSO: experiment_name (GP300, GP10k, etc.), experiment_type (real, simulation), antenna_count?, antenna_type? (or more antenna information that can change in time), antenna_layout?, antenna_frequency_window?, firmware_vetsion?, hardware pieces versions, sampling, etc. MJT: Agreed. Some of this will also be duplicated on RawData Part.
              "shower_sim": ROOT.vector("string")(), # simulation program (and version) used tosimulate the shower TODO: Standarize # LWP: I would move it to the ideas above. This tree will be common for real and simulated data, so specific simualtion field is probably not good . MJT: Not in this particular tree (SimShower)
                # TODO: Think about this. All this below is ZHAIRES specific. How to make it universal? Do we need to make it universal? Or can showers simulated with different simulators have different trees? If need to merge, turn branches off? # LWP: in JEM-EUSO we have a data tree common to simul/real data, an texp tree that contains experiment info common to simul/real, and a tsim which contains only simulator specific data. In case of real data, tsim is not in the file. MJT: Agreed. But again, this is the SimShower Tree.soo...here goes sim information...and some of it is simulator-specific.
                # do we want to have this in the event level instead?
                "rel_thin": np.zeros(1, np.float32),  # relative thinning energy
                "weight_factor": np.zeros(1, np.float32),  # weight factor
                "lowe_cut_e": np.zeros(1, np.float32),  # low energy cut for electrons(GeV) TODO: Check unit conventions
                "lowe_cut_gamma": np.zeros(1, np.float32),  # low energy cut for gammas(GeV) TODO: Check unit conventions
                "lowe_cut_mu": np.zeros(1, np.float32),  # low energy cut for muons(GeV) TODO: Check unit conventions
                "lowe_cut_meson": np.zeros(1, np.float32),  # low energy cut for mesons(GeV) TODO: Check unit conventions
                "lowe_cut_nucleon": np.zeros(1, np.float32)}  # low energy cut for nuceleons(GeV) TODO: Check unit conventions

    root_types = {"run_id": "/i",
                  "shower_sim": "/C",
                  "rel_thin": "/F",
                  "weight_factor": "/F",
                  "lowe_cut_e": "/F",
                  "lowe_cut_gamma": "/F",
                  "lowe_cut_mu": "/F",
                  "lowe_cut_meson": "/F",
                  "lowe_cut_nucleon": "/F"
                  }

    create_branches(values, root_types, t)

    return values


# Create or Set the TTree branches for each reconstructed shower event
def Setup_GRANDShower_Branches(tree, create_branches=True):
    t = tree
    
    # Reset all branch addresses just in case
    t.ResetBranchAddresses()
    
    values = {"run_id": np.zeros(1, np.uint32),                  #runID TODO: datatype. standarize. Do we want also a name or a short description? (so, a number and a string) # LWP: I think this should just be a number, while some names and descriptions, as additional branches should be only in the run ttree MJT: Agreed
              "evt_id": np.zeros(1, np.uint32),                  #eventID TODO: datatype. standarize. Do we want also a name? (so, a number and a string) # LWP: If a name, I would add it also as a separate branch (but I doubt we would need it, more so for runs). MJT: Agreed. naming an event is weird...but i was more thinking if we need a string or an unsigned int. I dont know how we will identify the events yet.
              "shower_type":ROOT.vector("string")(),             #shower primary type: If single particle, particle type. If not...tau decay,etc. TODO: Standarize              
              "shower_energy": np.zeros(1, np.float32),          #shower energy (GeV)  Check unit conventions.
              "shower_azimuth": np.zeros(1, np.float32),         #shower azimuth TODO: Discuss coordinates Cosmic ray convention is bad for neutrinos, but neurtino convention is problematic for round earth. Also, geoid vs sphere problem
              "shower_zenith": np.zeros(1, np.float32),          #shower zenith  TODO: Discuss coordinates Cosmic ray convention is bad for neutrinos, but neurtino convention is problematic for round earth
              "shower_core_pos": np.zeros(4, np.float32),        #shower core position TODO: Coordinates in geoid?. Undefined for neutrinos.
              "atmos_model": ROOT.vector("string")(),            #Atmospheric model name TODO:standarize
              "atmos_model_param": np.zeros(3, np.float32),      #Atmospheric model parameters: TODO: Think about this. Different models and softwares can have different parameters
              "magnetic_field": np.zeros(3, np.float32),         #Magnetic field parameters: Inclination, Declination, modulus. TODO: Standarize. Check units. Think about coordinates. Shower coordinates make sense.
              "date": ROOT.vector("string")(),                   #Event Date and time. TODO:standarize (date format, time format)
              "ground_alt": np.zeros(1, np.float32),             #Ground Altitude (m)
              "xmax_grams": np.zeros(1, np.float32),             #shower Xmax depth  (g/cm2 along the shower axis)
              "xmax_pos_shc": np.zeros(3, np.float64),           #shower Xmax position in shower coordinates
              "xmax_alt": np.zeros(1, np.float64),               #altitude of Xmax  (m, in the shower simulation earth. Its important for the index of refraction )
              "gh_fit_param": np.zeros(3, np.float32),           #X0,Xmax,Lambda (g/cm2) (3 parameter GH function fit to the longitudinal development of all particles)
              "core_time": np.zeros(1, np.float64)               # ToDo: Check; time when the shower was at the core position - defined in Charles, but not in Zhaires/Coreas?
             }
    root_types = {"run_id": "/i", 
                  "evt_id": "/i", 
                  "shower_type": "/C", 
                  "shower_energy": "/F",
                  "shower_azimuth": "/F",
                  "shower_zenith": "/F",
                  "shower_core_pos": "[4]/F",                  
                  "atmos_model": "/C",
                  "atmos_model_param": "[3]/F",
                  "magnetic_field": "[3]/F",
                  "date": "/C",
                  "ground_alt": "/F",
                  "xmax_grams": "/F",
                  "xmax_pos_shc": "[3]/D",
                  "xmax_alt": "/D",
                  "gh_fit_param": "[3]/F",
                  "core_time": "/D"
                 }

    create_branches(values, root_types, t)

    return values

# Create or Set the TTree branches for simulation-only data of each reconstructed shower event
def Setup_GRANDShowerSimdata_Branches(tree, create_branches=True):
    t = tree

    # Reset all branch addresses just in case
    t.ResetBranchAddresses()

    values = {"run_id": np.zeros(1, np.uint32),  # runID TODO: datatype. standarize. Do we want also a name or a short description? (so, a number and a string) # LWP: I think this should just be a number, while some names and descriptions, as additional branches should be only in the run ttree MJT: Agreed
    "evt_id": np.zeros(1, np.uint32),  # eventID TODO: datatype. standarize. Do we want also a name? (so, a number and a string) # LWP: If a name, I would add it also as a separate branch (but I doubt we would need it, more so for runs). MJT: Agreed. naming an event is weird...but i was more thinking if we need a string or an unsigned int. I dont know how we will identify the events yet.
    "rnd_seed": np.zeros(1, np.float64),  # random seed
    "energy_in_neutrinos": np.zeros(1, np.float32),  # Energy in neutrinos generated in the shower (GeV). Usefull for invisible energy
    "prim_energy": np.zeros(1, np.float32),  # primary energy (GeV) TODO: Support multiple primaries. Check unit conventions. # LWP: Multiple primaries? I guess, variable count. Thus variable size array or a std::vector
    "prim_type": ROOT.vector("string")(),  # primary particle type TODO: Support multiple primaries. standarize (PDG?)
    "prim_injpoint_shc": np.zeros(4, np.float32),  # primary injection point in Shower coordinates TODO: Support multiple primaries
    "prim_inj_alt_shc": np.zeros(1, np.float32),  # primary injection altitude in Shower Coordinates TODO: Support multiple primaries
    "prim_inj_dir_shc": np.zeros(3, np.float32),  # primary injection direction in Shower Coordinates  TODO: Support multiple primaries
    "hadronic_model": ROOT.vector("string")(),  # high energy hadronic model (and version) used TODO: standarize
    "low_energy_model": ROOT.vector("string")(),  # high energy model (and version) used TODO: standarize
    "cpu_time": np.zeros(3, np.float32),  # Time it took for the simulation. In the case shower and radio are simulated together, use TotalTime/(nant-1) as an approximation
    }
    root_types = {"run_id": "/i",
                  "evt_id": "/i",
                  "rnd_seed": "/D",
                  "energy_in_neutrinos": "/F",
                  "prim_energy": "/F",
                  "prim_type": "/C",
                  "prim_injpoint_shc": "[4]/F",
                  "prim_inj_alt_shc": "/F",
                  "prim_inj_dir_shc": "[3]/F",
                  "hadronic_model": "/C",
                  "low_energy_model": "/C",
                  "cpu_time": "[3]/F"
                  }

    create_branches(values, root_types, t)

    return values


# Create or Set the TTree branches for simulaton-only Efield data common for the whole Run and all antennas
def Setup_GRANDEfieldRunSimdata_Branches(tree, create_branches=True):
    t = tree
   # Reset all branch addresses just in case
    t.ResetBranchAddresses()

    values = {"run_id": np.zeros(1, np.uint32),                  #runID TODO: datatype. standarize. Do we want also a name or a short description? (so, a number and a string)
              # "evt_id": np.zeros(1, np.uint32),                  #eventID TODO: datatype. standarize. Do we want also a name? (so, a number and a string)
              "field_sim": ROOT.vector("string")(),              #name and model of the electric field simulator. TODO: Standarize  
              "refractivity_model": ROOT.vector("string")(),     #name of the atmospheric index of refraction model. TODO:Standarize  
              "refractivity_param": np.zeros(2, np.float32),     #parameters of the atmospheric index of refraction model. TODO: Standarize. Think how to support different model needs. 
              "t_pre":np.zeros(1, np.float32),                   #The antenna time window is defined arround a t0 that changes with the antenna, starts on t0+t_pre (thus t_pre is usually negative) and ends on t0+post
              "t_post":np.zeros(1, np.float32),                  #TODO: Should we support different antenna trace sizes? Currently its not posible. If that is the case, should t_pre,t_post and t_bin_size be on SimEfieldRun?
              "t_bin_size":np.zeros(1, np.float32)
             }
    root_types = {"run_id": "/i", 
                  # "evt_id": "/i",
                  "field_sim": "/C",
                  "refractivity_model": "/C",
                  "refractivity_param": "[2]/F",
                  "t_pre":"/F",
                  "t_post":"/F",
                  "t_bin_size":"/F", 
                 }

    create_branches(values, root_types, t)

    return values    
    
# Create or Set the TTree branches for simulation-only Efield data common for each Event and all antennas
def Setup_GRANDEfieldSimdata_Branches(tree, create_branches=True):
    t = tree

    # Reset all branch addresses just in case
    #t.ResetBranchAddresses()  it was reset in the Setup_SimSignal_Branches call. TODO: Merge both functions

    values = {"run_id": np.zeros(1, np.uint32),                  #runID TODO: datatype. standarize. Do we want also a name or a short description? (so, a number and a string)
              "evt_id": np.zeros(1, np.uint32),                  #eventID TODO: datatype. standarize. Do we want also a name? (so, a number and a string)
              "det_id": ROOT.vector("int")(),        #TODO: Standarize the ID of antennas. Do we Want a number? A string? both (ID and Name). This will/should be linked to the RunInfo, where some detector configuration should reside.
              "t_0": ROOT.vector("float")(),           #Time window t0
              "p2p": ROOT.vector("float")(),           #peak 2 peak amplitudes (x,y,z,modulus). TODO: Hillbert envelope quantities
              }
    root_types = {"run_id": "/i",
                  "evt_id": "/i",
                  "det_id": "vec",
                  "t_0": "vec",
                  "p2p": "vec",
                  }

    create_branches(values, root_types, t)

    return values

# Create or Set the TTree branches for simulaton-only Voltage data common for the whole Run and all antennas
def Setup_GRANDVoltageRunSimdata_Branches(tree, create_branches=True):
    t = tree
   # Reset all branch addresses just in case
    t.ResetBranchAddresses()

    values = {"run_id": np.zeros(1, np.uint32),                  #runID TODO: datatype. standarize. Do we want also a name or a short description? (so, a number and a string)
              "signal_sim": ROOT.vector("string")(),              # name and model of the signal simulator. TODO: Standarize
             }
    root_types = {"run_id": "/i",
                  "signal_sim": "/C",
                 }

    create_branches(values, root_types, t)

    return values

# Create or Set the TTree branches for simulation-only Voltage data common for each Event and all antennas
def Setup_GRANDVoltageSimdata_Branches(tree, create_branches=True):
    t = tree

    # Reset all branch addresses just in case
    #t.ResetBranchAddresses()  it was reset in the Setup_SimSignal_Branches call. TODO: Merge both functions

    values = {"run_id": np.zeros(1, np.uint32),                  #runID TODO: datatype. standarize. Do we want also a name or a short description? (so, a number and a string)
              "evt_id": np.zeros(1, np.uint32),                  #eventID TODO: datatype. standarize. Do we want also a name? (so, a number and a string)
              "det_id": ROOT.vector("int")(),        #TODO: Standarize the ID of antennas. Do we Want a number? A string? both (ID and Name). This will/should be linked to the RunInfo, where some detector configuration should reside.
              "t_0": ROOT.vector("float")(),           #Time window t0
              "p2p": ROOT.vector("float")(),           #peak 2 peak amplitudes (x,y,z,modulus). TODO: Hillbert envelope quantities
              }
    root_types = {"run_id": "/i",
                  "evt_id": "/i",
                  "det_id": "vec",
                  "t_0": "vec",
                  "p2p": "vec",
                  }

    create_branches(values, root_types, t)

    return values

# Create or Set the TTree branches for GRAND ADC counts storage
def Setup_GRANDADCCounts_Branches(tree, create_branches=True):
    t = tree

    # Reset all branch addresses just in case
    t.ResetBranchAddresses()

    values = {"run_id": np.zeros(1, np.uint32),
              "evt_id": np.zeros(1, np.uint32),
              "det_id": ROOT.vector("int")(),        #TODO: Standarize the ID of antennas. Do we Want a number? A string? both (ID and Name). This will/should be linked to the RunInfo, where some detector configuration should reside.
              "trace_length": ROOT.vector("unsigned int")(), # Do we need it? Can be obtained from traces. On the other hand, small in storage and easy to use. ("Raw/SimPoints in Charles)
              "start_time": ROOT.vector("double")(), # start_time_gps? But will there be anything else than GPS?
                                                     # 4 bytes for nanoseconds, 4 bytes for unix time. This is enough until 2038. We should have more, but no 128 bit field in a TTree..
                                                     # (GPS in Charles, t_0 in Zhaires?)
              "rel_peak_time": ROOT.vector("float")(),     # offset between start and the peak of the signal (do we always have it from hardware?) (TPulse in Charles)
              "det_time": ROOT.vector("double")(),     # Not from the hardware! I don't like this name! time of the peak of the signal relative to the time that the shower hit the surface (do we always have it from hardware?) (DetTime in Charles)
              "e_det_time": ROOT.vector("double")(),     # uncertainty of the above (e_DetTime in Charles)
              "isTriggered": ROOT.vector("bool")(),
              "sampling_speed": ROOT.vector("float")(), # ToDo: Think if to move to detectorInfo. Constant, depends on the electronics. But can be added with different values during tests in the same detector. Isn't this constant (and thus should be in another tree?). Why float? (Raw/SimMSPS in Charles)
              "trace_x":ROOT.vector("vector<float>")(), # Should it be float?
              "trace_y":ROOT.vector("vector<float>")(),
              "trace_z":ROOT.vector("vector<float>")()
              }

    root_types = {"run_id": "/i",
                  "evt_id": "/i",
                  "det_id": "vec",
                  "trace_length": "vec",
                  "start_time": "vec",
                  "rel_peak_time": "vec",
                  "det_time": "vec",
                  "e_det_time": "vec",
                  "isTriggered": "vec",
                  "sampling_speed": "vec",
                  "trace_x":"vec",
                  "trace_y":"vec",
                  "trace_z":"vec"
                  }

    create_branches(values, root_types, t)

    return values

# Create or Set the TTree branches for GRAND Voltage traces storage
def Setup_GRANDVoltage_Branches(tree, create_branches=True):
    t = tree

    # Reset all branch addresses just in case
    t.ResetBranchAddresses()

    values = {"run_id": np.zeros(1, np.uint32),
              "evt_id": np.zeros(1, np.uint32),
              "det_id": ROOT.vector("int")(),        #TODO: Standarize the ID of antennas. Do we Want a number? A string? both (ID and Name). This will/should be linked to the RunInfo, where some detector configuration should reside.
              "trace_length": ROOT.vector("unsigned int")(), # Do we need it? Can be obtained from traces. On the other hand, small in storage and easy to use. ("Raw/SimPoints in Charles)
              "start_time": ROOT.vector("double")(), # start_time_gps? But will there be anything else than GPS?
                                                     # 4 bytes for nanoseconds, 4 bytes for unix time. This is enough until 2038. We should have more, but no 128 bit field in a TTree..
                                                     # (GPS in Charles, t_0 in Zhaires?)
              "rel_peak_time": ROOT.vector("float")(),     # offset between start and the peak of the signal (do we always have it from hardware?) (TPulse in Charles)
              "det_time": ROOT.vector("double")(),     # Not from the hardware! I don't like this name! time of the peak of the signal relative to the time that the shower hit the surface (do we always have it from hardware?) (DetTime in Charles)
              "e_det_time": ROOT.vector("double")(),     # uncertainty of the above (e_DetTime in Charles)
              "isTriggered": ROOT.vector("bool")(),
              "sampling_speed": ROOT.vector("float")(), # ToDo: Think if to move to detectorInfo. Constant, depends on the electronics. But can be added with different values during tests in the same detector. Isn't this constant (and thus should be in another tree?). Why float? (Raw/SimMSPS in Charles)
              "trace_x":ROOT.vector("vector<float>")(),        #TODO: I would like to store the three channels
              "trace_y":ROOT.vector("vector<float>")(),
              "trace_z":ROOT.vector("vector<float>")()
              }

    root_types = {"run_id": "/i",
                  "evt_id": "/i",
                  "det_id": "vec",
                  "trace_length": "vec",
                  "start_time": "vec",
                  "rel_peak_time": "vec",
                  "det_time": "vec",
                  "e_det_time": "vec",
                  "isTriggered": "vec",
                  "sampling_speed": "vec",
                  "trace_x":"vec",
                  "trace_y":"vec",
                  "trace_z":"vec"
                  }

    create_branches(values, root_types, t)

    return values

# Create or Set the TTree branches for GRAND Efield traces and FFTs storage
def Setup_GRANDEfield_Branches(tree, create_branches=True):
    t = tree

    # Reset all branch addresses just in case
    t.ResetBranchAddresses()

    values = {"run_id": np.zeros(1, np.uint32),
              "evt_id": np.zeros(1, np.uint32),
              "det_id": ROOT.vector("int")(),        #TODO: Standarize the ID of antennas. Do we Want a number? A string? both (ID and Name). This will/should be linked to the RunInfo, where some detector configuration should reside.
              "trace_length": ROOT.vector("unsigned int")(), # Do we need it? Can be obtained from traces. On the other hand, small in storage and easy to use. ("Raw/SimPoints in Charles)
              "start_time": ROOT.vector("double")(), # start_time_gps? But will there be anything else than GPS?
                                                     # 4 bytes for nanoseconds, 4 bytes for unix time. This is enough until 2038. We should have more, but no 128 bit field in a TTree..
                                                     # (GPS in Charles, t_0 in Zhaires?)
              "rel_peak_time": ROOT.vector("float")(),     # offset between start and the peak of the signal (do we always have it from hardware?) (TPulse in Charles)
              "det_time": ROOT.vector("double")(),     # Not from the hardware! I don't like this name! time of the peak of the signal relative to the time that the shower hit the surface (do we always have it from hardware?) (DetTime in Charles)
              "e_det_time": ROOT.vector("double")(),     # uncertainty of the above (e_DetTime in Charles)
              "isTriggered": ROOT.vector("bool")(),
              "sampling_speed": ROOT.vector("float")(), # ToDo: Think if to move to detectorInfo. Constant, depends on the electronics. But can be added with different values during tests in the same detector. Isn't this constant (and thus should be in another tree?). Why float? (Raw/SimMSPS in Charles)
              "trace_x":ROOT.vector("vector<float>")(),        #TODO: I would like to store the three channels
              "trace_y":ROOT.vector("vector<float>")(),
              "trace_z":ROOT.vector("vector<float>")(),
              "fft_mag_x": ROOT.vector("vector<float>")(),
              "fft_mag_y": ROOT.vector("vector<float>")(),
              "fft_mag_z": ROOT.vector("vector<float>")(),
              "fft_phase_x": ROOT.vector("vector<float>")(),
              "fft_phase_y": ROOT.vector("vector<float>")(),
              "fft_phase_z": ROOT.vector("vector<float>")()
              }

    root_types = {"run_id": "/i",
                  "evt_id": "/i",
                  "det_id": "vec",
                  "trace_length": "vec",
                  "start_time": "vec",
                  "rel_peak_time": "vec",
                  "det_time": "vec",
                  "e_det_time": "vec",
                  "isTriggered": "vec",
                  "sampling_speed": "vec",
                  "trace_x":"vec",
                  "trace_y":"vec",
                  "trace_z":"vec",
                  "fft_mag_x": "vec",
                  "fft_mag_y": "vec",
                  "fft_mag_z": "vec",
                  "fft_phase_x": "vec",
                  "fft_phase_y": "vec",
                  "fft_phase_z": "vec"
                  }

    create_branches(values, root_types, t)

    return values

# Create or Set the TTree branches for each detector information
def Setup_GRANDDetectorInfo_Branches(tree,create_branches=True):
    t = tree

   # Reset all branch addresses just in case
    t.ResetBranchAddresses()

    values = {"det_id": np.zeros(1, np.uint32),
              "detector_model": ROOT.vector("string")(),
              "electronics_model": ROOT.vector("string")(),
              "position": np.zeros(3, np.float32),
             }
    root_types = {"det_id": "/i",
                  "detector_model": "/C",
                  "electronics_model": "/C",
                  "position": "[3]/F"
                 }

    create_branches(values, root_types, t)

    return values
