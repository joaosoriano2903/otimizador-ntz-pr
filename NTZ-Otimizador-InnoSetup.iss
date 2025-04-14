; Script Inno Setup - NTZ Otimizador Instalador

[Setup]
AppName=NTZ Otimizador
AppVersion=1.0
DefaultDirName={pf}\NTZ Otimizador
DefaultGroupName=NTZ Otimizador
AllowNoIcons=yes
OutputDir=instalador
OutputBaseFilename=NTZ-Otimizador-Setup
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
SetupIconFile=assets\ntz_icon.ico

[Languages]
Name: "portuguese"; MessagesFile: "compiler:Languages\Portuguese.isl"

[Files]
Source: "dist\main\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "assets\ntz_icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\NTZ Otimizador"; Filename: "{app}\main.exe"; WorkingDir: "{app}"
Name: "{commondesktop}\NTZ Otimizador"; Filename: "{app}\main.exe"; WorkingDir: "{app}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na Área de Trabalho"; GroupDescription: "Opções adicionais:"

[Run]
Filename: "{app}\main.exe"; Description: "Executar NTZ Otimizador"; Flags: nowait postinstall skipifsilent

[Code]
procedure InitializeWizard;
begin
  WizardForm.Caption := 'Instalação do NTZ Otimizador';

  with TLabel.Create(WizardForm) do
  begin
    Parent := WizardForm;
    Left := ScaleX(10);
    Top := WizardForm.ClientHeight div 2 - ScaleY(100);
    Width := WizardForm.ClientWidth - ScaleX(20);
    AutoSize := False;
    WordWrap := True;
    Caption :=
      'TERMO DE RESPONSABILIDADE - NTZ OTIMIZADOR' + #13#10 +
      '============================================================' + #13#10#13#10 +
      'Este software foi desenvolvido exclusivamente pela NTZ Soluções em Informática.' + #13#10 +
      'Sua redistribuição é permitida, desde que não haja fins lucrativos.' + #13#10#13#10 +
      'É terminantemente proibida a VENDA ou comercialização deste programa por terceiros.' + #13#10 +
      'Apenas o criador e detentor dos direitos autorais está autorizado a realizar vendas.' + #13#10#13#10 +
      'Ao utilizar o NTZ Otimizador, o usuário declara estar ciente de que as otimizações são por conta e risco próprios,' + #13#10 +
      'não cabendo à NTZ qualquer responsabilidade por danos decorrentes do uso incorreto ou indevido.' + #13#10#13#10 +
      'Caso não concorde com os termos, cancele a instalação.' + #13#10#13#10 +
      'NTZ Soluções em Informática. Todos os direitos reservados.';
  end;
end;
