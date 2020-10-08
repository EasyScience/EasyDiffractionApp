class PyQmlProxy {

    // Properties

    get calculatorList() {
        return ["calculator1"]
    }

    get calculatorIndex() {
        return 0
    }

    get minimizerList() {
        return ["minimizer1"]
    }

    get minimizerIndex() {
        return 0
    }

    get amplitude() {
        return 3.5
    }

    get period() {
        return 2.0
    }

    get xShift() {
        return 0
    }

    get yShift() {
        return 0
    }

    get statusModelAsXml() {
        return "<root><item><label>Calculator</label><value>calculator1</value></item><item><label>Minimizer</label><value>minimizer1</value></item></root>"
    }

    get fitablesListAsXml() {
        return "<root><item><number>1</number><label>amplitude</label><value>3.5</value><unit></unit><error>0.0</error><fit>1</fit></item><item><number>2</number><label>period</label><value>3.141592653589793</value><unit></unit><error>0.0</error><fit>1</fit></item><item><number>3</number><label>x_shift</label><value>0.0</value><unit></unit><error>0.0</error><fit>1</fit></item><item><number>4</number><label>y_shift</label><value>0.0</value><unit></unit><error>0.0</error><fit>1</fit></item></root>"
    }

    get fitablesDict() {
        return {'amplitude': 3.5, 'period': 3.141592653589793, 'x_shift': 0.0, 'y_shift': 0.0}
    }

    get constraintsListAsXml() {
        return "<root><item><number>1</number><dependentName>amplitude</dependentName><relationalOperator>=</relationalOperator><value>1.0000</value><arithmeticOperator>*</arithmeticOperator><independentName>period</independentName><enabled>1</enabled></item><item><number>2</number><dependentName>amplitude</dependentName><relationalOperator>&lt;</relationalOperator><value>4.0000</value><arithmeticOperator></arithmeticOperator><independentName></independentName><enabled>1</enabled></item></root>"
    }

    get projectInfoAsJson() {
        return {"calculations":"experiments.cif","experiments":"experiments.cif","keywords":"sine, cosine, lmfit, bumps","modified":"18.09.2020, 09:24","name":"Example Project","samples":"samples.cif"}
    }

    get phasesXml() {
        //return "<root><item><label>Fe3O4</label><atoms><item><label>Fe1</label><type>Fe</type><x>0</x><y>0</y><z>0</z></item><item><label>Fe2</label><type>Fe</type><x>0.5</x><y>0</y><z>0</z></item><item><label>O</label><type>O</type><x>0.3421</x><y>0</y><z>0.5</z></item></atoms></item><item><label>CoO</label><atoms><item><label>Co</label><type>Co</type><x>0.5</x><y>0.25</y><z>0.5</z></item><item><label>O</label><type>O</type><x>0.75</x><y>0.75</y><z>0.75</z></item></atoms></item></root>"
        //return "<root><item><label>Sin_1</label><color>darkolivegreen</color><parameters><item><amplitude>3.2</amplitude><period>2.1</period></item></parameters></item><item><label>Sin_2</label><color>steelblue</color><parameters><item><amplitude>2.5</amplitude><period>2.7</period></item></parameters></item></root>"
        return "<root><item><label>Co2SiO4</label><color>darkolivegreen</color><crystal_system>orthorhombic</crystal_system><space_group_name>P n m a</space_group_name><space_group_setting>abc</space_group_setting><cell_length_a>10.28</cell_length_a><cell_length_b>10.28</cell_length_b><cell_length_c>10.28</cell_length_c><cell_angle_alpha>90.0</cell_angle_alpha><cell_angle_beta>90.0</cell_angle_beta><cell_angle_gamma>90.0</cell_angle_gamma><atoms><item><label>Co1</label><type>Co</type><color>coral</color><x>0.0</x><y>0.0</y><z>0.0</z><occupancy>1.0</occupancy><adp_type>Uiso</adp_type><adp_iso>0.004</adp_iso></item><item><label>Co2</label><type>Co</type><color>coral</color><x>0.279</x><y>0.279</y><z>0.279</z><occupancy>1.0</occupancy><adp_type>Uiso</adp_type><adp_iso>0.007</adp_iso></item><item><label>Si</label><type>Si</type><color>steelblue</color><x>0.094</x><y>0.094</y><z>0.094</z><occupancy>1.0</occupancy><adp_type>Uiso</adp_type><adp_iso>0.005</adp_iso></item><item><label>O1</label><type>O</type><color>darkolivegreen</color><x>0.091</x><y>0.091</y><z>0.091</z><occupancy>1.0</occupancy><adp_type>Uiso</adp_type><adp_iso>0.008</adp_iso></item><item><label>O2</label><type>O</type><color>darkolivegreen</color><x>0.448</x><y>0.448</y><z>0.448</z><occupancy>1.0</occupancy><adp_type>Uiso</adp_type><adp_iso>0.008</adp_iso></item><item><label>O3</label><type>O</type><color>darkolivegreen</color><x>0.164</x><y>0.164</y><z>0.164</z><occupancy>1.0</occupancy><adp_type>Uiso</adp_type><adp_iso>0.011</adp_iso></item></atoms></item><item><label>CoO</label><color>steelblue</color><crystal_system>cubic</crystal_system><space_group_name>F m -3 m</space_group_name><space_group_setting>1</space_group_setting><cell_length_a>3.02</cell_length_a><cell_length_b>3.02</cell_length_b><cell_length_c>3.02</cell_length_c><cell_angle_alpha>90.0</cell_angle_alpha><cell_angle_beta>90.0</cell_angle_beta><cell_angle_gamma>90.0</cell_angle_gamma><atoms><item><label>Co</label><type>Co</type><color>coral</color><x>0.0</x><y>0.0</y><z>0.0</z><occupancy>1.0</occupancy><adp_type>Uiso</adp_type><adp_iso>0.0</adp_iso></item><item><label>O</label><type>O</type><color>darkolivegreen</color><x>0.2471</x><y>0.4986</y><z>0.7497</z><occupancy>1.0</occupancy><adp_type>Uiso</adp_type><adp_iso>0.0</adp_iso></item></atoms></item></root>"
    }

    get phasesDict() {
        return [{"atoms":[{"adp_iso":0.004,"adp_type":"Uiso","color":"coral","label":"Co1","occupancy":1,"type":"Co","x":0,"y":0,"z":0},{"adp_iso":0.007,"adp_type":"Uiso","color":"coral","label":"Co2","occupancy":1,"type":"Co","x":0.279,"y":0.279,"z":0.279},{"adp_iso":0.005,"adp_type":"Uiso","color":"steelblue","label":"Si","occupancy":1,"type":"Si","x":0.094,"y":0.094,"z":0.094},{"adp_iso":0.008,"adp_type":"Uiso","color":"darkolivegreen","label":"O1","occupancy":1,"type":"O","x":0.091,"y":0.091,"z":0.091},{"adp_iso":0.008,"adp_type":"Uiso","color":"darkolivegreen","label":"O2","occupancy":1,"type":"O","x":0.448,"y":0.448,"z":0.448},{"adp_iso":0.011,"adp_type":"Uiso","color":"darkolivegreen","label":"O3","occupancy":1,"type":"O","x":0.164,"y":0.164,"z":0.164}],"cell_angle_alpha":90,"cell_angle_beta":90,"cell_angle_gamma":90,"cell_length_a":10.28,"cell_length_b":10.28,"cell_length_c":10.28,"color":"darkolivegreen","crystal_system":"orthorhombic","label":"Co2SiO4","space_group_name":"P n m a","space_group_setting":"abc"},{"atoms":[{"adp_iso":0,"adp_type":"Uiso","color":"coral","label":"Co","occupancy":1,"type":"Co","x":0,"y":0,"z":0},{"adp_iso":0,"adp_type":"Uiso","color":"darkolivegreen","label":"O","occupancy":1,"type":"O","x":0.2471,"y":0.4986,"z":0.7497}],"cell_angle_alpha":90,"cell_angle_beta":90,"cell_angle_gamma":90,"cell_length_a":3.02,"cell_length_b":3.02,"cell_length_c":3.02,"color":"steelblue","crystal_system":"cubic","label":"CoO","space_group_name":"F m -3 m","space_group_setting":"1"}]
    }

    get phasesCurrentIndex() {
        return 0
    }

    get parametersCurrentIndex() {
        return 0
    }
    // Functions

    addLowerMeasuredSeriesRef(series) {}

    addUpperMeasuredSeriesRef(series) {}

    setCalculatedSeriesRef(series) {}

    updateCalculatedData() {}

    generateMeasuredData() {}

    startFitting() {}

    editFitableValueByName(name, value) {}

    editFitableByIndexAndName(index, name, value) {}

    addConstraints(dependent_par_idx, operator, independent_par_idx) {}

    removeConstraintByIndex(index) {}

    toggleConstraintByIndex(index, enabled) {}

    editProjectInfoByKey(key, value) {}

    editPhase(p1, p2, p3) {}
}
