// SPDX-FileCopyrightText: 2021 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

function Component()
{
  //console.log("* isInstaller:", installer.isInstaller())
  //console.log("* isUninstaller:", installer.isUninstaller())
  //console.log("* isUpdater:", installer.isUpdater())
  //console.log("* isPackageManager:", installer.isPackageManager())

  //if (installer.isInstaller() || installer.isUpdater())
  //{
    installer.setDefaultPageVisible(QInstaller.ComponentSelection, false)
    installer.installationStarted.connect(this, Component.prototype.onInstallationStarted)
  //}
  //installer.setDefaultPageVisible(QInstaller.LicenseCheck, false)
}

Component.prototype.onInstallationStarted = function()
{
    if (component.updateRequested() || component.installationRequested()) {
        if (installer.value("os") == "win") {
            component.installerbaseBinaryPath = "@TargetDir@/signedmaintenancetool.exe"
        }
        installer.setInstallerBaseBinary(component.installerbaseBinaryPath)
    }
}

// here we are creating the operation chain which will be processed at the real installation part later
Component.prototype.createOperations = function()
{
  // call default implementation to actually install the registeredfile
  component.createOperations();

  // https://doc.qt.io/qtinstallerframework/operations.html
  if (systemInfo.productType === "windows")
  {
    // Add desktop shortcut for the app
    component.addOperation(
      "CreateShortcut",
      "@TargetDir@/@ProductName@/@ProductName@.exe",
      "@DesktopDir@/@ProductName@.lnk",
      "workingDirectory=@TargetDir@/@ProductName@",
      "iconPath=@TargetDir@/@ProductName@/@ProductName@.exe", "iconId=0",
      "description=@ProductName@"
    )

    // Add start menu shortcut for the app
    component.addOperation(
      "CreateShortcut",
      "@TargetDir@/@ProductName@/@ProductName@.exe",
      "@StartMenuDir@/@ProductName@/@ProductName@.lnk",
      "workingDirectory=@TargetDir@/@ProductName@",
      "iconPath=@TargetDir@/@ProductName@/@ProductName@.exe", "iconId=0",
      "description=@ProductName@"
    )

    // Add start menu shortcut for the app uninstaller
    /*
    component.addOperation(
      "CreateShortcut",
      "@TargetDir@/@ProductName@Uninstaller.exe",
      "@StartMenuDir@/@ProductName@/@ProductName@Uninstaller.lnk",
      "workingDirectory=@TargetDir@",
      "iconPath=@TargetDir@/@ProductName@Uninstaller.exe", "iconId=0",
      "description=@ProductName@Uninstaller"
    )
    */
  }

  //if (systemInfo.productType === "ubuntu")
  if (installer.value("os") === "x11")
  {
    component.addOperation(
      "CreateDesktopEntry",
      "@TargetDir@/@ProductName@.desktop",
      "Comment=A scientific software for modelling and analysis of the neutron diffraction data.\n"+
      "Type=Application\n"+
      "Exec=@TargetDir@/@ProductName@/@ProductName@\n"+
      "Path=@TargetDir@/@ProductName@\n"+
      "Name=@ProductName@\n"+
      "GenericName=@ProductName@\n"+
      "Icon=@TargetDir@/@ProductName@/@ProductName@App/Gui/Resources/Logo/App.png\n"+
      "Terminal=false\n"+
      "Categories=Science;"
    )

    /*
    component.addOperation(
      "Execute",
      "gio",
      "set", "@TargetDir@/@ProductName@.desktop",
      "'metadata::trusted'", "yes"
    )
    */

    component.addOperation(
      "Copy",
      "@TargetDir@/easyDiffraction.desktop",
      "@HomeDir@/.local/share/applications/easyDiffraction.desktop"
    )

    /*
    component.addOperation(
      "Copy",
      "@TargetDir@/easyDiffraction.desktop",
      "/usr/share/applications/easyDiffraction.desktop"
    )
    */
  }

}
