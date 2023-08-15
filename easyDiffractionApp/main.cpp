// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QtWebEngineQuick/qtwebenginequickglobal.h>


int main(int argc, char *argv[])
{
    // QtWebEngine initialization for the QML GUI components
    QtWebEngineQuick::initialize();

    // Create application
    QGuiApplication app(argc, argv);

    // Create QML application engine
    QQmlApplicationEngine engine;

    // Add paths to be accessible from the QML components
    engine.addImportPath("qrc:/EasyApp");
    engine.addImportPath("qrc:/");

    // Load the root QML file
    engine.load("qrc:/Gui/main.qml");

    // Event loop
    if (engine.rootObjects().isEmpty())
        return -1;
    return app.exec();
}
