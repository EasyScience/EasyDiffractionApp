function calculated(xArray, slope, yIntercept) {
    return xArray.map(x => slope * x + yIntercept)
}

function pseudoMeasured(xArray, slope, yIntercept) {
    return xArray.map(x => slope * x + yIntercept + randomUniform(-0.1, 0.1))
}

function randomUniform(min, max) {
    return Math.random() * (max - min) + min
}
