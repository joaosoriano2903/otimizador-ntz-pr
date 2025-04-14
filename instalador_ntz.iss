[Code]
var
  Memo: TMemo;
  AcceptButton: TNewButton;

procedure AcceptClick(Sender: TObject);
begin
  WizardForm.NextButton.Enabled := True;
end;

procedure MemoScroll(Sender: TObject; ScrollCode: Integer; var ScrollPos: Integer);
begin
  if Memo.Perform(EM_GETFIRSTVISIBLELINE, 0, 0) + Memo.Height div Memo.Font.Height >= Memo.Lines.Count then
    AcceptButton.Enabled := True;
end;

procedure InitializeWizard;
begin
  WizardForm.Caption := 'Instalação do NTZ Otimizador';

  Memo := TMemo.Create(WizardForm);
  Memo.Parent := WizardForm;
  Memo.Left := ScaleX(10);
  Memo.Top := WizardForm.ClientHeight div 2;
  Memo.Width := WizardForm.ClientWidth - ScaleX(20);
  Memo.Height := ScaleY(150);
  Memo.ScrollBars := ssVertical;
  Memo.ReadOnly := True;
  Memo.WordWrap := True;
  Memo.OnVScroll := @MemoScroll;  // Aqui está o fix
  Memo.Lines.Text :=
    'TERMO DE RESPONSABILIDADE - NTZ OTIMIZADOR' + #13#10 +
    '============================================================' + #13#10 + #13#10 +
    'Este software foi desenvolvido exclusivamente pela NTZ Soluções em Informática.' + #13#10 +
    'Sua redistribuição é permitida, desde que não haja fins lucrativos.' + #13#10 + #13#10 +
    'É terminantemente proibida a VENDA ou comercialização deste programa por terceiros.' + #13#10 +
    'Apenas o criador e detentor dos direitos autorais está autorizado a realizar vendas.' + #13#10 + #13#10 +
    'Ao utilizar o NTZ Otimizador, o usuário declara estar ciente de que as otimizações são por conta e risco próprios,' + #13#10 +
    'não cabendo à NTZ qualquer responsabilidade por danos decorrentes do uso incorreto ou indevido.' + #13#10 + #13#10 +
    'Caso não concorde com os termos, cancele a instalação.' + #13#10 + #13#10 +
    'NTZ Soluções em Informática. Todos os direitos reservados.';

  AcceptButton := TNewButton.Create(WizardForm);
  AcceptButton.Caption := 'Li e concordo com os termos';
  AcceptButton.Enabled := False;
  AcceptButton.Parent := WizardForm;
  AcceptButton.Top := Memo.Top + Memo.Height + ScaleY(10);
  AcceptButton.Left := (WizardForm.ClientWidth - AcceptButton.Width) div 2;
  AcceptButton.OnClick := @AcceptClick;
end;

function NextButtonClick(CurPageID: Integer): Boolean;
begin
  if not AcceptButton.Enabled then
  begin
    MsgBox('Você deve rolar até o final do termo e aceitar para continuar.', mbError, MB_OK);
    Result := False;
  end else
    Result := True;
end;
