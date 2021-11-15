Feature: Check of the general functionality

Start the app, load an example project and check sanity of each tab

    Scenario: Open application and make sure all required elements are present

        Given Application is open
         When Start is clicked
          Then User can open a new project
          And User can not open help file
          And User can report a bug
          And User can not Save Project
          And User can not Undo
          And User can not Redo
          And User can select Home
          And User can not select Sample
          And User can not select Experiment
          And User can not select Analysis
          And User can not select Summary
          And User can select Create a New Project

         When Project tab is selected
         And The PbSO4 example is loaded
           Then Project Description has textual information
             And Reset Project is enabled

		 # Experimental data tab
         When Experiment tab is selected
           Then Experiment plot should be visible
           # And Experiment is HTML

         # Sample Model tab
         When Sample tab is selected
           Then Structure view should be visible

 		# Analysis tab
 		When Analysis tab is selected
 		  # Then Analysis plot should be visible
 		  Then Parameter table should be visible

		# Summary tab
 		When Summary tab is selected
 		  Then Report page should be visible
 		  Then Basic controls should be disabled

