import os
import cryspy

f_name = 'rhochi.rcif'

rhochi = cryspy.file_to_globaln(f_name)
rhochi.apply_constraint()

crystals = rhochi.crystals()
model = rhochi.experiments()[0]
x_array = model.pd_meas.numpy_ttheta

result1 = model.calc_profile(
    x_array, crystals, flag_internal=True, flag_polarized=True
)

print('END')
