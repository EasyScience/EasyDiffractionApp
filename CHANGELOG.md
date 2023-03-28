# Version 0.8.5-beta (28 Mar 2023)

### Changes

- GSASII calculation engine has been removed.
- Overall application performance has been significantly improved.

### Bug Fixes

- Summary report export widget is now properly enabled for custom projects.
- Undo/redo functionality has been fixed.

# Version 0.8.4-beta (28 Jul 2022)

### New Features

- Simulating and fitting polarised data using the [CrysPy](https://github.com/ikibalin/cryspy) calculation engine.
- Reading CIF files with experimental data and instrumental parameters.

### Changes

- Default example with experimental phase has been modified.
- Added example projects with polarised data.
- Windows installer is now 64-bit.

### Bug Fixes

- CrysFML simulation now shows Bragg peaks.
- Inclusion of the space group setting in calculations.
- The `Project save` button is now disabled for read-only example projects.
- The `Reset state` functionality now resets calculator choice.
- Overall performance has been improved.

# Version 0.8.3-beta (27 Jan 2022)

### Features

- Simulating and fitting multi-phase data using the [CrysPy](https://github.com/ikibalin/cryspy) calculation engine is now supported.

### Changes

- The MacOS installer is now digitally signed allowing for safer and less intrusive installation process.

### Bug Fixes

- Adding a new atom is now case-insensitve.
- Changing sample name in the Sample tab functionality has been fixed.
- Performance of project load has been improved.

# Version 0.8.2-beta (5 Nov 2021)

### Features

- Simulating and fitting time-of-flight (TOF) data using the [CrysPy](https://github.com/ikibalin/cryspy) calculation engine is now supported.
- Dependent and independent parameter constraints can be constructed for use during fitting.

### Changes

- Reset the estimated standard deviations on the `Analysis` page after fitting if the `Fit` box becomes unchecked.

### Bug Fixes

- The [lmfit](https://lmfit.github.io/lmfit-py/) minimization engine now works with the [CrysFML](https://code.ill.fr/scientific-software/crysfml) and [GSAS-II](https://subversion.xray.aps.anl.gov/trac/pyGSAS) calculators.
- Now project reset clears the simulated curve, experimental data, background and constraints tables.
- Size of the simulation/analysis chart on the `Summary` page has been fixed.
- The `Project save` button enable/disable state is now properly defined.
- Fixed updating a sample model via the build-in `CIF editor`.
- Now undo/redo triggers a parameter table update on the `Analysis` page.

# Version 0.8.1-beta (8 Jun 2021)

### Changes

- Implemented automatic update of the application and made it easier to update the application manually.
- Implemented a file-less interface with the CrysPy calculation engine.
- Add Bragg peaks for the GSAS-II calculation engine.
- Fitting calculations do not block the GUI on macOS anymore (implemented threading).
- Redesigned and expanded the application settings window.

### Bug Fixes

- Added an icon to the application window on Windows and Linux.

# Version 0.8.0-beta.1 (7 May 2021)

### Changes

- CrysFML and CrysPy simulations now show Bragg peaks.
- Updated and extended user tutorials.
- Contact email more prominently displayed.
- More detailed `README.md` file for the project.
- Updated module dependencies.
- Updated application installer.

### Bug Fixes

- CrysFML and GSAS-II binding on Linux have been fixed.
- Now project reset clears the experimental data correctly.
- When an example is loaded, the summary save path is corrected.
- Broken links in the About box have been updated.
- Minor text fixes.

# Version 0.8.0-beta (3 May 2021)

This is a new version of easyDiffraction, which is now based on the easyScience framework. Whereas some features present in the original implementation have not yet been implemented, new easyDiffraction has improved GUI, additional back-end calculator interfaces, enhancement of minimization options and other improvements over the original version of easyDiffraction (0.7.0).

### New features in version 0.8.0:

- Ability to run in simulation-only mode
- Multiple crystallographic calculation engines: [CrysPy](https://github.com/ikibalin/cryspy), [CrysFML](https://code.ill.fr/scientific-software/crysfml) and [GSAS-II](https://subversion.xray.aps.anl.gov/trac/pyGSAS)
- Multiple minimization engines: [lmfit](https://lmfit.github.io/lmfit-py/), [bumps](https://github.com/bumps/bumps) and [DFO_LS](https://github.com/numericalalgorithmsgroup/dfols)
- High quality structure visualizer
- Interactive HTML report generation
- Built-in guided tutorials
- Improved visualization of experimental and simulated data
- Structural editor for cells and atoms
- Improved project management
- Parameter searching and filtering
- Engine independent cif interpreter/editor
- Engine independent background generation
