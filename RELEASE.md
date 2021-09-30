### Changes

- Implemented simulation and fitting of the time-of-flight (TOF) data using the [CrysPy](https://github.com/ikibalin/cryspy) calculation engine.
- Implemented two types (single and double) of parameter constraints for the fitting.
- Reset the estimated standard deviations on the `Analysis` page after fitting if the `Fit` box becomes unchecked.

### Bug Fixes

- The [lmfit](https://lmfit.github.io/lmfit-py/) minimization engine now works with the [CrysFML](https://code.ill.fr/scientific-software/crysfml) and [GSAS-II](https://subversion.xray.aps.anl.gov/trac/pyGSAS) calculators.
- Now project reset clears the simulated curve, experimental data, background and constraints tables.
- Size of the simulation/analysis chart on the `Summary` page has been fixed.
- The `Project save` button enable/disable is now properly defined.
- Fixed updating a sample model via the build-in `CIF editor`.
- Now undo/redo triggers a parameter table update on the `Analysis` page.
