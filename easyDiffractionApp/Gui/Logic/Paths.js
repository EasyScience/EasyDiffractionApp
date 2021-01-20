function component(fileName)
{
    const dirPath = Qt.resolvedUrl("../Components")
    const filePath = dirPath + "/" + fileName
    return filePath
}
