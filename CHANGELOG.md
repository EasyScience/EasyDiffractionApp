# Version 0.8.0-beta.2 (12 May 2021)

### Changes

- Implement automatic update and simplify update app manually.

### Bug Fixes

- Add application window icon on Windows and Linux.

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
