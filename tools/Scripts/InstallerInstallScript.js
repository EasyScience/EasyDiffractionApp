
function Component()
{
  if (installer.isInstaller())
  {
    installer.setDefaultPageVisible(QInstaller.ComponentSelection, false) // works for Installer, but not for Updater !?
  }
  //installer.setDefaultPageVisible(QInstaller.LicenseCheck, false)
}

// here we are creating the operation chain which will be processed at the real installation part later
Component.prototype.createOperations = function()
{
  // call default implementation to actually install the registeredfile
  component.createOperations();

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

  if (systemInfo.productType === "ubuntu")
  //if (installer.value("os") === "x11")
  {
    component.addOperation(
      "CreateDesktopEntry",
      "@TargetDir@/easyDiffraction.desktop",
      "Comment=A scientific software for modelling and analysis of the neutron diffraction data.\n"+
      "Type=Application\n"+
      "Exec=@TargetDir@/@ProductName@/@ProductName@\n"+
      "Path=@TargetDir@/@ProductName@\n"+
      "Name=easyDiffraction\n"+
      "GenericName=easyDiffraction\n"+
      "Icon=@TargetDir@/@ProductName@/QmlImports/@ProductName@/Resources/Icons/App.png\n"+
      "Terminal=false\n"+
      "Categories=Science;"
    )

    component.addOperation(
      "Copy",
      "@TargetDir@/easyDiffraction.desktop",
      "/usr/share/applications/easyDiffraction.desktop"
    )
  }

}
