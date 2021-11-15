# -*- coding: utf-8 -*-

# A quick introduction to implementing scripts for BDD tests:
#
# This file contains snippets of script code to be executed as the .feature
# file is processed. See the section 'Behaviour Driven Testing' in the 'API
# Reference Manual' chapter of the Squish manual for a comprehensive reference.
#
# The decorators Given/When/Then/Step can be used to associate a script snippet
# with a pattern which is matched against the steps being executed. Optional
# table/multi-line string arguments of the step are passed via a mandatory
# 'context' parameter:
#
#   @When("I enter the text")
#   def whenTextEntered(context):
#      <code here>
#
# The pattern is a plain string without the leading keyword, but a couple of
# placeholders including |any|, |word| and |integer| are supported which can be
# used to extract arbitrary, alphanumeric and integer values resp. from the
# pattern; the extracted values are passed as additional arguments:
#
#   @Then("I get |integer| different names")
#   def namesReceived(context, numNames):
#      <code here>
#
# Instead of using a string with placeholders, a regular expression can be
# specified. In that case, make sure to set the (optional) 'regexp' argument
# to True.

import names
import time

@Given("Application is open")
def step(context):
    startApplication("easyDiffraction")
    test.compare(waitForObjectExists(names.o_appContainer_Rectangle).visible, True)
    test.compare(waitForObjectExists(names.contentArea_Start_SideBarButton).enabled, True)
    test.compare(waitForObjectExists(names.contentArea_rocket_Label).enabled, True)
    mouseClick(waitForObject(names.contentArea_Start_SideBarButton), 98, 18, Qt.LeftButton)

#@When("Start is clicked")
#def step(context):
    # mouseClick(waitForObject(names.contentArea_Start_SideBarButton), 100, 20, Qt.LeftButton)
    #mouseClick(waitForObject(names.contentArea_Start_SideBarButton))

#@When("Start is clicked")
#def step(context):
#    mouseClick(waitForObject(names.contentArea_rocket_Label))

@Then("User can open a new project")
def step(context):
    # mouseClick(waitForObject(names.items_Create_a_new_project_Label), Qt.NoModifier, Qt.NoButton)
    test.compare(waitForObjectExists(names.items_Open_an_existing_project_SideBarButton).enabled, True)
    test.compare(str(waitForObjectExists(names.items_Open_an_existing_project_SideBarButton).text), "Open an existing project")

@Then("User can not open help file")
def step(context):
    test.compare(waitForObjectExists(names.o_Help).visible, True)
    test.compare(waitForObjectExists(names.o_Help).enabled, False)

@Then("User can report a bug")
def step(context):
    test.compare(waitForObjectExists(names.o_Bug).visible, True)
    test.compare(waitForObjectExists(names.o_Bug).enabled, True)

@Then("User can not Undo")
def step(context):
    test.compare(waitForObjectExists(names.easyDiffraction_Undo).enabled, False)


@When("A test file is loaded")
def step(context):
    mouseClick(waitForObject(names.open_an_existing_project_Open), 62, 17, Qt.LeftButton)
    snooze(2)
    nativeType("main.cif")
    snooze(1)
    nativeType("<Return>")
    snooze(1)
         
@When("A test file is loaded 2")
def step(context):
    mouseClick(waitForObject(names.o_Text))
    # Workaround for Windows not having the right winhook.dll
    snooze(2) 
    nativeType("main.cif")
    snooze(1)
    nativeType("<Return>")
    snooze(1)    
    
@When("Structure tab open")
def step(context):
    mouseClick(waitForObject(names.tabBar_image_IconImage), 17, 9, Qt.LeftButton)    

@When("Chart tab open")
def step(context):
    mouseClick(waitForObject(names.tabBar_Home_Button), 147, 20, Qt.LeftButton)
    mouseClick(waitForObject(names.easyDiffraction_Text_3))    
    #mouseClick(waitForObject(names.easyDiffraction_label_MnemonicLabel_6))

@When("Fitting tab open")
def step(context):
    mouseClick(waitForObject(names.easyDiffraction_Experimental_Data_Button), 334, 21, Qt.LeftButton)
    mouseClick(waitForObject(names.easyDiffraction_label_MnemonicLabel_5))
    mouseClick(waitForObject(names.easyDiffraction_label_MnemonicLabel_7))

@When("First parameter checked")
def step(context):
    test.compare(waitForObjectExists(names.contentRow_CheckBox).checked, True)

@Then("Fit button enabled")
def step(context):
    test.compare(waitForObjectExists(names.easyDiffraction_Start_fitting_Button).enabled, True)
    test.compare(str(waitForObjectExists(names.easyDiffraction_Start_fitting_Button).text), "Start fitting")

@When("Selected Experimental Data tab")
def step(context):
    mouseClick(waitForObject(names.easyDiffraction_label_MnemonicLabel_6))

@Then("Chart should be active")
def step(context):
    test.compare(waitForObjectExists(names.tabBar_Experimental_Data_Button).checked, True)
    test.compare(waitForObjectExists(names.tabBar_Experimental_Data_Button).enabled, True)


@Then("Chart should be visible")
def step(context):
    test.vp("VP1")

@Then("Chart Table View should be present")
def step(context):
    mouseClick(waitForObject(names.tabBar_label_MnemonicLabel))
    test.compare(str(waitForObjectExists(names.headerTableView_x_Text).text), "x")
    test.compare(waitForObjectExists(names.headerTableView_x_Text).visible, True)
    test.compare(waitForObjectExists(names.headerTableView_y_obs_up_Text).visible, True)
    test.compare(str(waitForObjectExists(names.headerTableView_y_obs_up_Text).text), "y_obs_up")
    test.compare(str(waitForObjectExists(names.headerTableView_sy_obs_up_Text).text), "sy_obs_up")
    test.compare(waitForObjectExists(names.headerTableView_sy_obs_up_Text).visible, True)
    test.compare(str(waitForObjectExists(names.contentTableView_TextInput).text), "10.1000")
    test.compare(waitForObjectExists(names.contentTableView_TextInput).visible, True)

@Then("Chart Text View should be present")
def step(context):
    test.compare(str(waitForObjectExists(names.tabBar_Text_View_TabButton).text), "Text View")
    test.compare(waitForObjectExists(names.tabBar_Text_View_TabButton).visible, True)

@When("Selected Sample Model tab")
def step(context):
    mouseClick(waitForObject(names.tabBar_Sample_Sample), 29, 17, Qt.LeftButton)

@Then("Structure should be visible")
def step(context):
    test.vp("VP2")

@Then("Structure should be active")
def step(context):
    test.compare(waitForObjectExists(names.tabBar_Structure_View_TabButton_2).enabled, True)
    test.compare(waitForObjectExists(names.tabBar_Structure_View_TabButton_2).visible, True)
    test.compare(str(waitForObjectExists(names.tabBar_Structure_View_TabButton_2).text), "Structure View")


@Then("Structure Text View should be present")
def step(context):
    mouseClick(waitForObject(names.tabBar_Text_View_TabButton_2), 242, 21, Qt.LeftButton)
    test.compare(waitForObjectExists(names.o_TextArea).enabled, True)
    test.compare(waitForObjectExists(names.o_TextArea).visible, True)


@Then("Analysis button enabled")
def step(context):
    mouseClick(waitForObject(names.tabBar_Structure_View_TabButton), 48, 20, Qt.LeftButton)
    test.compare(waitForObjectExists(names.easyDiffraction_Button).enabled, True)
    test.compare(str(waitForObjectExists(names.easyDiffraction_Button).text), "Analysis")
    test.compare(waitForObjectExists(names.easyDiffraction_Button).visible, True)


@When("Structure is rotated")
def step(context):
    mouseDrag(waitForObject(names.easyDiffraction_chart_QtDataVisualization_DeclarativeScatter), 501, 277, 252, 406, Qt.NoModifier, Qt.RightButton)


@When("Structure is reset")
def step(context):
    mouseClick(waitForObject(names.easyDiffraction_chart_QtDataVisualization_DeclarativeScatter), 494, 302, Qt.LeftButton)

@Then("Structure looks the same")
def step(context):
    test.vp("VP2")

@Then("Structure looks rotated")
def step(context):
    test.vp("VP1")

@Then("Structure looks different than original")
def step(context):
    test.vp("VP3")  # same structure as VP2 but with eception selected


@When("Structure is zoomed")
def step(context):
    mouseWheel(waitForObject(names.easyDiffraction_chart_QtDataVisualization_DeclarativeScatter), 494, 302, 0, -100, Qt.NoModifier)
    

@Then("user can select Show Animated Intro")
def step(context):
    test.compare(waitForObjectExists(names.easyDiffraction_Show_Animated_Intro_CheckBox).checkable, True)
    test.compare(waitForObjectExists(names.easyDiffraction_Show_Animated_Intro_CheckBox).checked, False)
    test.compare(waitForObjectExists(names.easyDiffraction_Show_Animated_Intro_CheckBox).visible, True)

@Then("user can select Show User Guides")
def step(context):
    test.compare(waitForObjectExists(names.easyDiffraction_Show_User_Guides_CheckBox).checkable, True)
    test.compare(waitForObjectExists(names.easyDiffraction_Show_User_Guides_CheckBox).checked, False)
    test.compare(waitForObjectExists(names.easyDiffraction_Show_User_Guides_CheckBox).visible, True)


@Then("Two options are visible")
def step(context):
    test.compare(waitForObjectExists(names.easyDiffraction_ColumnLayout_2).implicitHeight, 66)


@Then("Structure looks zoomed")
def step(context):
    test.vp("VP4")


@When("Experimental Data tab open")
def step(context):
    mouseClick(waitForObject(names.easyDiffraction_Text_3))

@Then("Chart looks like the default")
def step(context):
    test.vp("VP1")

@When("A peak is clicked")
def step(context):
    mouseClick(waitForObject(names.easyDiffraction_topChart_QtCharts_DeclarativeChart), 482, 363, Qt.LeftButton)

@Then("Coordinates are shown")
def step(context):
    mouseClick(waitForObject(names.easyDiffraction_topChart_QtCharts_DeclarativeChart), 483, 363, Qt.LeftButton)

@When("Chart is zoomed in")
def step(context):
    mouseWheel(waitForObject(names.easyDiffraction_topChart_QtCharts_DeclarativeChart), 384, 297, 0, 135, Qt.NoModifier)
    mouseClick(waitForObject(names.easyDiffraction_topChart_QtCharts_DeclarativeChart), 384, 297, Qt.LeftButton)
    mouseDrag(waitForObject(names.easyDiffraction_topChart_QtCharts_DeclarativeChart), 156, 285, 389, 258, Qt.NoModifier, Qt.LeftButton)

@Then("Chart looks different than original")
def step(context):
    test.vp("VP2")

@When("Right button clicked")
def step(context):
    mouseClick(waitForObject(names.easyDiffraction_topChart_QtCharts_DeclarativeChart), 414, 287, Qt.RightButton)

@Then("Symmetry and cell information shown")
def step(context):
    test.compare(waitForObjectExists(names.easyDiffraction_TextField).enabled, False)
    test.compare(waitForObjectExists(names.easyDiffraction_TextField).visible, True)
    test.compare(str(waitForObjectExists(names.easyDiffraction_TextField).text), "orthorhombic")
    test.compare(waitForObjectExists(names.easyDiffraction_TextField_2).enabled, False)
    test.compare(str(waitForObjectExists(names.easyDiffraction_TextField_2).displayText), "62.  P n m a")
    test.compare(waitForObjectExists(names.easyDiffraction_TextField_2).visible, True)
    test.compare(waitForObjectExists(names.easyDiffraction_TextField_3).enabled, False)
    test.compare(str(waitForObjectExists(names.easyDiffraction_TextField_3).displayText), "abc")
    test.compare(waitForObjectExists(names.easyDiffraction_TextField_3).visible, True)
    test.compare(waitForObjectExists(names.contentRow_8_5500_Text).enabled, True)
    test.compare(str(waitForObjectExists(names.contentRow_8_5500_Text).text), "8.4779")
    test.compare(waitForObjectExists(names.contentRow_8_5500_Text).visible, True)
    test.compare(waitForObjectExists(names.contentRow_8_5500_Text_2).enabled, True)
    test.compare(str(waitForObjectExists(names.contentRow_8_5500_Text_2).text), "5.3968")
    test.compare(waitForObjectExists(names.contentRow_8_5500_Text_2).visible, True)
    test.compare(waitForObjectExists(names.contentRow_8_5500_Text_3).enabled, True)
    test.compare(waitForObjectExists(names.contentRow_8_5500_Text_3).visible, True)
    test.compare(str(waitForObjectExists(names.contentRow_8_5500_Text_3).text), "6.9581")
    test.compare(waitForObjectExists(names.contentRow_90_0000_Text).enabled, True)
    test.compare(str(waitForObjectExists(names.contentRow_90_0000_Text).text), "90.0000")
    test.compare(waitForObjectExists(names.contentRow_90_0000_Text).visible, True)
    test.compare(waitForObjectExists(names.contentRow_90_0000_Text_2).enabled, True)
    test.compare(str(waitForObjectExists(names.contentRow_90_0000_Text_2).text), "90.0000")
    test.compare(waitForObjectExists(names.contentRow_90_0000_Text_2).visible, True)

@Then("Atomic coordinates section shown")
def step(context):
    test.compare(waitForObjectExists(names.contentRow_Fe3A_Text).enabled, True)
    test.compare(str(waitForObjectExists(names.contentRow_Fe3A_Text).text), "Pb")
    test.compare(waitForObjectExists(names.contentRow_Fe3A_Text).visible, True)
    test.compare(str(waitForObjectExists(names.contentRow_Fe3B_Text).text), "S")
    test.compare(waitForObjectExists(names.contentRow_Fe3B_Text).visible, True)
    test.compare(str(waitForObjectExists(names.contentRow_O1_Text).text), "O1")
    test.compare(waitForObjectExists(names.contentRow_O1_Text).visible, True)
    test.compare(waitForObjectExists(names.easyDiffraction_Color_Text).enabled, False)
    test.compare(str(waitForObjectExists(names.easyDiffraction_Color_Text).text), "Color")
    test.compare(waitForObjectExists(names.easyDiffraction_Color_Text).visible, True)
    test.compare(str(waitForObjectExists(names.contentRow_Rectangle).color.name), "#ed6a5e")
    test.compare(waitForObjectExists(names.contentRow_Rectangle).visible, True)
    test.compare(str(waitForObjectExists(names.o0_1872_Text).text), "0.1872")
    test.compare(str(waitForObjectExists(names.o0_0643_Text).text), "0.0643")
    test.compare(str(waitForObjectExists(names.o0_9079_Text).text), "0.9079")
    test.compare(str(waitForObjectExists(names.easyDiffraction_Add_new_atom_Button).text), "Add new atom")
    test.compare(waitForObjectExists(names.easyDiffraction_Add_new_atom_Button).visible, True)
    test.compare(waitForObjectExists(names.easyDiffraction_Remove_all_atoms_Button).enabled, False)
    test.compare(str(waitForObjectExists(names.easyDiffraction_Remove_all_atoms_Button).text), "Remove all atoms")
    test.compare(waitForObjectExists(names.easyDiffraction_Remove_all_atoms_Button).visible, True)

    
@Then("Atomic displacement section shown")
def step(context):
    test.compare(str(waitForObjectExists(names.easyDiffraction_Label_Text).text), "Label")
    test.compare(waitForObjectExists(names.easyDiffraction_Label_Text).visible, True)
    test.compare(waitForObjectExists(names.easyDiffraction_Label_Text).enabled, False)
    test.compare(waitForObjectExists(names.easyDiffraction_Type_Text).enabled, False)
    test.compare(str(waitForObjectExists(names.easyDiffraction_Type_Text).text), "Type")
    test.compare(waitForObjectExists(names.easyDiffraction_Type_Text).visible, True)
    test.compare(waitForObjectExists(names.easyDiffraction_Uiso_Text).enabled, False)
    test.compare(str(waitForObjectExists(names.easyDiffraction_Uiso_Text).text), "Uiso")
    test.compare(waitForObjectExists(names.easyDiffraction_Uiso_Text).visible, True)
    test.compare(waitForObjectExists(names.easyDiffraction_U11_Text).enabled, False)
    test.compare(str(waitForObjectExists(names.easyDiffraction_U11_Text).text), "U11")
    test.compare(waitForObjectExists(names.easyDiffraction_U11_Text).visible, True)
    test.compare(waitForObjectExists(names.easyDiffraction_U23_Text).enabled, False)
    test.compare(str(waitForObjectExists(names.easyDiffraction_U23_Text).text), "U23")
    test.compare(waitForObjectExists(names.easyDiffraction_U23_Text).visible, True)
    test.compare(waitForObjectExists(names.contentRow_1_Text).enabled, True)
    test.compare(str(waitForObjectExists(names.contentRow_1_Text).text), "1")
    test.compare(waitForObjectExists(names.contentRow_1_Text).visible, True)
    test.compare(waitForObjectExists(names.contentRow_Fe3A_Text_2).enabled, True)
    test.compare(str(waitForObjectExists(names.contentRow_Fe3A_Text_2).text), "Pb")
    test.compare(waitForObjectExists(names.contentRow_Fe3A_Text_2).visible, True)
    test.compare(waitForObjectExists(names.contentRow_uani_Text).enabled, True)
    test.compare(str(waitForObjectExists(names.contentRow_uani_Text).text), "Uiso")
    test.compare(waitForObjectExists(names.contentRow_uani_Text).visible, True)
    test.compare(waitForObjectExists(names.contentRow_0_0000_Text).enabled, True)
    test.compare(str(waitForObjectExists(names.contentRow_0_0000_Text).text), "0.0000")
    test.compare(waitForObjectExists(names.contentRow_0_0000_Text).visible, True)
    test.compare(waitForObjectExists(names.contentRow_O1_Text_2).enabled, True)
    test.compare(waitForObjectExists(names.contentRow_O1_Text_2).visible, True)
    test.compare(str(waitForObjectExists(names.contentRow_O1_Text_2).text), "O1")
    test.compare(waitForObjectExists(names.contentRow_0_0000_Text_2).enabled, True)
    test.compare(str(waitForObjectExists(names.contentRow_0_0000_Text_2).text), "0.0000")
    test.compare(waitForObjectExists(names.contentRow_0_0000_Text_2).visible, True)
    test.compare(waitForObjectExists(names.contentRow_Text).enabled, True)
    test.compare(str(waitForObjectExists(names.contentRow_Text).text), "")
    test.compare(waitForObjectExists(names.contentRow_Text).visible, True)
    test.compare(waitForObjectExists(names.contentRow_Text_2).enabled, True)
    test.compare(waitForObjectExists(names.contentRow_Text_2).visible, True)
    test.compare(str(waitForObjectExists(names.contentRow_Text_2).text), "")

@Then("Magnetic susceptibility section shown")
def step(context):
    test.compare(waitForObjectExists(names.easyDiffraction_iso_Text).enabled, False)
    test.compare(str(waitForObjectExists(names.easyDiffraction_iso_Text).text), "χiso")
    test.compare(waitForObjectExists(names.easyDiffraction_iso_Text).visible, True)
    test.compare(waitForObjectExists(names.easyDiffraction_23_Text).enabled, False)
    test.compare(str(waitForObjectExists(names.easyDiffraction_23_Text).text), "χ23")
    test.compare(waitForObjectExists(names.easyDiffraction_23_Text).visible, True)
    test.compare(waitForObjectExists(names.contentRow_2_Text).enabled, True)
    test.compare(str(waitForObjectExists(names.contentRow_2_Text).text), "2")
    test.compare(waitForObjectExists(names.contentRow_2_Text).visible, True)
    test.compare(waitForObjectExists(names.contentRow_Text_3).enabled, True)
    test.compare(str(waitForObjectExists(names.contentRow_Text_3).text), "")
    test.compare(waitForObjectExists(names.contentRow_Text_3).visible, True)
    test.compare(waitForObjectExists(names.contentRow_O1_Text_3).enabled, True)
    test.compare(str(waitForObjectExists(names.contentRow_O1_Text_3).text), "O1")
    test.compare(waitForObjectExists(names.contentRow_O1_Text_3).visible, True)
    test.compare(waitForObjectExists(names.contentRow_Text_4).enabled, True)
    test.compare(str(waitForObjectExists(names.contentRow_Text_4).text), "")
    test.compare(waitForObjectExists(names.contentRow_Text_4).visible, True)
    test.compare(waitForObjectExists(names.contentRow_Text_5).enabled, True)
    test.compare(str(waitForObjectExists(names.contentRow_Text_5).text), "")
    test.compare(waitForObjectExists(names.contentRow_Text_5).visible, True)

@Then("Fitting chart is visible 2")
def step(context):
    test.vp("VP1")

@Then("Difference chart is visible 2")
def step(context):
    test.vp("VP2")

@When("Parameter 1 value is changed")
def step(context):
    mouseClick(waitForObject(names.contentRow_qwe_TextInput), 35, 19, Qt.LeftButton)
    type(waitForObject(names.contentRow_qwe_TextInput), "<Backspace>")
    type(waitForObject(names.contentRow_qwe_TextInput), "11")
    type(waitForObject(names.contentRow_qwe_TextInput), "<Return>")
    time.sleep(2.0)    

#def step(context):
#    test.compare(str(waitForObjectExists(names.contentRow_qwe_TextInput).text), "11.5500")

@Then("The fitting chart looks different")
def step(context):
    test.vp("VP3")

@When("Parameter value slider is moved")
def step(context):
    longMouseDrag(waitForObject(names.easyDiffraction_sliderHandle_Rectangle), 8, 15, -9, 1, Qt.NoModifier, Qt.LeftButton)
    time.sleep(2.0)
    #if waitFor("names.contentRow_qwe_TextInput.text == 8.7176", 2000):
    #    test.passes("Property had the expected value")
    #else:
    #    test.fail("Property did not have the expected value")


@Then("The fitting chart looks different 2")
def step(context):
    test.vp("VP7")


@Then("Fitting chart is visible")
def step(context):
    test.vp("VP5")

@Then("Difference chart is visible")
def step(context):
    test.vp("VP6")


@Then("Parameter value is changed")
def step(context):
    test.compare(str(waitForObjectExists(names.o_TextInput).text), "8.2357")

@Then("Default parameters are unchecked for fitting")
def step(context):
    test.compare(waitForObjectExists(names.contentRow_CheckBox).checked, False)
    test.compare(waitForObjectExists(names.contentRow_CheckBox).enabled, True)
    test.compare(waitForObjectExists(names.contentRow_CheckBox_2).checked, False)
    mouseDrag(waitForObject(names.contentListView_Rectangle_2), 4, 71, 31, 153, Qt.NoModifier, Qt.LeftButton)       
    test.compare(waitForObjectExists(names.contentRow_CheckBox_3).checked, False)
    test.compare(waitForObjectExists(names.contentRow_CheckBox_4).checked, False)

@Then("Default parameters are checked for fitting 2")
def step(context):
    test.compare(waitForObjectExists(names.contentRow_CheckBox).checked, True)
    test.compare(waitForObjectExists(names.contentRow_CheckBox).enabled, True)
    test.compare(waitForObjectExists(names.contentRow_CheckBox_2).checked, True)
    mouseDrag(waitForObject(names.contentListView_Rectangle_2), 4, 71, 31, 153, Qt.NoModifier, Qt.LeftButton)       
    test.compare(waitForObjectExists(names.contentRow_CheckBox_3).checked, True)
    test.compare(waitForObjectExists(names.contentRow_CheckBox_4).checked, True)

@When("Default parameters are checked for fitting")
def step(context):
    test.compare(waitForObjectExists(names.contentRow_CheckBox).checked, True)
    test.compare(waitForObjectExists(names.contentRow_CheckBox).enabled, True)
    test.compare(waitForObjectExists(names.contentRow_CheckBox_2).checked, True)
    mouseDrag(waitForObject(names.contentListView_Rectangle_2), 4, 71, 31, 153, Qt.NoModifier, Qt.LeftButton)       
    test.compare(waitForObjectExists(names.contentRow_CheckBox_3).checked, True)
    test.compare(waitForObjectExists(names.contentRow_CheckBox_4).checked, True)
        
@Then("Fitting can be performed")
def step(context):
    test.compare(waitForObjectExists(names.easyDiffraction_Start_fitting_Button).enabled, True)
    test.compare(str(waitForObjectExists(names.easyDiffraction_Start_fitting_Button).text), "Start fitting")
    test.compare(waitForObjectExists(names.easyDiffraction_Start_fitting_Button).visible, True)


@Then("Fitting cannot be performed")
def step(context):
    test.compare(waitForObjectExists(names.start_fitting_PausePlay).enabled, True)
    test.compare(str(waitForObjectExists(names.start_fitting_PausePlay).text), "Start fitting")

@When("Fitting started")
def step(context):
    mouseClick(waitForObject(names.start_fitting_PausePlay))

@Then("Wait for fitting finished 2")
def step(context):
    test.compare(waitForObjectExists(names.o_Rectangle, 10000).visible, True)

@When("Fitting finished")
def step(context):
    test.compare(waitForObjectExists(names.o_Rectangle, 10000).visible, True)

@Then("Fitting details are shown 2")
def step(context):
    test.compare(waitForObjectExists(names.optimization_terminated_successfully_Number_of_evaluations_of_the_objective_functions_120_Number_of_iterations_performed_by_the_optimizer_15_Final_goodnes_of_fit_3_00_Label).visible, True)
    #test.compare(str(waitForObjectExists(names.optimization_terminated_successfully_Number_of_evaluations_of_the_objective_functions_120_Number_of_iterations_performed_by_the_optimizer_15_Final_goodnes_of_fit_3_00_Label).text), "Optimization terminated successfully.\nNumber of evaluations of the objective functions: 120\nNumber of iterations performed by the optimizer: 15\nFinal goodness-of-fit (χ²): 3.00")
    test.compare(str(waitForObjectExists(names.optimization_terminated_successfully_Number_of_evaluations_of_the_objective_functions_120_Number_of_iterations_performed_by_the_optimizer_15_Final_goodnes_of_fit_3_00_Label).text), "Desired error not necessarily achieved due to precision loss.")
    mouseClick(waitForObject(names.o_Rectangle_2), 932, 306, Qt.LeftButton)
    
@Then("Select first parameter for fitting")
def step(context):
    mouseClick(waitForObject(names.contentRow_CheckBox_2), 20, 17, Qt.LeftButton)


@Then("Wait for fitting finished")
def step(context):
    test.compare(waitForObjectExists(names.o_Rectangle, 20000).visible, True)

@Then("Fitting details are shown")
def step(context):
    test.compare(str(waitForObjectExists(names.optimization_terminated_successfully_Number_of_evaluations_of_the_objective_functions_120_Number_of_iterations_performed_by_the_optimizer_15_Final_goodnes_of_fit_3_00_Label).text), "Desired error not necessarily achieved due to precision loss.\n\nGoodness-of-fit (χ²): 332.39\nNum. refined parameters: 1")
    test.compare(waitForObjectExists(names.optimization_terminated_successfully_Number_of_evaluations_of_the_objective_functions_120_Number_of_iterations_performed_by_the_optimizer_15_Final_goodnes_of_fit_3_00_Label).visible, True)
    mouseClick(waitForObject(names.o_Rectangle), 932, 306, Qt.LeftButton)


@Then("Optimized parameters are displayed 2")
def step(context):
    test.compare(waitForObjectExists(names.contentRow_qwe_TextInput).visible, True)
    test.compare(str(waitForObjectExists(names.contentRow_qwe_TextInput).text), "8.5626")
    test.compare(waitForObjectExists(names.contentRow_qwe_TextInput_2).visible, True)
    test.compare(str(waitForObjectExists(names.contentRow_qwe_TextInput_2).text), "-3.4751")

@Then("Error for optimized parameters is displayed 2")
def step(context):
    test.compare(str(waitForObjectExists(names.contentRow_0_0008_Text).text), "0.0008")
    test.compare(waitForObjectExists(names.contentRow_0_0008_Text).visible, True)
    #test.compare(str(waitForObjectExists(names.contentRow_Text_7).text), "0.0551")
    test.compare(waitForObjectExists(names.contentRow_Text_7).visible, True)


@Then("Text report is available 2")
def step(context):
    test.compare(waitForObjectExists(names.tabBar_Report_TabButton).enabled, True)
    test.compare(waitForObjectExists(names.tabBar_Report_TabButton).visible, True)
    test.compare(str(waitForObjectExists(names.tabBar_Report_TabButton).text), "Report")
    test.compare(waitForObjectExists(names.easyDiffraction_textArea_TextArea).visible, True)

@Then("Export report is available 2")
def step(context):
    test.compare(waitForObjectExists(names.easyDiffraction_Export_as_GroupBox).collapsed, False)
    test.compare(waitForObjectExists(names.easyDiffraction_Export_as_GroupBox).visible, True)
    test.compare(str(waitForObjectExists(names.easyDiffraction_Export_as_GroupBox).title), "Export as...")
    test.compare(waitForObjectExists(names.easyDiffraction_TextField).enabled, True)
    test.compare(waitForObjectExists(names.easyDiffraction_TextField).visible, True)
    test.compare(str(waitForObjectExists(names.easyDiffraction_TextField).placeholderText), "Report File Name")
    test.compare(waitForObjectExists(names.easyDiffraction_exportFileExt_ComboBox).currentIndex, 0)
    test.compare(str(waitForObjectExists(names.easyDiffraction_exportFileExt_ComboBox).currentText), ".HTML")
    test.compare(waitForObjectExists(names.easyDiffraction_exportFileExt_ComboBox).visible, True)
    test.compare(waitForObjectExists(names.easyDiffraction_Export_Button).enabled, True)
    test.compare(str(waitForObjectExists(names.easyDiffraction_Export_Button).text), "Export")
    test.compare(waitForObjectExists(names.easyDiffraction_Export_Button).visible, True)

   
    
@When("All parameters are deselected 2")
def step(context):
    mouseClick(waitForObject(names.contentRow_ColorImage), 16, 18, Qt.LeftButton)
    mouseClick(waitForObject(names.contentRow_ColorImage_2), 12, 15, Qt.LeftButton)
    mouseDrag(waitForObject(names.contentListView_Rectangle_2), 4, 62, 3, 159, Qt.NoModifier, Qt.LeftButton)
    mouseClick(waitForObject(names.contentRow_ColorImage_3), 11, 16, Qt.LeftButton)
    mouseClick(waitForObject(names.contentRow_ColorImage_4), 13, 12, Qt.LeftButton)

@Then("Wait for bad fitting finished 2")
def step(context):
    test.compare(waitForObjectExists(names.o_Rectangle, 20000).visible, True)
        
    mouseClick(waitForObject(names.easyDiffraction_label_MnemonicLabel_8))
    test.compare(waitForObjectExists(names.o_Rectangle).enabled, True)
    test.compare(waitForObjectExists(names.o_Rectangle).visible, True)
    test.compare(waitForObjectExists(names.unknow_problems_during_refinement_Label).visible, True)
    test.compare(str(waitForObjectExists(names.unknow_problems_during_refinement_Label).text), "Unknow problems during refinement")

@When("Symmetry and cell parameters opened")
def step(context):
    mouseClick(waitForObject(names.image_IconImage), 7, 4, Qt.LeftButton)

@When("Symmetry and cell parameters closed")
def step(context):
    mouseClick(waitForObject(names.image_IconImage_2), 3, 4, Qt.LeftButton)

@When("Atoms, atomic coordinates and occupation opened")
def step(context):
    mouseClick(waitForObject(names.image_IconImage_3), 1, 3, Qt.LeftButton)

@When("Atoms, atomic coordinates and occupation closed")
def step(context):
    mouseClick(waitForObject(names.image_IconImage_2), 4, 3, Qt.LeftButton)

@When("Atomic displacement parameters opened")
def step(context):
    mouseClick(waitForObject(names.image_IconImage_4), 3, 1, Qt.LeftButton)

@When("Atomic displacement parameter closed")
def step(context):
    mouseClick(waitForObject(names.image_IconImage_2), 3, 1, Qt.LeftButton)

@When("Magnetic susceptibility parameters opened")
def step(context):
    mouseClick(waitForObject(names.image_IconImage_5), 7, 4, Qt.LeftButton)


@Then("User can not Save Project")
def step(context):
    test.compare(waitForObjectExists(names.easyDiffraction_SaveState).enabled, False)
    test.compare(waitForObjectExists(names.easyDiffraction_SaveState).visible, True)

@Then("User can not Redo")
def step(context):
    test.compare(waitForObjectExists(names.easyDiffraction_Redo).enabled, False)
    test.compare(waitForObjectExists(names.easyDiffraction_Redo).visible, True)


@Then("User can select Create a New Project")
def step(context):
    test.compare(waitForObjectExists(names.create_a_new_project_Create).checkable, False)
    test.compare(waitForObjectExists(names.create_a_new_project_Create).enabled, True)



@Given("Simulation started")
def step(context):
    mouseClick(waitForObject(names.label_MnemonicLabel_3))

        

@Then("Home page has textual information")
def step(context):
    test.compare(str(waitForObjectExists(names.pbSO4_Text).text), "PbSO4\n")
    test.compare(waitForObjectExists(names.pbSO4_Text).visible, True)
    test.compare(waitForObjectExists(names.project_Keywords_Text).visible, True)
    test.compare(str(waitForObjectExists(names.project_Keywords_Text).text), "Project Keywords:")
    test.compare(waitForObjectExists(names.unpolarised_neutron_diffraction_powder_1d_Text).visible, True)
    test.compare(str(waitForObjectExists(names.unpolarised_neutron_diffraction_powder_1d_Text).text), "unpolarised neutron diffraction, powder, 1d")
    test.compare(waitForObjectExists(names.phases_Text).visible, True)
    test.compare(str(waitForObjectExists(names.phases_Text).text), "Phases:")
    test.compare(waitForObjectExists(names.pbSO4_Text_2).visible, True)
    test.compare(str(waitForObjectExists(names.pbSO4_Text_2).text), "PbSO4")
    test.compare(waitForObjectExists(names.easyDiffraction_Text_5).visible, True)
    test.compare(str(waitForObjectExists(names.easyDiffraction_Text_5).text), "Experiments:")
    test.compare(str(waitForObjectExists(names.pd_Text).text), "pd")
    test.compare(waitForObjectExists(names.pd_Text).visible, True)
    test.compare(str(waitForObjectExists(names.easyDiffraction_Text_4).text), "Instrument:")
    test.compare(waitForObjectExists(names.easyDiffraction_Text_4).visible, True)
    test.compare(str(waitForObjectExists(names.o6T2_at_LLB_Text).text), "6T2 at LLB")
    test.compare(waitForObjectExists(names.o6T2_at_LLB_Text).visible, True)



@Then("Optimized parameters are displayed")
def step(context):
    test.compare(str(waitForObjectExists(names.o_TextInput).text), "8.4790")
    test.compare(waitForObjectExists(names.o_TextInput).visible, True)
    test.compare(str(waitForObjectExists(names.ang_Text).text), "ang")
    test.compare(waitForObjectExists(names.ang_Text).visible, True)


@Then("Error for optimized parameters is displayed")
def step(context):
    test.compare(str(waitForObjectExists(names.o0_0001_Text).text), "0.0001")
    test.compare(waitForObjectExists(names.o0_0001_Text).visible, True)

@Then("Text report is available")
def step(context):
    test.compare(waitForObjectExists(names.easyDiffraction_textArea_TextArea).visible, True)
    test.compare(str(waitForObjectExists(names.easyDiffraction_textArea_TextArea).id), "textArea")

@Then("Export report is available")
def step(context):
    test.compare(str(waitForObjectExists(names.easyDiffraction_Export_as_GroupBox).title), "Export as...")
    test.compare(waitForObjectExists(names.easyDiffraction_Export_as_GroupBox).enabled, True)
    test.compare(waitForObjectExists(names.easyDiffraction_exportFileExt_ComboBox).enabled, True)
    test.compare(str(waitForObjectExists(names.easyDiffraction_exportFileExt_ComboBox).currentText), ".HTML")
    test.compare(waitForObjectExists(names.easyDiffraction_exportFileExt_ComboBox).count, 2)
    test.compare(waitForObjectExists(names.export_Export).enabled, True)
    test.compare(str(waitForObjectExists(names.export_Export).text), "Export")


@When("All parameters are deselected")
def step(context):
    mouseClick(waitForObject(names.o_ColorImage), 15, 10, Qt.LeftButton)


@Then("Wait for bad fitting finished")
def step(context):
    #mouseClick(waitForObject(names.image_IconImage_6), 12, 8, Qt.LeftButton)
    #mouseClick(waitForObject(names.label_MnemonicLabel))
    #mouseWheel(waitForObject(names.phases_PbSO4_atoms_S_fract_z_Text), 243, 21, 0, -15, Qt.NoModifier)
    #mouseWheel(waitForObject(names.o_Text_2), 52, 26, 0, -15, Qt.NoModifier)
    #mouseDrag(waitForObject(names.o_Rectangle_3), 5, 20, 5, -292, Qt.NoModifier, Qt.LeftButton)
    
    mouseClick(waitForObject(names.image_IconImage_6), 19, 9, Qt.LeftButton)
    test.compare(waitForObjectExists(names.o_Rectangle).visible, True)
    test.compare(str(waitForObjectExists(names.no_parameters_selected_for_refinement_Text).text), "No parameters selected for refinement")
    test.compare(waitForObjectExists(names.no_parameters_selected_for_refinement_Text).visible, True)


@Then("User can select Start Simulation")
def step(context):
    test.compare(str(waitForObjectExists(names.start_Simulation_Refinement_TabButton).text), "Start Simulation/Refinement")
    test.compare(waitForObjectExists(names.start_Simulation_Refinement_TabButton).visible, True)
    test.compare(str(waitForObjectExists(names.start_Simulation_Refinement_TabButton).background.color.name), "#2a99d9")

@Then("User can open About box")
def step(context):
    mouseClick(waitForObject(names.about_easyDiffraction_Text))
    test.compare(waitForObjectExists(names.o_Rectangle).visible, True)
    test.compare(waitForObjectExists(names.o_Rectangle).enabled, True)
    test.compare(str(waitForObjectExists(names.end_User_Licence_Agreement_Text).text), "End User Licence Agreement")
    test.compare(waitForObjectExists(names.end_User_Licence_Agreement_Text).enabled, True)
    test.compare(waitForObjectExists(names.dependent_Open_Source_Licenses_Text).enabled, True)
    test.compare(str(waitForObjectExists(names.dependent_Open_Source_Licenses_Text).text), "Dependent Open Source Licenses")
    mouseClick(waitForObject(names.label_MnemonicLabel))
    
@Then("User can open Video Tutorial link")
def step(context):
    test.compare(str(waitForObjectExists(names.easyDiffraction_Text_2).text), "Get Started Video Tutorial")
    test.compare(waitForObjectExists(names.easyDiffraction_Text_2).enabled, True)

@Then("User can open Online Documentation link")
def step(context):
    test.compare(waitForObjectExists(names.online_Documentation_Text).enabled, True)
    test.compare(str(waitForObjectExists(names.online_Documentation_Text).text), "Online Documentation")

@Then("User can open a Touch Online link")
def step(context):
    test.compare(waitForObjectExists(names.get_in_Touch_Online_Text).enabled, True)
    test.compare(str(waitForObjectExists(names.get_in_Touch_Online_Text).text), "Get in Touch Online")
    



@Then("User can select Home")
def step(context):
    test.compare(waitForObjectExists(names.appBarCentralTabs_Home_AppBarTabButton).enabled, True)
    test.compare(waitForObjectExists(names.appBarCentralTabs_Home_AppBarTabButton).visible, True)


@Then("User can not select Sample")
def step(context):
    test.compare(waitForObjectExists(names.appBarCentralTabs_Sample_AppBarTabButton).visible, True)
    test.compare(waitForObjectExists(names.appBarCentralTabs_Sample_AppBarTabButton).enabled, False)

@Then("User can not select Experiment")
def step(context):
    test.compare(waitForObjectExists(names.appBarCentralTabs_Experiment_AppBarTabButton).enabled, False)
    test.compare(waitForObjectExists(names.appBarCentralTabs_Experiment_AppBarTabButton).visible, True)

@Then("User can not select Analysis")
def step(context):
    test.compare(waitForObjectExists(names.appBarCentralTabs_Analysis_AppBarTabButton).enabled, False)
    test.compare(waitForObjectExists(names.appBarCentralTabs_Analysis_AppBarTabButton).visible, True)

@Then("User can not select Summary")
def step(context):
    test.compare(waitForObjectExists(names.appBarCentralTabs_Summary_AppBarTabButton).enabled, False)
    test.compare(waitForObjectExists(names.appBarCentralTabs_Summary_AppBarTabButton).visible, True)


@When("Program Preferences opened")
def step(context):
    mouseClick(waitForObject(names.o_label_MnemonicLabel))

@Then("User can select Prompts")
def step(context):
    test.compare(waitForObjectExists(names.view_toolTipsCheckBox_CheckBox).checked, True)
    test.compare(waitForObjectExists(names.view_toolTipsCheckBox_CheckBox).checkable, True)

@Then("User can select Updates")
def step(context):
    mouseClick(waitForObject(names.bar_Rectangle), 111, 35, Qt.LeftButton)
    test.compare(str(waitForObjectExists(names.view_Check_now_SideBarButton).text), "Check now")
    test.compare(waitForObjectExists(names.view_Check_now_SideBarButton).enabled, True)

@Then("User can select Appearance")
def step(context):
    mouseClick(waitForObject(names.bar_Rectangle), 176, 39, Qt.LeftButton)
    test.compare(waitForObjectExists(names.view_ComboBox).enabled, True)
    test.compare(str(waitForObjectExists(names.view_ComboBox).currentText), "System")
    test.compare(str(waitForObjectExists(names.view_ComboBox_2).displayText), "bokeh")
    test.compare(waitForObjectExists(names.view_ComboBox_2).enabled, True)
    test.compare(waitForObjectExists(names.view_ComboBox_3).enabled, True)
    test.compare(str(waitForObjectExists(names.view_ComboBox_3).displayText), "chemdoodle")

@Then("User can select Experimental")
def step(context):
    mouseClick(waitForObject(names.bar_Rectangle), 268, 36, Qt.LeftButton)
    test.compare(waitForObjectExists(names.view_ComboBox_4).enabled, True)
    test.compare(str(waitForObjectExists(names.view_ComboBox_4).displayText), "100%")
    test.compare(waitForObjectExists(names.view_languageSelector_ComboBox).enabled, True)
    test.compare(str(waitForObjectExists(names.view_languageSelector_ComboBox).displayText), "English")

@Then("User can select Develop")
def step(context):
    mouseClick(waitForObject(names.bar_Rectangle), 340, 54, Qt.LeftButton)
    test.compare(waitForObjectExists(names.view_ComboBox_5).enabled, False)
    test.compare(str(waitForObjectExists(names.view_ComboBox_5).displayText), "Terminal")
    test.compare(waitForObjectExists(names.view_ComboBox_6).enabled, False)
    test.compare(str(waitForObjectExists(names.view_ComboBox_6).displayText), "Debug")

@When("The PbSO4 example is loaded")
def step(context):
    mouseClick(waitForObject(names.items_Rectangle), 506, 53, Qt.LeftButton)

@Then("Project Description has textual information")
def step(context):
    test.compare(str(waitForObjectExists(names.items_TextInput).text), "PbSO4")
    test.compare(str(waitForObjectExists(names.items_TextInput_2).text), "neutrons, powder, constant wavelength, 1D")

@When("Experiment tab is selected")
def step(context):
    mouseClick(waitForObject(names.appBarCentralTabs_Rectangle), 219, 25, Qt.LeftButton)

@When("Sample tab is selected")
def step(context):
    mouseClick(waitForObject(names.appBarCentralTabs_Rectangle), 146, 43, Qt.LeftButton)


@Then("Reset Project is enabled")
def step(context):
    test.compare(waitForObjectExists(names.o_ToolButton).enabled, True)
    test.compare(waitForObjectExists(names.o_ToolButton).visible, True)

@Then("Experiment plot should be visible")
def step(context):
    test.compare(waitForObjectExists(names.items_chartView_WebEngineView).visible, True)
    #test.compare(waitForObjectExists(names.o_container_container_container_o_QQuickApplicationWindow_id_contentArea_type_ContentArea_unnamed_1_visible_true_id_items_occurrence_5_type_SwipeView_unnamed_1_visible_true_type_ExperimentDataChartBokeh_unnamed_1_visible_true_chartView_0_DOCUMENT_HTML1).visible, True)


@When("Project tab is selected")
def step(context):
    mouseClick(waitForObject(names.appBarCentralTabs_Rectangle), 91, 39, Qt.LeftButton)



@Then("Structure view should be visible")
def step(context):
    test.imagePresent("image_1")

@When("Analysis tab is selected")
def step(context):
    mouseClick(waitForObject(names.appBarCentralTabs_Rectangle), 289, 32, Qt.LeftButton)

@Then("Analysis plot should be visible")
def step(context):
    test.imagePresent("image_2")

@Then("Parameter table should be visible")
def step(context):
    test.compare(waitForObjectExists(names.items_AnalysisFitables).visible, True)
    test.compare(waitForObjectExists(names.items_AnalysisFitables).enabled, True)
    test.compare(str(waitForObjectExists(names.items_valueColumn_TableViewTextInput).text), "8.4781")


@When("Summary tab is selected")
def step(context):
    mouseClick(waitForObject(names.appBarCentralTabs_Rectangle), 375, 26, Qt.LeftButton)

@Then("Report page should be visible")
def step(context):
    # test.compare(waitForObjectExists(names.o_container_container_container_o_QQuickApplicationWindow_id_contentArea_type_ContentArea_unnamed_1_visible_true_id_items_occurrence_9_type_SwipeView_unnamed_1_visible_true_id_webView_type_WebEngineView_unnamed_1_visible_true_DOCUMENT).visible, True)
    test.compare(waitForObjectExists(names.items_webView_WebEngineView).visible, True)

@Then("Basic controls should be disabled")
def step(context):
    test.compare(waitForObjectExists(names.items_Export_report_GroupBox).enabled, False)


@Then("Experiment is HTML")
def step(context):
    test.compare(waitForObjectExists(names.items_chartView_WebEngineView).visible, True)
    test.compare(waitForObjectExists(names.o_container_contentArea_items_SwipeView_4_id_chartView_type_WebEngineView_unnamed_1_visible_true_DOCUMENT_HTML1).tagName, "HTML")


@When("Start is clicked")
def step(context):
    mouseClick(waitForObject(names.contentArea_Start_Label))
