; Instalador profissional do SystemOptimizer
[Setup]
AppName=SystemOptimizer
AppVersion=1.1.0
DefaultDirName={pf}\SystemOptimizer
DefaultGroupName=SystemOptimizer
OutputDir=dist
OutputBaseFilename=SystemOptimizer_Installer
Compression=lzma2
SolidCompression=yes
SetupIconFile=assets\system_optimizer_icon.ico
UninstallDisplayIcon={app}\system_optimizer_icon.ico
PrivilegesRequired=admin
ArchitecturesAllowed=x86 x64
LicenseFile=docs\termo_de_uso.txt   

[Files]
Source: "dist\SystemOptimizer.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "assets\system_optimizer_icon.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\*.dll"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\SystemOptimizer"; Filename: "{app}\SystemOptimizer.exe"; IconFilename: "{app}\system_optimizer_icon.ico"
Name: "{commondesktop}\SystemOptimizer"; Filename: "{app}\SystemOptimizer.exe"; Tasks: desktopicon; IconFilename: "{app}\system_optimizer_icon.ico"
Name: "{userstartmenu}\SystemOptimizer"; Filename: "{app}\SystemOptimizer.exe"; IconFilename: "{app}\system_optimizer_icon.ico"

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na Área de Trabalho"; GroupDescription: "Opções adicionais:"; Flags: checkedonce

[Run]
Filename: "{app}\SystemOptimizer.exe"; Description: "Executar o SystemOptimizer agora"; Flags: nowait postinstall skipifsilent runascurrentuser

[UninstallDelete]
Type: files; Name: "{app}\system_optimizer_icon.ico"

[Messages]
WelcomeLabel1=Bem-vindo ao instalador do SystemOptimizer!
FinishedLabel=SystemOptimizer foi instalado com sucesso!
