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
        return "<root><item><label>Sin_1</label><color>darkolivegreen</color><parameters><item><amplitude>3.2</amplitude><period>2.1</period></item></parameters></item><item><label>Sin_2</label><color>steelblue</color><parameters><item><amplitude>2.5</amplitude><period>2.7</period></item></parameters></item></root>"
    }

    get phasesDict() {
        return [{"color":"darkolivegreen","label":"Sin_1","parameters":[{"amplitude":3.2,"period":2.1}]},{"color":"steelblue","label":"Sin_2","parameters":[{"amplitude":2.5,"period":2.7}]}]
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
